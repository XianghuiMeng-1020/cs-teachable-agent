"""
Cross-Domain Knowledge Transfer Analysis

Analyzes how knowledge transfers between Python, Database, and AI Literacy domains.
Identifies transferable skills and learning accelerations.

Research Applications:
- Transfer learning in education
- Domain adaptation
- Skill generalization
- Accelerated learning pathways
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Set
from enum import Enum
from collections import defaultdict


class Domain(Enum):
    """Learning domains."""
    PYTHON = "python"
    DATABASE = "database"
    AI_LITERACY = "ai_literacy"


class TransferType(Enum):
    """Types of knowledge transfer."""
    DIRECT = "direct"           # Direct application
    ANALOGICAL = "analogical"  # By analogy
    ABSTRACT = "abstract"       # Abstract principle
    SYNTACTIC = "syntactic"     # Surface-level similarity
    PROCEDURAL = "procedural"   # Process similarity


class TransferStrength(Enum):
    """Strength of transfer."""
    NONE = 0
    WEAK = 1
    MODERATE = 2
    STRONG = 3
    VERY_STRONG = 4


@dataclass
class ConceptMapping:
    """Mapping between concepts in different domains."""
    source_concept: str
    target_concept: str
    source_domain: Domain
    target_domain: Domain
    transfer_type: TransferType
    strength: TransferStrength
    explanation: str
    prerequisites: List[str]
    examples: List[str]


@dataclass
class TransferPathway:
    """Pathway for transferring knowledge."""
    student_id: int
    source_domain: Domain
    target_domain: Domain
    transferable_concepts: List[ConceptMapping]
    acceleration_factor: float  # 1.0 = normal, 2.0 = 2x faster
    estimated_time_saved: int  # hours
    recommended_sequence: List[str]
    potential_pitfalls: List[str]


@dataclass
class TransferAssessment:
    """Assessment of transfer readiness."""
    student_id: int
    source_domain: Domain
    source_mastery: float
    transfer_readiness: float  # 0-1
    transferable_skills: List[str]
    gaps_to_address: List[str]
    recommendations: List[str]


class CrossDomainTransferAnalyzer:
    """
    Analyzes and facilitates cross-domain knowledge transfer.
    
    Key Features:
    - Concept mapping between domains
    - Transfer pathway generation
    - Readiness assessment
    - Accelerated learning recommendations
    """
    
    # Predefined concept mappings
    CONCEPT_MAPPINGS = [
        # Python -> Database
        ConceptMapping(
            source_concept="variables",
            target_concept="columns",
            source_domain=Domain.PYTHON,
            target_domain=Domain.DATABASE,
            transfer_type=TransferType.DIRECT,
            strength=TransferStrength.STRONG,
            explanation="Variables in Python store data, similar to how columns store data in database tables",
            prerequisites=["data_types"],
            examples=["x = 5" → "column INT", "name = 'John'" → "column VARCHAR"],
        ),
        ConceptMapping(
            source_concept="lists",
            target_concept="tables",
            source_domain=Domain.PYTHON,
            target_domain=Domain.DATABASE,
            transfer_type=TransferType.ANALOGICAL,
            strength=TransferStrength.MODERATE,
            explanation="Lists are collections of items, tables are collections of rows",
            prerequisites=["data_structures"],
            examples=["[1, 2, 3]" → "table with rows 1, 2, 3"],
        ),
        ConceptMapping(
            source_concept="conditionals",
            target_concept="WHERE_clause",
            source_domain=Domain.PYTHON,
            target_domain=Domain.DATABASE,
            transfer_type=TransferType.DIRECT,
            strength=TransferStrength.VERY_STRONG,
            explanation="If statements filter code execution, WHERE filters data",
            prerequisites=["operators", "booleans"],
            examples=["if x > 5:" → "WHERE x > 5"],
        ),
        ConceptMapping(
            source_concept="loops",
            target_concept="JOIN_operations",
            source_domain=Domain.PYTHON,
            target_domain=Domain.DATABASE,
            transfer_type=TransferType.ABSTRACT,
            strength=TransferStrength.MODERATE,
            explanation="Loops iterate over collections, JOINs combine collections",
            prerequisites=["iteration", "collections"],
            examples=["for item in list:" → "JOIN combines tables"],
        ),
        ConceptMapping(
            source_concept="functions",
            target_concept="stored_procedures",
            source_domain=Domain.PYTHON,
            target_domain=Domain.DATABASE,
            transfer_type=TransferType.ANALOGICAL,
            strength=TransferStrength.MODERATE,
            explanation="Functions encapsulate reusable logic, stored procedures do the same in SQL",
            prerequisites=["parameters", "return_values"],
            examples=["def calculate(x):" → "CREATE PROCEDURE calculate"],
        ),
        
        # Python -> AI Literacy
        ConceptMapping(
            source_concept="functions",
            target_concept="models",
            source_domain=Domain.PYTHON,
            target_domain=Domain.AI_LITERACY,
            transfer_type=TransferType.ANALOGICAL,
            strength=TransferStrength.MODERATE,
            explanation="Functions transform inputs to outputs, ML models learn this transformation",
            prerequisites=["inputs_outputs"],
            examples=["def predict(x): return x * 2" → "model learns f(x) = wx + b"],
        ),
        ConceptMapping(
            source_concept="data_types",
            target_concept="features",
            source_domain=Domain.PYTHON,
            target_domain=Domain.AI_LITERACY,
            transfer_type=TransferType.DIRECT,
            strength=TransferStrength.STRONG,
            explanation="Understanding data types helps identify feature types for ML",
            prerequisites=["type_system"],
            examples=["int, float" → "numerical features", "string" → "categorical features"],
        ),
        ConceptMapping(
            source_concept="dictionaries",
            target_concept="feature_vectors",
            source_domain=Domain.PYTHON,
            target_domain=Domain.AI_LITERACY,
            transfer_type=TransferType.ANALOGICAL,
            strength=TransferStrength.MODERATE,
            explanation="Dictionaries map keys to values, feature vectors map features to values",
            prerequisites=["key_value_pairs"],
            examples=["{'age': 25, 'income': 50000}" → "feature vector [25, 50000]"],
        ),
        ConceptMapping(
            source_concept="conditionals",
            target_concept="decision_trees",
            source_domain=Domain.PYTHON,
            target_domain=Domain.AI_LITERACY,
            transfer_type=TransferType.DIRECT,
            strength=TransferStrength.VERY_STRONG,
            explanation="Decision trees are essentially nested if-else statements learned from data",
            prerequisites=["nested_conditionals"],
            examples=["if age > 18: if income > 50000:" → "decision tree splits"],
        ),
        
        # Database -> AI Literacy
        ConceptMapping(
            source_concept="aggregation",
            target_concept="summarization",
            source_domain=Domain.DATABASE,
            target_domain=Domain.AI_LITERACY,
            transfer_type=TransferType.ABSTRACT,
            strength=TransferStrength.MODERATE,
            explanation="Data aggregation summarizes information, similar to how AI extracts insights",
            prerequisites=["GROUP_BY", "aggregate_functions"],
            examples=["SELECT AVG(salary)" → "statistical summary for ML"],
        ),
        ConceptMapping(
            source_concept="query_optimization",
            target_concept="model_optimization",
            source_domain=Domain.DATABASE,
            target_domain=Domain.AI_LITERACY,
            transfer_type=TransferType.PROCEDURAL,
            strength=TransferStrength.WEAK,
            explanation="Both involve finding the most efficient way to process information",
            prerequisites=["performance_tuning"],
            examples=["query plan optimization" → "hyperparameter tuning"],
        ),
        ConceptMapping(
            source_concept="data_cleaning",
            target_concept="preprocessing",
            source_domain=Domain.DATABASE,
            target_domain=Domain.AI_LITERACY,
            transfer_type=TransferType.DIRECT,
            strength=TransferStrength.STRONG,
            explanation="Data cleaning in SQL directly applies to ML preprocessing",
            prerequisites=["NULL_handling", "data_validation"],
            examples=["DELETE NULL" → "imputation or removal"],
        ),
        
        # AI Literacy -> Python
        ConceptMapping(
            source_concept="prompt_engineering",
            target_concept="API_design",
            source_domain=Domain.AI_LITERACY,
            target_domain=Domain.PYTHON,
            transfer_type=TransferType.ANALOGICAL,
            strength=TransferStrength.MODERATE,
            explanation="Crafting prompts is like designing clear, effective function interfaces",
            prerequisites=["clear_instructions"],
            examples=["well-structured prompt" → "clear function signature"],
        ),
        ConceptMapping(
            source_concept="tokenization",
            target_concept="string_processing",
            source_domain=Domain.AI_LITERACY,
            target_domain=Domain.PYTHON,
            transfer_type=TransferType.DIRECT,
            strength=TransferStrength.MODERATE,
            explanation="Tokenization is advanced string splitting and processing",
            prerequisites=["string_methods", "split_join"],
            examples=["text.split()" → "tokenization"],
        ),
    ]
    
    def __init__(self):
        self.transfer_history: Dict[int, List[TransferPathway]] = {}
    
    def analyze_transfer_potential(
        self,
        student_id: int,
        source_domain: Domain,
        target_domain: Domain,
        source_mastery: Dict[str, float],
    ) -> TransferPathway:
        """
        Analyze potential for knowledge transfer between domains.
        
        Args:
            student_id: Student ID
            source_domain: Domain with existing knowledge
            target_domain: Target domain to learn
            source_mastery: Mastery levels of source concepts
        
        Returns:
            Transfer pathway with recommendations
        """
        # Find relevant mappings
        mappings = [
            m for m in self.CONCEPT_MAPPINGS
            if m.source_domain == source_domain and m.target_domain == target_domain
        ]
        
        # Filter by prerequisites
        transferable = []
        for mapping in mappings:
            # Check if prerequisites are met
            prereqs_met = all(
                source_mastery.get(p, 0) >= 0.7
                for p in mapping.prerequisites
            )
            
            if prereqs_met:
                # Calculate transfer score
                mastery = source_mastery.get(mapping.source_concept, 0)
                if mastery >= 0.6:  # Minimum mastery for transfer
                    transferable.append((mapping, mastery))
        
        # Sort by strength and mastery
        transferable.sort(
            key=lambda x: (x[0].strength.value, x[1]),
            reverse=True
        )
        
        # Calculate acceleration
        acceleration = self._calculate_acceleration(transferable)
        time_saved = self._estimate_time_saved(transferable, acceleration)
        
        # Generate sequence
        sequence = self._generate_learning_sequence(transferable, target_domain)
        
        # Identify pitfalls
        pitfalls = self._identify_pitfalls(transferable, target_domain)
        
        pathway = TransferPathway(
            student_id=student_id,
            source_domain=source_domain,
            target_domain=target_domain,
            transferable_concepts=[m for m, _ in transferable],
            acceleration_factor=acceleration,
            estimated_time_saved=time_saved,
            recommended_sequence=sequence,
            potential_pitfalls=pitfalls,
        )
        
        # Store in history
        if student_id not in self.transfer_history:
            self.transfer_history[student_id] = []
        self.transfer_history[student_id].append(pathway)
        
        return pathway
    
    def _calculate_acceleration(
        self,
        transferable: List[tuple],
    ) -> float:
        """Calculate learning acceleration factor."""
        if not transferable:
            return 1.0
        
        # Base acceleration from number of transferable concepts
        base_accel = 1.0 + len(transferable) * 0.1
        
        # Adjust by strength
        strength_bonus = sum(
            m.strength.value * 0.05
            for m, _ in transferable
        )
        
        # Adjust by mastery
        mastery_factor = sum(
            mastery * 0.1
            for _, mastery in transferable
        ) / len(transferable)
        
        acceleration = base_accel + strength_bonus + mastery_factor
        return min(3.0, acceleration)  # Cap at 3x
    
    def _estimate_time_saved(
        self,
        transferable: List[tuple],
        acceleration: float,
    ) -> int:
        """Estimate time saved through transfer."""
        # Base learning time for domain (hours)
        base_time = 40
        
        # Calculate effective time
        effective_time = base_time / acceleration
        
        # Time saved
        time_saved = int(base_time - effective_time)
        
        return max(0, time_saved)
    
    def _generate_learning_sequence(
        self,
        transferable: List[tuple],
        target_domain: Domain,
    ) -> List[str]:
        """Generate recommended learning sequence."""
        sequence = []
        
        # Start with strong transfers
        strong_transfers = [
            m.target_concept
            for m, _ in transferable
            if m.strength.value >= TransferStrength.STRONG.value
        ]
        sequence.extend(strong_transfers)
        
        # Add domain-specific fundamentals
        if target_domain == Domain.DATABASE:
            sequence.extend(["SQL_basics", "table_design", "normalization"])
        elif target_domain == Domain.AI_LITERACY:
            sequence.extend(["ML_concepts", "training_data", "evaluation"])
        elif target_domain == Domain.PYTHON:
            sequence.extend(["syntax_basics", "control_flow", "functions"])
        
        return sequence[:8]  # Limit sequence length
    
    def _identify_pitfalls(
        self,
        transferable: List[tuple],
        target_domain: Domain,
    ) -> List[str]:
        """Identify potential transfer pitfalls."""
        pitfalls = []
        
        # Check for false analogies
        weak_analogies = [m for m, _ in transferable if m.strength.value <= TransferStrength.WEAK.value]
        if weak_analogies:
            pitfalls.append(f"Don't over-rely on weak analogies: {', '.join(m.target_concept for m, _ in weak_analogies[:2])}")
        
        # Domain-specific warnings
        if target_domain == Domain.DATABASE:
            pitfalls.append("Remember SQL is declarative, not imperative")
            pitfalls.append("Data persistence differs from variable assignment")
        elif target_domain == Domain.AI_LITERACY:
            pitfalls.append("ML models are probabilistic, not deterministic")
            pitfalls.append("Training data quality is crucial - garbage in, garbage out")
        elif target_domain == Domain.PYTHON:
            pitfalls.append("Python syntax requires precise indentation")
        
        return pitfalls[:4]
    
    def assess_transfer_readiness(
        self,
        student_id: int,
        source_domain: Domain,
        source_mastery: Dict[str, float],
    ) -> TransferAssessment:
        """Assess readiness for knowledge transfer."""
        # Calculate overall mastery
        if source_mastery:
            avg_mastery = sum(source_mastery.values()) / len(source_mastery)
        else:
            avg_mastery = 0
        
        # Determine transferable skills
        transferable_skills = []
        gaps = []
        
        for mapping in self.CONCEPT_MAPPINGS:
            if mapping.source_domain == source_domain:
                mastery = source_mastery.get(mapping.source_concept, 0)
                
                if mastery >= 0.7:
                    transferable_skills.append(mapping.source_concept)
                elif mastery >= 0.4:
                    gaps.append(f"Strengthen {mapping.source_concept} for better transfer")
        
        # Calculate readiness score
        readiness = min(1.0, avg_mastery * 1.2 + len(transferable_skills) * 0.05)
        
        # Generate recommendations
        recommendations = []
        if readiness >= 0.8:
            recommendations.append("Excellent readiness! You can start learning the new domain.")
            recommendations.append(f"You have {len(transferable_skills)} transferable skills")
        elif readiness >= 0.6:
            recommendations.append("Good foundation. Address the identified gaps first.")
            recommendations.append("Focus on strengthening core concepts")
        else:
            recommendations.append("Build stronger foundation in current domain first")
            recommendations.append("Aim for 70%+ mastery in core concepts")
        
        return TransferAssessment(
            student_id=student_id,
            source_domain=source_domain,
            source_mastery=round(avg_mastery, 2),
            transfer_readiness=round(readiness, 2),
            transferable_skills=transferable_skills[:5],
            gaps_to_address=gaps[:3],
            recommendations=recommendations,
        )
    
    def get_transfer_statistics(self, student_id: int) -> Dict:
        """Get transfer statistics for a student."""
        history = self.transfer_history.get(student_id, [])
        
        if not history:
            return {"message": "No transfer history available"}
        
        total_time_saved = sum(p.estimated_time_saved for p in history)
        avg_acceleration = sum(p.acceleration_factor for p in history) / len(history)
        
        domain_pairs = [
            f"{p.source_domain.value} → {p.target_domain.value}"
            for p in history
        ]
        
        return {
            "total_transfers": len(history),
            "total_time_saved_hours": total_time_saved,
            "average_acceleration": round(avg_acceleration, 2),
            "transfer_pairs": domain_pairs,
            "most_effective_transfer": max(history, key=lambda p: p.acceleration_factor).__dict__ if history else None,
        }


def analyze_cross_domain_transfer(
    student_id: int,
    source_domain: str,
    target_domain: str,
    source_mastery: Dict[str, float],
) -> Dict:
    """
    Main API-facing function for transfer analysis.
    
    Args:
        student_id: Student ID
        source_domain: Source domain name
        target_domain: Target domain name
        source_mastery: Concept mastery levels
    
    Returns:
        Transfer analysis results
    """
    analyzer = CrossDomainTransferAnalyzer()
    
    source = Domain(source_domain)
    target = Domain(target_domain)
    
    # Analyze transfer potential
    pathway = analyzer.analyze_transfer_potential(
        student_id, source, target, source_mastery
    )
    
    # Assess readiness
    assessment = analyzer.assess_transfer_readiness(
        student_id, source, source_mastery
    )
    
    return {
        "transfer_pathway": {
            "source_domain": pathway.source_domain.value,
            "target_domain": pathway.target_domain.value,
            "acceleration_factor": round(pathway.acceleration_factor, 2),
            "estimated_time_saved_hours": pathway.estimated_time_saved,
            "transferable_concepts": [
                {
                    "source": m.source_concept,
                    "target": m.target_concept,
                    "type": m.transfer_type.value,
                    "strength": m.strength.value,
                    "explanation": m.explanation,
                }
                for m in pathway.transferable_concepts
            ],
            "recommended_sequence": pathway.recommended_sequence,
            "potential_pitfalls": pathway.potential_pitfalls,
        },
        "transfer_readiness": {
            "source_mastery": assessment.source_mastery,
            "transfer_readiness": assessment.transfer_readiness,
            "transferable_skills": assessment.transferable_skills,
            "gaps_to_address": assessment.gaps_to_address,
            "recommendations": assessment.recommendations,
        },
    }
