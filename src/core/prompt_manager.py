"""M-64 & M-65: Prompt versioning metadata and A/B testing framework."""

import hashlib
import json
import logging
import random
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class PromptVersionStatus(Enum):
    """Status of a prompt version."""

    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


@dataclass
class PromptVersion:
    """M-64: Prompt version with metadata."""

    prompt_id: str
    version: str
    template: str
    description: str
    created_at: datetime
    author: str
    status: PromptVersionStatus
    tags: list[str] = field(default_factory=list)
    parameters: dict[str, Any] = field(default_factory=dict)
    model_config: dict[str, Any] = field(default_factory=dict)
    expected_output_schema: Optional[dict] = None
    checksum: str = ""
    parent_version: Optional[str] = None
    change_notes: str = ""

    def __post_init__(self):
        if not self.checksum:
            self.checksum = self._calculate_checksum()

    def _calculate_checksum(self) -> str:
        """Calculate SHA-256 checksum of prompt template."""
        return hashlib.sha256(self.template.encode()).hexdigest()[:16]

    def to_dict(self) -> dict:
        return {
            "prompt_id": self.prompt_id,
            "version": self.version,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "author": self.author,
            "status": self.status.value,
            "tags": self.tags,
            "parameters": self.parameters,
            "model_config": self.model_config,
            "expected_output_schema": self.expected_output_schema,
            "checksum": self.checksum,
            "parent_version": self.parent_version,
            "change_notes": self.change_notes,
            "template_preview": self.template[:200] + "..." if len(self.template) > 200 else self.template,
        }


@dataclass
class ABTestVariant:
    """M-65: A/B test variant configuration."""

    variant_id: str
    name: str
    prompt_version: str
    weight: float  # 0.0-1.0, sum of all variants should be 1.0
    traffic_percentage: float  # For analytics
    success_metrics: dict[str, Any] = field(default_factory=dict)


@dataclass
class ABTest:
    """M-65: A/B test configuration."""

    test_id: str
    name: str
    prompt_id: str
    description: str
    created_at: datetime
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: str  # "draft", "running", "paused", "completed"
    variants: list[ABTestVariant]
    success_criteria: dict[str, Any]
    traffic_allocation: float = 1.0  # 0.0-1.0, percentage of traffic in test

    def select_variant(self, user_id: Optional[str] = None) -> ABTestVariant:
        """Select a variant based on weights or user hash."""
        if user_id:
            # Deterministic assignment based on user_id
            hash_val = int(hashlib.md5(f"{self.test_id}:{user_id}".encode()).hexdigest(), 16)
            bucket = (hash_val % 100) / 100
        else:
            # Random assignment
            bucket = random.random()

        cumulative = 0.0
        for variant in self.variants:
            cumulative += variant.weight
            if bucket < cumulative:
                return variant

        # Fallback to last variant
        return self.variants[-1]

    def to_dict(self) -> dict:
        return {
            "test_id": self.test_id,
            "name": self.name,
            "prompt_id": self.prompt_id,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status,
            "variants": [
                {
                    "variant_id": v.variant_id,
                    "name": v.name,
                    "prompt_version": v.prompt_version,
                    "weight": v.weight,
                    "traffic_percentage": v.traffic_percentage,
                }
                for v in self.variants
            ],
            "success_criteria": self.success_criteria,
            "traffic_allocation": self.traffic_allocation,
        }


class PromptManager:
    """Manager for prompt versions and A/B tests."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self._versions: dict[str, list[PromptVersion]] = {}
        self._active_versions: dict[str, PromptVersion] = {}
        self._ab_tests: dict[str, ABTest] = {}
        self._user_assignments: dict[tuple[str, str], str] = {}  # (test_id, user_id) -> variant_id

    def register_version(self, version: PromptVersion) -> None:
        """Register a new prompt version."""
        if version.prompt_id not in self._versions:
            self._versions[version.prompt_id] = []

        # Check for duplicate versions
        existing = [v for v in self._versions[version.prompt_id] if v.version == version.version]
        if existing:
            raise ValueError(f"Version {version.version} already exists for prompt {version.prompt_id}")

        self._versions[version.prompt_id].append(version)
        logger.info("Registered prompt version: %s@%s", version.prompt_id, version.version)

        # Auto-activate if first version
        if version.status == PromptVersionStatus.ACTIVE:
            self._active_versions[version.prompt_id] = version

    def get_version(self, prompt_id: str, version: Optional[str] = None) -> Optional[PromptVersion]:
        """Get a specific version or the active version."""
        if version:
            versions = self._versions.get(prompt_id, [])
            for v in versions:
                if v.version == version:
                    return v
            return None
        return self._active_versions.get(prompt_id)

    def set_active_version(self, prompt_id: str, version: str) -> bool:
        """Set a specific version as active."""
        versions = self._versions.get(prompt_id, [])
        for v in versions:
            if v.version == version:
                # Deactivate current
                if prompt_id in self._active_versions:
                    self._active_versions[prompt_id].status = PromptVersionStatus.DEPRECATED
                # Activate new
                v.status = PromptVersionStatus.ACTIVE
                self._active_versions[prompt_id] = v
                logger.info("Activated prompt version: %s@%s", prompt_id, version)
                return True
        return False

    def list_versions(self, prompt_id: str) -> list[PromptVersion]:
        """List all versions of a prompt."""
        return sorted(
            self._versions.get(prompt_id, []),
            key=lambda v: v.created_at,
            reverse=True,
        )

    def create_ab_test(
        self,
        test_id: str,
        name: str,
        prompt_id: str,
        description: str,
        variants: list[ABTestVariant],
        success_criteria: dict[str, Any],
        traffic_allocation: float = 1.0,
    ) -> ABTest:
        """M-65: Create a new A/B test."""
        # Validate variant weights
        total_weight = sum(v.weight for v in variants)
        if abs(total_weight - 1.0) > 0.001:
            raise ValueError(f"Variant weights must sum to 1.0, got {total_weight}")

        test = ABTest(
            test_id=test_id,
            name=name,
            prompt_id=prompt_id,
            description=description,
            created_at=datetime.utcnow(),
            start_date=None,
            end_date=None,
            status="draft",
            variants=variants,
            success_criteria=success_criteria,
            traffic_allocation=traffic_allocation,
        )

        self._ab_tests[test_id] = test
        logger.info("Created A/B test: %s for prompt %s", test_id, prompt_id)
        return test

    def start_ab_test(self, test_id: str) -> bool:
        """Start an A/B test."""
        test = self._ab_tests.get(test_id)
        if not test:
            return False

        test.status = "running"
        test.start_date = datetime.utcnow()
        logger.info("Started A/B test: %s", test_id)
        return True

    def stop_ab_test(self, test_id: str) -> bool:
        """Stop an A/B test."""
        test = self._ab_tests.get(test_id)
        if not test:
            return False

        test.status = "completed"
        test.end_date = datetime.utcnow()
        logger.info("Stopped A/B test: %s", test_id)
        return True

    def get_prompt_for_user(
        self,
        prompt_id: str,
        user_id: Optional[str] = None,
        test_id: Optional[str] = None,
    ) -> tuple[Optional[PromptVersion], Optional[str]]:
        """M-65: Get prompt version for a user, considering A/B test assignment."""
        # Check if there's a running A/B test for this prompt
        if not test_id:
            for tid, test in self._ab_tests.items():
                if test.prompt_id == prompt_id and test.status == "running":
                    test_id = tid
                    break

        if test_id and test_id in self._ab_tests:
            test = self._ab_tests[test_id]

            # Check if already assigned
            if user_id:
                assignment_key = (test_id, user_id)
                if assignment_key in self._user_assignments:
                    variant_id = self._user_assignments[assignment_key]
                    for v in test.variants:
                        if v.variant_id == variant_id:
                            return self.get_version(prompt_id, v.prompt_version), test_id

            # Select and record assignment
            variant = test.select_variant(user_id)
            if user_id:
                self._user_assignments[(test_id, user_id)] = variant.variant_id

            return self.get_version(prompt_id, variant.prompt_version), test_id

        # No A/B test, return active version
        return self.get_version(prompt_id), None

    def record_test_result(
        self,
        test_id: str,
        variant_id: str,
        user_id: Optional[str],
        metrics: dict[str, Any],
    ) -> None:
        """Record result metrics for an A/B test variant."""
        # In production, this would write to a database or analytics system
        logger.info(
            "A/B test result: %s variant=%s metrics=%s",
            test_id,
            variant_id,
            json.dumps(metrics, default=str),
        )

    def get_test_results(self, test_id: str) -> Optional[dict]:
        """Get results for an A/B test (placeholder - real implementation would aggregate from DB)."""
        test = self._ab_tests.get(test_id)
        if not test:
            return None

        return {
            "test": test.to_dict(),
            "note": "In production, this would aggregate actual results from database",
        }


# Global instance
prompt_manager = PromptManager()


def register_system_prompts() -> None:
    """Register built-in system prompts with version metadata."""
    from src.prompts import guided_teaching, conversation

    # Register guided teaching prompt
    guided_version = PromptVersion(
        prompt_id="guided_teaching",
        version="1.0.0",
        template=guided_teaching.PROMPT,
        description="Standard guided teaching prompt for TA interaction",
        created_at=datetime.utcnow(),
        author="system",
        status=PromptVersionStatus.ACTIVE,
        tags=["teaching", "guided", "core"],
        parameters={"max_tokens": 1000, "temperature": 0.7},
        change_notes="Initial version",
    )
    prompt_manager.register_version(guided_version)

    # Register conversation prompt
    conv_version = PromptVersion(
        prompt_id="conversation",
        version="1.0.0",
        template=conversation.PROMPT,
        description="Standard conversation prompt for TA interaction",
        created_at=datetime.utcnow(),
        author="system",
        status=PromptVersionStatus.ACTIVE,
        tags=["conversation", "general", "core"],
        parameters={"max_tokens": 500, "temperature": 0.8},
        change_notes="Initial version",
    )
    prompt_manager.register_version(conv_version)

    logger.info("Registered %d system prompts", 2)
