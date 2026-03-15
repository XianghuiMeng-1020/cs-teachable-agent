"""
Concept Relation Inference Engine

Automatically discovers and maps relationships between knowledge concepts.
Uses graph algorithms and semantic analysis.

Research Applications:
- Knowledge structure discovery
- Concept prerequisite identification
- Learning pathway optimization
- Misconception propagation analysis
"""

from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Optional
from enum import Enum
import re
from collections import defaultdict


class RelationType(Enum):
    """Types of concept relationships."""
    PREREQUISITE = "prerequisite"      # Must learn before
    DEPENDENT = "dependent"            # Builds upon
    SIMILAR = "similar"               # Related concepts
    CONTRAST = "contrast"             # Opposing concepts
    PART_OF = "part_of"               # Component relationship
    EXTENDS = "extends"               # Extension/Generalization
    APPLIES_TO = "applies_to"         # Application relationship


@dataclass
class ConceptRelation:
    """A relationship between two concepts."""
    source: str
    target: str
    relation_type: RelationType
    strength: float  # 0.0 to 1.0
    evidence: List[str]  # Supporting evidence
    confidence: float  # 0.0 to 1.0
    discovered_by: str  # "manual", "inferred", "pattern"


@dataclass
class ConceptNode:
    """A concept in the knowledge graph."""
    concept_id: str
    name: str
    description: str
    level: int  # Bloom's taxonomy level
    centrality: float  # Graph centrality score
    incoming: List[str]  # Prerequisites
    outgoing: List[str]  # Dependents


@dataclass
class KnowledgeGraph:
    """Complete knowledge graph."""
    nodes: Dict[str, ConceptNode]
    relations: List[ConceptRelation]
    clusters: List[List[str]]  # Concept clusters
    critical_paths: List[List[str]]  # Key learning paths


class ConceptRelationInferenceEngine:
    """
    Infers concept relationships from various sources.
    
    Sources:
    - Explicit prerequisites from curriculum
    - Co-occurrence in teaching materials
    - Student learning patterns
    - Semantic similarity in descriptions
    """
    
    def __init__(self):
        self.known_relations: List[ConceptRelation] = []
        self.concept_descriptions: Dict[str, str] = {}
        self.semantic_keywords: Dict[str, List[str]] = {}
    
    def infer_relations_from_curriculum(
        self,
        knowledge_units: List[Dict],
    ) -> List[ConceptRelation]:
        """
        Infer relations from curriculum structure.
        
        Args:
            knowledge_units: List of knowledge unit definitions
        
        Returns:
            List of inferred relations
        """
        relations = []
        
        # Extract explicit prerequisites
        for unit in knowledge_units:
            unit_id = unit.get("id", "")
            prereqs = unit.get("prerequisites", [])
            
            for prereq in prereqs:
                relations.append(ConceptRelation(
                    source=prereq,
                    target=unit_id,
                    relation_type=RelationType.PREREQUISITE,
                    strength=1.0,
                    evidence=["Explicitly defined in curriculum"],
                    confidence=1.0,
                    discovered_by="manual",
                ))
                
                # Also add reverse dependency
                relations.append(ConceptRelation(
                    source=unit_id,
                    target=prereq,
                    relation_type=RelationType.DEPENDENT,
                    strength=1.0,
                    evidence=["Reverse of prerequisite"],
                    confidence=1.0,
                    discovered_by="inferred",
                ))
        
        # Infer part-of relationships
        relations.extend(self._infer_part_of_relations(knowledge_units))
        
        # Infer extends relationships (generalization)
        relations.extend(self._infer_extends_relations(knowledge_units))
        
        return relations
    
    def infer_relations_from_learning_data(
        self,
        student_learning_sequences: List[List[str]],
    ) -> List[ConceptRelation]:
        """
        Infer relations from how students actually learn.
        
        Args:
            student_learning_sequences: Lists of concept learning order
        
        Returns:
            List of inferred relations
        """
        relations = []
        
        # Count co-occurrence and sequence patterns
        concept_pairs: Dict[Tuple[str, str], int] = defaultdict(int)
        
        for sequence in student_learning_sequences:
            for i in range(len(sequence)):
                for j in range(i + 1, min(i + 3, len(sequence))):  # Look 2 ahead
                    pair = (sequence[i], sequence[j])
                    concept_pairs[pair] += 1
        
        # Find significant patterns
        for (first, second), count in concept_pairs.items():
            if count >= 3:  # Minimum support
                strength = min(1.0, count / len(student_learning_sequences))
                
                relations.append(ConceptRelation(
                    source=first,
                    target=second,
                    relation_type=RelationType.PREREQUISITE,
                    strength=strength,
                    evidence=[f"Learned before in {count} student sequences"],
                    confidence=strength * 0.8,
                    discovered_by="pattern",
                ))
        
        return relations
    
    def infer_relations_from_semantics(
        self,
        concept_descriptions: Dict[str, str],
    ) -> List[ConceptRelation]:
        """
        Infer relations from concept descriptions.
        
        Uses keyword matching and semantic similarity.
        """
        relations = []
        
        # Extract keywords from each concept
        concept_keywords = {}
        for concept_id, description in concept_descriptions.items():
            keywords = self._extract_keywords(description)
            concept_keywords[concept_id] = keywords
        
        # Find similar concepts
        concept_ids = list(concept_keywords.keys())
        
        for i, id1 in enumerate(concept_ids):
            for id2 in concept_ids[i + 1:]:
                similarity = self._calculate_similarity(
                    concept_keywords[id1],
                    concept_keywords[id2]
                )
                
                if similarity > 0.5:
                    relations.append(ConceptRelation(
                        source=id1,
                        target=id2,
                        relation_type=RelationType.SIMILAR,
                        strength=similarity,
                        evidence=[f"{similarity:.0%} keyword overlap"],
                        confidence=similarity * 0.7,
                        discovered_by="inferred",
                    ))
                
                # Check for contrast keywords
                contrast_score = self._calculate_contrast(
                    concept_descriptions[id1],
                    concept_descriptions[id2]
                )
                
                if contrast_score > 0.6:
                    relations.append(ConceptRelation(
                        source=id1,
                        target=id2,
                        relation_type=RelationType.CONTRAST,
                        strength=contrast_score,
                        evidence=["Contrasting concepts detected"],
                        confidence=contrast_score * 0.7,
                        discovered_by="inferred",
                    ))
        
        return relations
    
    def infer_relations_from_misconceptions(
        self,
        misconception_data: List[Dict],
    ) -> List[ConceptRelation]:
        """
        Infer relations from common misconceptions.
        
        Often students confuse related concepts.
        """
        relations = []
        
        # Group misconceptions by confused concepts
        confusion_groups: Dict[str, List[str]] = defaultdict(list)
        
        for m in misconception_data:
            confused_with = m.get("confused_with", [])
            concept = m.get("concept_id", "")
            for other in confused_with:
                confusion_groups[concept].append(other)
        
        # Create similarity relations for frequently confused concepts
        for concept, confused_list in confusion_groups.items():
            for other in set(confused_list):
                frequency = confused_list.count(other)
                if frequency >= 2:
                    strength = min(1.0, frequency / 5)
                    
                    relations.append(ConceptRelation(
                        source=concept,
                        target=other,
                        relation_type=RelationType.SIMILAR,
                        strength=strength,
                        evidence=[f"Confused {frequency} times by students"],
                        confidence=strength * 0.9,
                        discovered_by="pattern",
                    ))
        
        return relations
    
    def build_knowledge_graph(
        self,
        concepts: List[Dict],
        all_relations: List[ConceptRelation],
    ) -> KnowledgeGraph:
        """
        Build complete knowledge graph from concepts and relations.
        """
        nodes: Dict[str, ConceptNode] = {}
        
        # Create nodes
        for concept in concepts:
            concept_id = concept.get("id", "")
            nodes[concept_id] = ConceptNode(
                concept_id=concept_id,
                name=concept.get("name", concept_id),
                description=concept.get("description", ""),
                level=concept.get("bloom_level", 1),
                centrality=0.0,
                incoming=[],
                outgoing=[],
            )
        
        # Populate relations in nodes
        for relation in all_relations:
            if relation.relation_type == RelationType.PREREQUISITE:
                if relation.target in nodes:
                    nodes[relation.target].incoming.append(relation.source)
                if relation.source in nodes:
                    nodes[relation.source].outgoing.append(relation.target)
        
        # Calculate centrality
        self._calculate_centrality(nodes)
        
        # Find clusters
        clusters = self._find_clusters(nodes, all_relations)
        
        # Find critical paths
        critical_paths = self._find_critical_paths(nodes)
        
        return KnowledgeGraph(
            nodes=nodes,
            relations=all_relations,
            clusters=clusters,
            critical_paths=critical_paths,
        )
    
    def discover_hidden_prerequisites(
        self,
        graph: KnowledgeGraph,
    ) -> List[ConceptRelation]:
        """
        Discover hidden prerequisites using graph algorithms.
        
        Transitive closure reveals implied prerequisites.
        """
        hidden = []
        
        # For each concept, find indirect prerequisites
        for concept_id, node in graph.nodes.items():
            # BFS to find all indirect prerequisites
            visited = set()
            queue = list(node.incoming)
            indirect = []
            
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                
                if current not in node.incoming:
                    indirect.append(current)
                
                if current in graph.nodes:
                    queue.extend(graph.nodes[current].incoming)
            
            # Add relations for significant indirect prerequisites
            for prereq in indirect[:3]:  # Top 3
                hidden.append(ConceptRelation(
                    source=prereq,
                    target=concept_id,
                    relation_type=RelationType.PREREQUISITE,
                    strength=0.5,
                    evidence=["Indirect prerequisite discovered via graph analysis"],
                    confidence=0.6,
                    discovered_by="inferred",
                ))
        
        return hidden
    
    def suggest_learning_order(
        self,
        graph: KnowledgeGraph,
        target_concepts: List[str],
    ) -> List[str]:
        """
        Suggest optimal learning order for target concepts.
        
        Uses topological sort with prerequisite handling.
        """
        # Collect all required concepts (target + prerequisites)
        required = set(target_concepts)
        
        for target in target_concepts:
            if target in graph.nodes:
                self._collect_prerequisites(graph, target, required)
        
        # Topological sort
        in_degree = {c: 0 for c in required}
        adjacency = defaultdict(list)
        
        for concept in required:
            if concept in graph.nodes:
                for prereq in graph.nodes[concept].incoming:
                    if prereq in required:
                        in_degree[concept] += 1
                        adjacency[prereq].append(concept)
        
        # Kahn's algorithm
        order = []
        queue = [c for c in required if in_degree[c] == 0]
        
        while queue:
            current = queue.pop(0)
            order.append(current)
            
            for neighbor in adjacency[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return order
    
    def _infer_part_of_relations(
        self,
        knowledge_units: List[Dict],
    ) -> List[ConceptRelation]:
        """Infer part-of relationships."""
        relations = []
        
        # Check for composite concepts
        for unit in knowledge_units:
            name = unit.get("name", "").lower()
            if " and " in name or " & " in name:
                parts = re.split(r"\s+(?:and|&)\s+", name)
                for part in parts:
                    part_clean = part.strip().replace(" ", "_")
                    relations.append(ConceptRelation(
                        source=part_clean,
                        target=unit.get("id", ""),
                        relation_type=RelationType.PART_OF,
                        strength=0.9,
                        evidence=[f"Component of composite concept: {name}"],
                        confidence=0.8,
                        discovered_by="inferred",
                    ))
        
        return relations
    
    def _infer_extends_relations(
        self,
        knowledge_units: List[Dict],
    ) -> List[ConceptRelation]:
        """Infer extension/generalization relationships."""
        relations = []
        
        # Check for "advanced" or "extended" concepts
        for unit in knowledge_units:
            name = unit.get("name", "").lower()
            if any(word in name for word in ["advanced", "extended", "complex"]):
                # Look for base concept
                base_name = name.replace("advanced", "").replace("extended", "").replace("complex", "").strip()
                base_id = base_name.replace(" ", "_")
                
                relations.append(ConceptRelation(
                    source=base_id,
                    target=unit.get("id", ""),
                    relation_type=RelationType.EXTENDS,
                    strength=0.8,
                    evidence=[f"{name} extends {base_name}"],
                    confidence=0.7,
                    discovered_by="inferred",
                ))
        
        return relations
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Simple keyword extraction
        words = re.findall(r'\b[a-zA-Z_]+\b', text.lower())
        # Filter common words
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been"}
        return [w for w in words if w not in stop_words and len(w) > 2]
    
    def _calculate_similarity(self, keywords1: List[str], keywords2: List[str]) -> float:
        """Calculate Jaccard similarity between keyword sets."""
        set1 = set(keywords1)
        set2 = set(keywords2)
        
        if not set1 or not set2:
            return 0.0
        
        intersection = set1 & set2
        union = set1 | set2
        
        return len(intersection) / len(union)
    
    def _calculate_contrast(self, desc1: str, desc2: str) -> float:
        """Calculate contrast score based on opposite keywords."""
        contrast_keywords = [
            ("mutable", "immutable"),
            ("local", "global"),
            ("static", "dynamic"),
            ("deep", "shallow"),
            ("public", "private"),
        ]
        
        score = 0.0
        for word1, word2 in contrast_keywords:
            if (word1 in desc1.lower() and word2 in desc2.lower()) or \
               (word2 in desc1.lower() and word1 in desc2.lower()):
                score += 0.3
        
        return min(1.0, score)
    
    def _calculate_centrality(self, nodes: Dict[str, ConceptNode]):
        """Calculate node centrality (simple degree centrality)."""
        for node in nodes.values():
            node.centrality = len(node.incoming) + len(node.outgoing)
    
    def _find_clusters(
        self,
        nodes: Dict[str, ConceptNode],
        relations: List[ConceptRelation],
    ) -> List[List[str]]:
        """Find concept clusters using connected components."""
        # Build adjacency for similar relations
        adjacency = defaultdict(set)
        
        for r in relations:
            if r.relation_type == RelationType.SIMILAR:
                adjacency[r.source].add(r.target)
                adjacency[r.target].add(r.source)
        
        # Find connected components
        visited = set()
        clusters = []
        
        for node_id in nodes:
            if node_id not in visited:
                cluster = []
                queue = [node_id]
                
                while queue:
                    current = queue.pop(0)
                    if current in visited:
                        continue
                    visited.add(current)
                    cluster.append(current)
                    queue.extend(adjacency[current] - visited)
                
                if len(cluster) > 1:
                    clusters.append(cluster)
        
        return clusters
    
    def _find_critical_paths(
        self,
        nodes: Dict[str, ConceptNode],
    ) -> List[List[str]]:
        """Find critical learning paths."""
        # Find paths from high-centrality entry points
        entry_points = [
            n.concept_id for n in nodes.values()
            if n.centrality >= 3 and len(n.incoming) <= 1
        ]
        
        paths = []
        for entry in entry_points[:3]:  # Top 3 entry points
            path = self._find_longest_path(nodes, entry, set())
            if len(path) >= 3:
                paths.append(path)
        
        return paths
    
    def _find_longest_path(
        self,
        nodes: Dict[str, ConceptNode],
        start: str,
        visited: Set[str],
    ) -> List[str]:
        """Find longest path from start node."""
        if start in visited or start not in nodes:
            return []
        
        visited.add(start)
        node = nodes[start]
        
        longest = [start]
        for next_node in node.outgoing:
            if next_node not in visited:
                subpath = self._find_longest_path(nodes, next_node, visited.copy())
                if len(subpath) + 1 > len(longest):
                    longest = [start] + subpath
        
        return longest
    
    def _collect_prerequisites(
        self,
        graph: KnowledgeGraph,
        concept: str,
        collected: Set[str],
    ):
        """Recursively collect all prerequisites."""
        if concept in graph.nodes:
            for prereq in graph.nodes[concept].incoming:
                if prereq not in collected:
                    collected.add(prereq)
                    self._collect_prerequisites(graph, prereq, collected)


def infer_concept_relations(
    knowledge_units: List[Dict],
    learning_sequences: List[List[str]],
    descriptions: Dict[str, str],
) -> Dict[str, any]:
    """
    Main API-facing function for concept relation inference.
    
    Args:
        knowledge_units: Knowledge unit definitions
        learning_sequences: Student learning sequences
        descriptions: Concept descriptions
    
    Returns:
        Complete knowledge graph and relations
    """
    engine = ConceptRelationInferenceEngine()
    
    # Infer from multiple sources
    curriculum_relations = engine.infer_relations_from_curriculum(knowledge_units)
    learning_relations = engine.infer_relations_from_learning_data(learning_sequences)
    semantic_relations = engine.infer_relations_from_semantics(descriptions)
    
    # Combine all relations
    all_relations = curriculum_relations + learning_relations + semantic_relations
    
    # Build graph
    graph = engine.build_knowledge_graph(knowledge_units, all_relations)
    
    # Discover hidden relations
    hidden = engine.discover_hidden_prerequisites(graph)
    all_relations.extend(hidden)
    
    # Update graph with hidden relations
    graph = engine.build_knowledge_graph(knowledge_units, all_relations)
    
    return {
        "concepts_count": len(graph.nodes),
        "relations_count": len(graph.relations),
        "clusters": graph.clusters,
        "critical_paths": graph.critical_paths,
        "central_concepts": [
            {"id": n.concept_id, "centrality": n.centrality}
            for n in sorted(graph.nodes.values(), key=lambda x: x.centrality, reverse=True)[:5]
        ],
        "relations_by_type": {
            t.value: len([r for r in graph.relations if r.relation_type == t])
            for t in RelationType
        },
    }
