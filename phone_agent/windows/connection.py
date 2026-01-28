"""Connection management for Windows (minimal implementation for API compatibility)."""

from dataclasses import dataclass
from enum import Enum


class ConnectionType(Enum):
    """Type of connection."""

    LOCAL = "local"


@dataclass
class DeviceInfo:
    """Device information."""

    device_id: str
    status: str
    connection_type: ConnectionType
    model: str | None = None


class WindowsConnection:
    """Windows connection manager (no actual connection needed)."""

    def connect(self, address: str) -> tuple[bool, str]:
        """Not applicable for Windows."""
        return False, "Windows doesn't support remote connections"

    def disconnect(self, address: str | None = None) -> tuple[bool, str]:
        """Not applicable for Windows."""
        return False, "Windows doesn't support remote connections"

    def enable_tcpip(
        self, port: int = 5555, device_id: str | None = None
    ) -> tuple[bool, str]:
        """Not applicable for Windows."""
        return False, "Windows doesn't support TCP/IP mode"

    def get_device_ip(self, device_id: str | None = None) -> str | None:
        """Not applicable for Windows."""
        return None


def list_devices() -> list[DeviceInfo]:
    """
    List Windows devices (always returns local machine).

    Returns:
        List with single local device.
    """
    import platform

    return [
        DeviceInfo(
            device_id="local",
            status="ready",
            connection_type=ConnectionType.LOCAL,
            model=platform.system() + " " + platform.release(),
        )
    ]
