"""Demo accounts and sample data for AI Resistant Teaching System (ARTS-CS).

Creates demo users and teaching sessions for demonstration purposes.
Run: python seed/demo_accounts.py
"""
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.db.database import SessionLocal, init_db
from src.db.models import User, TAInstance, TeachingSession, TeachingEvent, TestAttempt, TraceEvent
from src.api.deps import get_password_hash
from src.core.knowledge_state import StateTracker
from src.api.domain_helpers import get_domain_adapter
import json

# Demo accounts
DEMO_STUDENTS = [
    {"username": "demo_student", "password": "demo123", "role": "student"},
    {"username": "alice_cs101", "password": "demo123", "role": "student"},
    {"username": "bob_python", "password": "demo123", "role": "student"},
]

DEMO_TEACHERS = [
    {"username": "demo_teacher", "password": "demo123", "role": "teacher"},
    {"username": "prof_chen", "password": "demo123", "role": "teacher"},
]

DEMO_TA_CONFIGS = [
    {"domain_id": "python", "name": "Python TA - Beginner"},
    {"domain_id": "python", "name": "Python TA - Intermediate"},
    {"domain_id": "database", "name": "SQL TA"},
    {"domain_id": "ai_literacy", "name": "AI Literacy TA"},
]

SAMPLE_TEACHING_INPUTS = [
    "Variables store values. You use the equals sign = to assign a value to a variable, like x = 5.",
    "The print function outputs text to the screen. You write print(\"Hello\") to display Hello.",
    "An if statement checks a condition. If the condition is True, the code inside runs.",
    "A for loop repeats code. Use for i in range(5) to repeat 5 times.",
    "Lists store multiple values. Create one with my_list = [1, 2, 3] and access with my_list[0].",
    "Functions are reusable code blocks. Define with def my_function(): and call with my_function().",
]

SAMPLE_TA_RESPONSES = [
    "Can you give me an example of assigning a different value to a variable?",
    "What happens if you print multiple things separated by commas?",
    "Can you show me an if statement with an else clause?",
    "How would you use a for loop to print numbers from 1 to 10?",
    "What happens if you try to access an index that doesn't exist in the list?",
    "Can you write a function that takes a parameter and returns a value?",
]


def create_demo_users(db):
    """Create demo student and teacher accounts."""
    created_users = []
    
    for user_data in DEMO_STUDENTS + DEMO_TEACHERS:
        # Check if user exists
        existing = db.query(User).filter(User.username == user_data["username"]).first()
        if existing:
            print(f"  User '{user_data['username']}' already exists (role: {user_data['role']})")
            created_users.append(existing)
            continue
        
        # Create user
        user = User(
            username=user_data["username"],
            password_hash=get_password_hash(user_data["password"]),
            role=user_data["role"],
        )
        db.add(user)
        db.flush()
        created_users.append(user)
        print(f"  Created {user_data['role']}: '{user_data['username']}' (id: {user.id})")
    
    db.commit()
    return created_users


def create_demo_ta_instances(db, student_users):
    """Create demo TA instances for students."""
    tas = []
    
    for user in student_users:
        # Create 1-2 TAs per student
        configs = DEMO_TA_CONFIGS[:2] if user.id % 2 == 0 else DEMO_TA_CONFIGS[:1]
        
        for config in configs:
            # Check if TA already exists for this user with this name
            existing = db.query(TAInstance).filter(
                TAInstance.user_id == user.id,
                TAInstance.name == config["name"]
            ).first()
            
            if existing:
                print(f"  TA '{config['name']}' for '{user.username}' already exists")
                tas.append(existing)
                continue
            
            # Initialize knowledge state for domain
            adapter = get_domain_adapter(config["domain_id"])
            units = adapter.load_knowledge_units()
            tracker = StateTracker(unit_definitions=units, domain=config["domain_id"])
            state = tracker.get_full_state()
            
            ta = TAInstance(
                user_id=user.id,
                domain_id=config["domain_id"],
                name=config["name"],
                knowledge_state=state,
            )
            db.add(ta)
            db.flush()
            tas.append(ta)
            print(f"  Created TA: '{config['name']}' ({config['domain_id']}) for '{user.username}'")
    
    db.commit()
    return tas


def create_sample_teaching_history(db, ta_instances):
    """Create sample teaching sessions and events for demo TAs."""
    import uuid
    
    for ta in ta_instances[:3]:  # Only for first 3 TAs
        # Create 1-2 sessions per TA
        num_sessions = 2 if ta.id % 2 == 0 else 1
        
        for session_num in range(num_sessions):
            # Create session
            session = TeachingSession(
                ta_instance_id=ta.id,
                started_at=datetime.now() - timedelta(days=session_num + 1),
                ended_at=datetime.now() - timedelta(days=session_num) if session_num == 0 else None,
            )
            db.add(session)
            db.flush()
            
            # Add 2-4 teaching events per session
            num_events = min(len(SAMPLE_TEACHING_INPUTS), 4)
            
            for i in range(num_events):
                event_id = str(uuid.uuid4())
                event = TeachingEvent(
                    session_id=session.id,
                    teaching_event_id=event_id,
                    student_input=SAMPLE_TEACHING_INPUTS[i],
                    topic_taught=SAMPLE_TEACHING_INPUTS[i].split(".")[0],
                    interpreted_units=["variable_assignment"] if "variable" in SAMPLE_TEACHING_INPUTS[i].lower() else ["print_function"],
                    quality_score=0.8 + (i * 0.05),
                    ta_response=SAMPLE_TA_RESPONSES[i],
                    created_at=session.started_at + timedelta(minutes=i * 10),
                )
                db.add(event)
            
            # Add trace events
            for i in range(num_events):
                trace = TraceEvent(
                    session_id=session.id,
                    event_type="teaching",
                    payload={
                        "input": SAMPLE_TEACHING_INPUTS[i],
                        "response": SAMPLE_TA_RESPONSES[i],
                    },
                    created_at=session.started_at + timedelta(minutes=i * 10),
                )
                db.add(trace)
            
            print(f"  Created session {session_num + 1} for TA '{ta.name}' with {num_events} teaching events")
    
    db.commit()


def create_demo_test_attempts(db, ta_instances):
    """Create sample test attempts for demo TAs."""
    import uuid
    
    for ta in ta_instances[:2]:  # Only for first 2 TAs
        # Get or create a session
        session = db.query(TeachingSession).filter(
            TeachingSession.ta_instance_id == ta.id
        ).first()
        
        if not session:
            continue
        
        # Create test attempts
        test_data = [
            {"problem_id": "prob_var_001", "passed": True, "score": 0.9},
            {"problem_id": "prob_io_001", "passed": False, "score": 0.3},
            {"problem_id": "prob_if_001", "passed": True, "score": 0.85},
        ]
        
        for i, test in enumerate(test_data):
            attempt = TestAttempt(
                session_id=session.id,
                problem_id=test["problem_id"],
                ta_code="# Sample TA code",
                passed=test["passed"],
                execution_output="Sample output" if test["passed"] else "Error: syntax error",
                score=test["score"],
                misconceptions_active=[],
            )
            db.add(attempt)
        
        print(f"  Created {len(test_data)} test attempts for TA '{ta.name}'")
    
    db.commit()


def main():
    """Main function to create all demo data."""
    print("=" * 70)
    print("Creating Demo Data for AI Resistant Teaching System (ARTS-CS)")
    print("=" * 70)
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        print("\n1. Creating Demo Users...")
        users = create_demo_users(db)
        
        # Filter student users
        student_users = [u for u in users if u.role == "student"]
        teacher_users = [u for u in users if u.role == "teacher"]
        
        print(f"\n   Total users: {len(users)} ({len(student_users)} students, {len(teacher_users)} teachers)")
        
        print("\n2. Creating Demo TA Instances...")
        tas = create_demo_ta_instances(db, student_users)
        print(f"\n   Total TA instances: {len(tas)}")
        
        print("\n3. Creating Sample Teaching History...")
        create_sample_teaching_history(db, tas)
        
        print("\n4. Creating Sample Test Attempts...")
        create_demo_test_attempts(db, tas)
        
        print("\n" + "=" * 70)
        print("Demo Data Created Successfully!")
        print("=" * 70)
        print("\nDemo Accounts:")
        print("  Students:")
        for u in DEMO_STUDENTS:
            print(f"    - {u['username']} / {u['password']}")
        print("  Teachers:")
        for u in DEMO_TEACHERS:
            print(f"    - {u['username']} / {u['password']}")
        print("\nYou can now log in at: https://cs-teachable-agent.pages.dev/login")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
