"""Host-side Python driver for the Blackpill HIL Testbench.

Owner: Seif (host layer).
"""
from .client import (
    Testbench,
    TestbenchError,
    TestbenchTimeout,
    TestbenchCommandError,
)

__all__ = [
    "Testbench",
    "TestbenchError",
    "TestbenchTimeout",
    "TestbenchCommandError",
]
__version__ = "0.1.0"
