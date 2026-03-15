"""
Smart Learning Path Recommendation System

Uses topological sorting with weighted edges to find optimal learning paths.
Considers:
- Prerequisite dependencies
- Knowledge unit difficulty
- Student's learning history
- BKT mastery probability
- Misconception impact
"""

from dataclasses import dataclass
from typing import Optional
import heapq


@dataclass
class KnowledgeNode:
    """Represents a knowledge unit in the learning graph."""
    id: str
    name: str
    prerequisites: list[str]
    difficulty: float  # 1.0 (easy) to 5.0 (hard)
    topic_group: str
    estimated_minutes: int
    importance: float  # 0.0 to 1.0, how central this concept is


@dataclass
class PathEdge:
    """Edge between two knowledge nodes with learning cost."""
    from_node: str
    to_node: str
    cost: float  # Combined metric of difficulty and prerequisite gap


@dataclass
class LearningPathRecommendation:
    """Recommended learning path with metadata."""
    sequence: list[KnowledgeNode]
    total_estimated_minutes: int
    total_difficulty: float
    path_confidence: float  # How confident we are this path is optimal
    rationale: str  # Explanation of why this path was chosen


def calculate_edge_cost(
    node: KnowledgeNode,
    prerequisite_mastery: dict[str, float],
    student_history: Optional[dict] = None
) -> float:
    """
    Calculate the learning cost for a knowledge unit.
    
    Lower cost = easier/more recommended to learn next.
    """
    base_cost = node.difficulty
    
    # Penalty for unmet prerequisites
    unmet_count = 0
    prereq_gap_penalty = 0.0
    for prereq in node.prerequisites:
        mastery = prerequisite_mastery.get(prereq, 0.0)
        if mastery < 0.5:  # Not sufficiently learned
            unmet_count += 1
            prereq_gap_penalty += (0.5 - mastery) * 2.0
    
    # If all prerequisites met, reduce cost (preferred path)
    if unmet_count == 0:
        base_cost *= 0.7  # 30% discount for ready-to-learn items
    else:
        base_cost += prereq_gap_penalty * 1.5
    
    # Boost important concepts
    importance_boost = (1.0 - node.importance) * 0.5
    base_cost -= importance_boost
    
    # Historical performance adjustment
    if student_history:
        # If student struggled with similar topic group before, increase cost
        topic_attempts = student_history.get("topic_attempts", {}).get(node.topic_group, {})
        if topic_attempts:
            failure_rate = topic_attempts.get("failures", 0) / max(1, topic_attempts.get("total", 1))
            base_cost += failure_rate * 1.0
    
    return max(0.1, base_cost)


def build_learning_graph(
    knowledge_units: list[dict],
    learned_units: set[str],
    bkt_state: Optional[dict[str, float]] = None,
    student_history: Optional[dict] = None
) -> tuple[dict[str, KnowledgeNode], dict[str, list[PathEdge]]]:
    """
    Build a weighted directed graph of knowledge units.
    
    Returns:
        - nodes: dict mapping unit_id to KnowledgeNode
        - edges: adjacency list mapping unit_id to list of outgoing edges
    """
    nodes: dict[str, KnowledgeNode] = {}
    
    # Calculate importance (centrality) based on how many other units depend on this
    dependency_count: dict[str, int] = {}
    for ku in knowledge_units:
        ku_id = ku["id"]
        for prereq in ku.get("prerequisites", []):
            dependency_count[prereq] = dependency_count.get(prereq, 0) + 1
    
    max_deps = max(dependency_count.values()) if dependency_count else 1
    
    # Create nodes
    for ku in knowledge_units:
        ku_id = ku["id"]
        if ku_id not in learned_units:  # Only include unlearned units
            importance = dependency_count.get(ku_id, 0) / max_deps
            nodes[ku_id] = KnowledgeNode(
                id=ku_id,
                name=ku.get("name", ku_id),
                prerequisites=ku.get("prerequisites", []),
                difficulty=ku.get("difficulty", 3.0),
                topic_group=ku.get("topic_group", "general"),
                estimated_minutes=ku.get("estimated_minutes", 10),
                importance=importance
            )
    
    # Build edges (prerequisite relationships)
    edges: dict[str, list[PathEdge]] = {node_id: [] for node_id in nodes}
    
    prerequisite_mastery = {
        ku_id: bkt_state.get(ku_id, 0.0) if bkt_state else (1.0 if ku_id in learned_units else 0.0)
        for ku_id in learned_units
    }
    
    for node_id, node in nodes.items():
        cost = calculate_edge_cost(node, prerequisite_mastery, student_history)
        # Create edges from prerequisites to this node
        for prereq in node.prerequisites:
            if prereq in nodes:  # Only add if prereq is also unlearned
                edges[prereq].append(PathEdge(from_node=prereq, to_node=node_id, cost=cost))
    
    return nodes, edges


def find_optimal_learning_path(
    nodes: dict[str, KnowledgeNode],
    edges: dict[str, list[PathEdge]],
    start_nodes: list[str],
    max_path_length: int = 10
) -> LearningPathRecommendation:
    """
    Find the optimal learning path using a modified Dijkstra's algorithm.
    
    Considers both cumulative cost and learning coherence.
    """
    if not start_nodes:
        return LearningPathRecommendation(
            sequence=[],
            total_estimated_minutes=0,
            total_difficulty=0.0,
            path_confidence=0.0,
            rationale="No recommended starting points available."
        )
    
    # Priority queue: (cumulative_cost, path_length, node_id, path_so_far)
    pq: list[tuple[float, int, str, list[str]]] = []
    
    for start in start_nodes:
        if start in nodes:
            heapq.heappush(pq, (0.0, 1, start, [start]))
    
    best_path: list[str] = []
    best_cost = float('inf')
    
    # Track visited to avoid cycles
    visited: set[tuple[str, int]] = set()
    
    while pq and len(best_path) < max_path_length:
        cost, length, node_id, path = heapq.heappop(pq)
        
        state = (node_id, length)
        if state in visited:
            continue
        visited.add(state)
        
        # Update best path if this is the most complete path found
        if length > len(best_path) or (length == len(best_path) and cost < best_cost):
            best_path = path
            best_cost = cost
        
        # Stop if we've reached max length
        if length >= max_path_length:
            break
        
        # Explore neighbors
        for edge in edges.get(node_id, []):
            next_node = edge.to_node
            if next_node not in nodes:
                continue
            
            # Check if adding this node would create a cycle
            if next_node in path:
                continue
            
            # Check prerequisites are met
            next_node_obj = nodes[next_node]
            prereqs_met = all(
                p in path or p not in nodes  # Either already in path or already learned
                for p in next_node_obj.prerequisites
            )
            
            if prereqs_met:
                new_cost = cost + edge.cost
                new_path = path + [next_node]
                heapq.heappush(pq, (new_cost, length + 1, next_node, new_path))
    
    # Build the recommendation
    sequence = [nodes[node_id] for node_id in best_path if node_id in nodes]
    
    total_minutes = sum(node.estimated_minutes for node in sequence)
    total_difficulty = sum(node.difficulty for node in sequence) / max(1, len(sequence))
    
    # Calculate confidence based on path completeness
    all_unlearned = set(nodes.keys())
    path_coverage = len(best_path) / max(1, len(all_unlearned))
    path_confidence = min(1.0, path_coverage * 2)  # Scale confidence
    
    # Generate rationale
    if sequence:
        rationale_parts = [
            f"Starting with '{sequence[0].name}' because its prerequisites are met.",
        ]
        
        # Group by topic for coherent learning
        topic_groups = {}
        for node in sequence:
            topic_groups.setdefault(node.topic_group, []).append(node.name)
        
        if len(topic_groups) == 1:
            rationale_parts.append(f"This path focuses on {list(topic_groups.keys())[0]} for coherent learning.")
        elif len(topic_groups) <= 3:
            rationale_parts.append(f"This path covers {len(topic_groups)} related topics sequentially.")
        
        if len(sequence) >= 3:
            rationale_parts.append(f"Complete in approximately {total_minutes} minutes across {len(sequence)} concepts.")
        
        rationale = " ".join(rationale_parts)
    else:
        rationale = "Unable to generate a learning path at this time."
    
    return LearningPathRecommendation(
        sequence=sequence,
        total_estimated_minutes=total_minutes,
        total_difficulty=total_difficulty,
        path_confidence=path_confidence,
        rationale=rationale
    )


def get_smart_learning_path(
    knowledge_units: list[dict],
    learned_units: set[str],
    bkt_state: Optional[dict[str, float]] = None,
    student_history: Optional[dict] = None,
    active_misconceptions: Optional[list[str]] = None
) -> LearningPathRecommendation:
    """
    Main entry point: Get an intelligent learning path recommendation.
    
    This is the function called by the API to get recommendations.
    """
    # Build the learning graph
    nodes, edges = build_learning_graph(
        knowledge_units=knowledge_units,
        learned_units=learned_units,
        bkt_state=bkt_state,
        student_history=student_history
    )
    
    if not nodes:
        return LearningPathRecommendation(
            sequence=[],
            total_estimated_minutes=0,
            total_difficulty=0.0,
            path_confidence=1.0,
            rationale="All concepts have been learned! Great job!"
        )
    
    # Find starting points (nodes with all prerequisites met)
    start_nodes = [
        node_id for node_id, node in nodes.items()
        if all(p in learned_units for p in node.prerequisites)
    ]
    
    # If no obvious start nodes, find the node with fewest unmet prerequisites
    if not start_nodes:
        min_unmet = float('inf')
        for node_id, node in nodes.items():
            unmet = sum(1 for p in node.prerequisites if p not in learned_units)
            if unmet < min_unmet:
                min_unmet = unmet
                start_nodes = [node_id]
            elif unmet == min_unmet:
                start_nodes.append(node_id)
    
    # Adjust for misconceptions - prioritize units that can address misconceptions
    if active_misconceptions:
        # Find units that can help with active misconceptions
        misconception_units: set[str] = set()
        for ku in knowledge_units:
            ku_misconceptions = ku.get("misconceptions_related", [])
            if any(m in active_misconceptions for m in ku_misconceptions):
                misconception_units.add(ku["id"])
        
        # Prioritize these units in start_nodes
        prioritized = [n for n in start_nodes if n in misconception_units]
        other = [n for n in start_nodes if n not in misconception_units]
        start_nodes = prioritized + other
    
    # Find the optimal path
    recommendation = find_optimal_learning_path(
        nodes=nodes,
        edges=edges,
        start_nodes=start_nodes,
        max_path_length=8
    )
    
    return recommendation


def format_learning_path_for_api(recommendation: LearningPathRecommendation) -> dict:
    """Convert recommendation to API response format."""
    return {
        "recommended": [
            {
                "id": node.id,
                "name": node.name,
                "topic_group": node.topic_group,
                "prerequisites": node.prerequisites,
                "difficulty": node.difficulty,
                "estimated_minutes": node.estimated_minutes,
            }
            for node in recommendation.sequence
        ],
        "path_summary": {
            "total_estimated_minutes": recommendation.total_estimated_minutes,
            "average_difficulty": round(recommendation.total_difficulty, 2),
            "confidence": round(recommendation.path_confidence, 2),
            "rationale": recommendation.rationale,
            "path_length": len(recommendation.sequence),
        },
        "learned_count": 0,  # Will be filled by caller
        "total_count": 0,  # Will be filled by caller
        "estimated_minutes_remaining": recommendation.total_estimated_minutes,
    }
