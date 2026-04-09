"""M-63: Port configuration alignment check and validation."""

import logging
import os
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class PortConfig:
    """Unified port configuration for all services."""

    backend_port: int = 8000
    frontend_dev_port: int = 5173
    frontend_prod_port: int = 3000
    db_port: int = 5432

    @classmethod
    def from_env(cls) -> "PortConfig":
        """Load configuration from environment variables."""
        return cls(
            backend_port=int(os.environ.get("BACKEND_PORT", "8000")),
            frontend_dev_port=int(os.environ.get("FRONTEND_DEV_PORT", "5173")),
            frontend_prod_port=int(os.environ.get("FRONTEND_PROD_PORT", "3000")),
            db_port=int(os.environ.get("DB_PORT", "5432")),
        )

    def validate(self) -> dict:
        """Validate port configuration for conflicts."""
        issues = []
        warnings_list = []

        ports = {
            "backend": self.backend_port,
            "frontend_dev": self.frontend_dev_port,
            "frontend_prod": self.frontend_prod_port,
            "database": self.db_port,
        }

        # Check for duplicate ports
        seen_ports = {}
        for service, port in ports.items():
            if port in seen_ports:
                issues.append(
                    f"Port conflict: {service} and {seen_ports[port]} both use port {port}"
                )
            else:
                seen_ports[port] = service

        # Check for privileged ports (< 1024)
        for service, port in ports.items():
            if port < 1024:
                warnings_list.append(
                    f"{service} uses privileged port {port} (requires admin/root)"
                )

        # Check for commonly conflicting ports
        common_ports = [80, 443, 22, 21, 23, 25, 3306, 6379, 27017]
        for service, port in ports.items():
            if port in common_ports:
                warnings_list.append(
                    f"{service} uses common service port {port} - may conflict with other services"
                )

        # Check port ranges
        for service, port in ports.items():
            if port < 1 or port > 65535:
                issues.append(f"{service} port {port} is out of valid range (1-65535)")

        # Check for Docker compatibility (common ranges)
        if self.backend_port >= 49152:
            warnings_list.append(
                f"Backend port {self.backend_port} is in dynamic/private range - may cause Docker issues"
            )

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings_list,
            "ports": ports,
        }

    def get_cors_origins(self, environment: str = "development") -> list[str]:
        """Generate CORS origins based on configuration."""
        origins = []

        if environment == "development":
            origins.extend([
                f"http://localhost:{self.frontend_dev_port}",
                f"http://127.0.0.1:{self.frontend_dev_port}",
            ])
        else:
            origins.extend([
                f"http://localhost:{self.frontend_prod_port}",
                f"http://127.0.0.1:{self.frontend_prod_port}",
            ])

        # Add additional origins from environment
        additional = os.environ.get("CORS_ADDITIONAL_ORIGINS", "")
        if additional:
            origins.extend([o.strip() for o in additional.split(",") if o.strip()])

        return origins

    def to_dict(self) -> dict:
        """Return configuration as dictionary."""
        return {
            "backend_port": self.backend_port,
            "frontend_dev_port": self.frontend_dev_port,
            "frontend_prod_port": self.frontend_prod_port,
            "db_port": self.db_port,
            "validation": self.validate(),
        }


def check_port_availability(port: int) -> bool:
    """Check if a port is available for use."""
    import socket

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", port))
            return True
    except OSError:
        return False


def validate_environment_ports() -> dict:
    """Comprehensive port validation for the current environment."""
    config = PortConfig.from_env()
    validation = config.validate()

    # Check port availability
    availability = {}
    for service, port in validation["ports"].items():
        availability[service] = {
            "port": port,
            "available": check_port_availability(port),
        }

    validation["availability"] = availability

    # Log results
    if not validation["valid"]:
        for issue in validation["issues"]:
            logger.error("Port configuration issue: %s", issue)

    if validation["warnings"]:
        for warning in validation["warnings"]:
            logger.warning("Port configuration warning: %s", warning)

    for service, avail in availability.items():
        if not avail["available"]:
            logger.warning("Port %d for %s is already in use", avail["port"], service)

    return validation


# Global configuration instance
port_config = PortConfig.from_env()
