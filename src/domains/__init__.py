"""Domain adapters: Python, Database, AI Literacy."""

from src.domains.base import DomainAdapter
from src.domains.python_domain.adapter import PythonDomainAdapter

__all__ = ["DomainAdapter", "PythonDomainAdapter"]
