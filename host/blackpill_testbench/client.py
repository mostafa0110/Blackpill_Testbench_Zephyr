"""pyserial driver that speaks the Zephyr Shell `tb` protocol.

See docs/Protocol_Spec.md for the wire format. This is a scaffold: the command
strings and response parsing are implemented; reconnect/retry hardening is
marked TODO for the host owner (Seif).
"""
from __future__ import annotations

import time

try:
    import serial  # pyserial
except ImportError as exc:  # pragma: no cover
    raise ImportError("pyserial is required: pip install pyserial") from exc


class TestbenchError(Exception):
    """Base class for all testbench errors."""


class TestbenchTimeout(TestbenchError):
    """Raised when the device does not respond within the timeout."""


class TestbenchCommandError(TestbenchError):
    """Raised when the device returns an ERROR: response."""


class Testbench:
    """High-level driver for the Blackpill testbench over a serial port.

    Example:
        with Testbench("/dev/ttyUSB0") as tb:
            tb.set_gpio(1, True)
            assert tb.get_gpio(1) is True
            tb.set_pwm(1, freq_hz=1000, duty_percent=50)
            mv = tb.read_adc(1)
    """

    PROMPT = "uart> "

    def __init__(self, port: str, baudrate: int = 115200,
                 timeout: float = 1.0, retries: int = 2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.retries = retries
        self._ser: "serial.Serial | None" = None

    # ----- lifecycle -----
    def open(self) -> "Testbench":
        self._ser = serial.Serial(
            self.port, self.baudrate, timeout=self.timeout,
            bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )
        time.sleep(0.1)
        self._ser.reset_input_buffer()
        return self

    def close(self) -> None:
        if self._ser and self._ser.is_open:
            self._ser.close()
        self._ser = None

    def __enter__(self) -> "Testbench":
        return self.open()

    def __exit__(self, *exc) -> None:
        self.close()

    # ----- transport -----
    def _send(self, command: str) -> str:
        """Send one command line and return the first meaningful response line.

        Raises TestbenchCommandError on 'ERROR:' and TestbenchTimeout on silence.
        TODO(host/Seif): add reconnect-on-drop and the retry loop using self.retries.
        """
        if not self._ser or not self._ser.is_open:
            raise TestbenchError("port not open; call open() or use a 'with' block")

        self._ser.reset_input_buffer()
        self._ser.write((command + "\r\n").encode("ascii"))
        self._ser.flush()

        deadline = time.time() + self.timeout
        while time.time() < deadline:
            raw = self._ser.readline().decode("ascii", errors="replace").strip()
            if not raw or raw == self.PROMPT or raw.endswith(command):
                continue  # skip echo / prompt / blank lines
            if raw.startswith("ERROR:"):
                raise TestbenchCommandError(raw)
            return raw
        raise TestbenchTimeout(f"no response to {command!r} within {self.timeout}s")

    # ----- protocol API -----
    def set_gpio(self, pin: int, state: bool) -> None:
        resp = self._send(f"tb gpio set tb_out_{pin} {1 if state else 0}")
        if resp != "OK":
            raise TestbenchCommandError(f"unexpected response: {resp!r}")

    def get_gpio(self, pin: int) -> bool:
        resp = self._send(f"tb gpio get tb_in_{pin}")  # -> "VAL: 1"
        return bool(int(resp.removeprefix("VAL:").strip()))

    def set_pwm(self, pin: int, freq_hz: int, duty_percent: int) -> None:
        resp = self._send(f"tb pwm set tb_pwm_{pin} {freq_hz} {duty_percent}")
        if resp != "OK":
            raise TestbenchCommandError(f"unexpected response: {resp!r}")

    def read_adc(self, pin: int) -> int:
        """Return the measured voltage in millivolts."""
        resp = self._send(f"tb adc read tb_adc_{pin}")  # -> "VAL: 1650 mV"
        return int(resp.removeprefix("VAL:").replace("mV", "").strip())
