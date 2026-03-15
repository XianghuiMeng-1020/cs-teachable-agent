"""
Collaborative Learning System

Enables multiple students to teach the same TA simultaneously,
with real-time synchronization, discussion, and leaderboards.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from datetime import datetime
from typing import Optional
import json

from src.api.deps import DbSession, CurrentUser
from src.api.domain_helpers import get_domain_adapter, get_tracker_for_ta
from src.db.models import (
    TAInstance, CollaborationRoom, CollaborationParticipant,
    CollaborationMessage, User, TeachingEvent, GamificationProfile
)

router = APIRouter(prefix="/api/collaboration", tags=["collaboration"])


def _get_or_create_collaboration_room(
    db: DbSession, 
    domain_id: str, 
    room_name: Optional[str] = None
) -> CollaborationRoom:
    """Get existing public room or create a new one for this domain."""
    room = db.query(CollaborationRoom).filter(
        CollaborationRoom.domain_id == domain_id,
        CollaborationRoom.is_active == True,
        CollaborationRoom.is_private == False
    ).first()
    
    if not room:
        room = CollaborationRoom(
            name=room_name or f"{domain_id.upper()} Study Group",
            domain_id=domain_id,
            is_private=False,
            max_participants=10,
            created_at=datetime.utcnow(),
            is_active=True,
        )
        db.add(room)
        db.commit()
        db.refresh(room)
    
    return room


@router.post("/join")
def join_collaboration_room(
    domain_id: str,
    current_user: CurrentUser,
    db: DbSession,
    room_id: Optional[int] = None,
):
    """Join a collaboration room for a domain."""
    if room_id:
        room = db.query(CollaborationRoom).filter(
            CollaborationRoom.id == room_id,
            CollaborationRoom.is_active == True
        ).first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
    else:
        room = _get_or_create_collaboration_room(db, domain_id)
    
    # Check if already participant
    existing = db.query(CollaborationParticipant).filter(
        CollaborationParticipant.room_id == room.id,
        CollaborationParticipant.user_id == current_user.id
    ).first()
    
    if existing:
        existing.last_active_at = datetime.utcnow()
        db.commit()
        return {
            "room_id": room.id,
            "room_name": room.name,
            "domain_id": room.domain_id,
            "participant_id": existing.id,
            "joined_at": existing.joined_at.isoformat(),
        }
    
    # Check room capacity
    participant_count = db.query(func.count(CollaborationParticipant.id)).filter(
        CollaborationParticipant.room_id == room.id
    ).scalar()
    
    if participant_count >= room.max_participants:
        raise HTTPException(status_code=403, detail="Room is full")
    
    # Create TA instance for this user in the collaboration room
    ta = TAInstance(
        user_id=current_user.id,
        domain_id=room.domain_id,
        name=f"Collaborative TA - {room.name}",
        knowledge_state={},
        created_at=datetime.utcnow(),
    )
    db.add(ta)
    db.flush()
    
    # Add participant
    participant = CollaborationParticipant(
        room_id=room.id,
        user_id=current_user.id,
        ta_instance_id=ta.id,
        joined_at=datetime.utcnow(),
        last_active_at=datetime.utcnow(),
        contribution_score=0,
    )
    db.add(participant)
    db.commit()
    
    return {
        "room_id": room.id,
        "room_name": room.name,
        "domain_id": room.domain_id,
        "participant_id": participant.id,
        "ta_instance_id": ta.id,
        "joined_at": participant.joined_at.isoformat(),
    }


@router.get("/room/{room_id}/participants")
def get_room_participants(
    room_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get all participants in a collaboration room with their progress."""
    room = db.query(CollaborationRoom).filter(
        CollaborationRoom.id == room_id
    ).first()
    
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    participants = db.query(CollaborationParticipant).filter(
        CollaborationParticipant.room_id == room_id
    ).all()
    
    result = []
    for p in participants:
        user = db.query(User).filter(User.id == p.user_id).first()
        
        # Get TA progress
        if p.ta_instance_id:
            ta = db.query(TAInstance).filter(TAInstance.id == p.ta_instance_id).first()
            if ta:
                tracker = get_tracker_for_ta(ta)
                learned_count = len(tracker.get_learned_units())
                total_kus = len(ta.domain_adapter.load_knowledge_units())
            else:
                learned_count = 0
                total_kus = 0
        else:
            learned_count = 0
            total_kus = 0
        
        # Get contribution score from gamification
        gamification = db.query(GamificationProfile).filter(
            GamificationProfile.user_id == p.user_id
        ).first()
        
        result.append({
            "participant_id": p.id,
            "user_id": p.user_id,
            "username": user.username if user else "Unknown",
            "joined_at": p.joined_at.isoformat() if p.joined_at else None,
            "last_active_at": p.last_active_at.isoformat() if p.last_active_at else None,
            "contribution_score": p.contribution_score or 0,
            "progress": {
                "learned_count": learned_count,
                "total_count": total_kus,
                "percentage": round((learned_count / max(1, total_kus)) * 100, 1),
            },
            "gamification": {
                "points": gamification.points if gamification else 0,
                "level": gamification.level if gamification else 1,
            } if gamification else None,
        })
    
    # Sort by contribution score (descending)
    result.sort(key=lambda x: x["contribution_score"], reverse=True)
    
    return {
        "room_id": room_id,
        "room_name": room.name,
        "participants": result,
        "total_participants": len(result),
    }


@router.post("/room/{room_id}/message")
def post_collaboration_message(
    room_id: int,
    message: str,
    message_type: str = "chat",  # chat, teaching_tip, question, celebration
    current_user: CurrentUser = Depends(),
    db: DbSession = Depends(),
):
    """Post a message to the collaboration room."""
    # Verify participant
    participant = db.query(CollaborationParticipant).filter(
        CollaborationParticipant.room_id == room_id,
        CollaborationParticipant.user_id == current_user.id
    ).first()
    
    if not participant:
        raise HTTPException(status_code=403, detail="Not a participant of this room")
    
    # Create message
    msg = CollaborationMessage(
        room_id=room_id,
        participant_id=participant.id,
        user_id=current_user.id,
        message_type=message_type,
        content=message,
        created_at=datetime.utcnow(),
    )
    db.add(msg)
    
    # Update contribution score for helpful messages
    if message_type in ["teaching_tip", "answer"]:
        participant.contribution_score = (participant.contribution_score or 0) + 5
    elif message_type == "celebration":
        participant.contribution_score = (participant.contribution_score or 0) + 2
    else:
        participant.contribution_score = (participant.contribution_score or 0) + 1
    
    participant.last_active_at = datetime.utcnow()
    db.commit()
    
    return {
        "message_id": msg.id,
        "posted_at": msg.created_at.isoformat() if msg.created_at else None,
    }


@router.get("/room/{room_id}/messages")
def get_collaboration_messages(
    room_id: int,
    current_user: CurrentUser,
    db: DbSession,
    since: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
):
    """Get messages from collaboration room."""
    # Verify participant
    participant = db.query(CollaborationParticipant).filter(
        CollaborationParticipant.room_id == room_id,
        CollaborationParticipant.user_id == current_user.id
    ).first()
    
    if not participant:
        raise HTTPException(status_code=403, detail="Not a participant of this room")
    
    query = db.query(CollaborationMessage).filter(
        CollaborationMessage.room_id == room_id
    )
    
    if since:
        try:
            since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            query = query.filter(CollaborationMessage.created_at > since_dt)
        except ValueError:
            pass
    
    messages = query.order_by(CollaborationMessage.created_at.desc()).limit(limit).all()
    
    result = []
    for msg in messages:
        user = db.query(User).filter(User.id == msg.user_id).first()
        result.append({
            "id": msg.id,
            "user_id": msg.user_id,
            "username": user.username if user else "Unknown",
            "message_type": msg.message_type,
            "content": msg.content,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
        })
    
    return {
        "messages": list(reversed(result)),
        "room_id": room_id,
    }


@router.get("/leaderboard")
def get_collaboration_leaderboard(
    current_user: CurrentUser,
    db: DbSession,
    domain_id: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
):
    """Get global collaboration leaderboard."""
    query = db.query(
        CollaborationParticipant.user_id,
        func.sum(CollaborationParticipant.contribution_score).label("total_score"),
        func.count(CollaborationParticipant.id).label("rooms_joined"),
    ).group_by(CollaborationParticipant.user_id)
    
    if domain_id:
        # Filter by domain through room
        query = query.join(CollaborationRoom).filter(CollaborationRoom.domain_id == domain_id)
    
    leaders = query.order_by(func.sum(CollaborationParticipant.contribution_score).desc()).limit(limit).all()
    
    result = []
    for rank, (user_id, total_score, rooms_joined) in enumerate(leaders, 1):
        user = db.query(User).filter(User.id == user_id).first()
        
        # Get gamification data
        gamification = db.query(GamificationProfile).filter(
            GamificationProfile.user_id == user_id
        ).first()
        
        result.append({
            "rank": rank,
            "user_id": user_id,
            "username": user.username if user else "Unknown",
            "contribution_score": total_score or 0,
            "rooms_joined": rooms_joined or 0,
            "level": gamification.level if gamification else 1,
            "points": gamification.points if gamification else 0,
        })
    
    return {
        "leaderboard": result,
        "domain": domain_id or "all",
        "total_users": len(result),
    }


@router.post("/sync-teaching")
def sync_teaching_event(
    room_id: int,
    teaching_event: dict,
    current_user: CurrentUser,
    db: DbSession,
):
    """Sync a teaching event to all room participants."""
    participant = db.query(CollaborationParticipant).filter(
        CollaborationParticipant.room_id == room_id,
        CollaborationParticipant.user_id == current_user.id
    ).first()
    
    if not participant:
        raise HTTPException(status_code=403, detail="Not a participant")
    
    # Update contribution score for teaching
    topic = teaching_event.get("topic_taught", "")
    if topic:
        participant.contribution_score = (participant.contribution_score or 0) + 10
        participant.last_active_at = datetime.utcnow()
        db.commit()
    
    return {
        "synced": True,
        "room_id": room_id,
        "contribution_bonus": 10,
    }


@router.get("/active-rooms")
def get_active_collaboration_rooms(
    current_user: CurrentUser,
    db: DbSession,
    domain_id: Optional[str] = None,
):
    """Get list of active public collaboration rooms."""
    query = db.query(CollaborationRoom).filter(
        CollaborationRoom.is_active == True,
        CollaborationRoom.is_private == False
    )
    
    if domain_id:
        query = query.filter(CollaborationRoom.domain_id == domain_id)
    
    rooms = query.all()
    
    result = []
    for room in rooms:
        participant_count = db.query(func.count(CollaborationParticipant.id)).filter(
            CollaborationParticipant.room_id == room.id
        ).scalar()
        
        # Check if current user is in this room
        is_member = db.query(CollaborationParticipant).filter(
            CollaborationParticipant.room_id == room.id,
            CollaborationParticipant.user_id == current_user.id
        ).first() is not None
        
        result.append({
            "room_id": room.id,
            "name": room.name,
            "domain_id": room.domain_id,
            "participant_count": participant_count,
            "max_participants": room.max_participants,
            "is_member": is_member,
            "created_at": room.created_at.isoformat() if room.created_at else None,
        })
    
    return {"rooms": result}
