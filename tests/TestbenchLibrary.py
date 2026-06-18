"""Robot Framework keyword library wrapping the host Testbench driver.

Owner: Seif (test layer). Method names map to Robot keywords, e.g.
`set_testbench_pin_high` -> "Set Testbench Pin High".
"""
from __future__ import annotations

from robot.api.deco import keyword, library
from blackpill_testbench import Testbench


@library(scope="SUITE")
class TestbenchLibrary:
    def __init__(self):
        self._tb: Testbench | None = None

    @keyword("Connect Testbench")
    def connect_testbench(self, port: str, baudrate: int = 115200):
        self._tb = Testbench(port, baudrate=int(baudrate)).open()

    @keyword("Disconnect Testbench")
    def disconnect_testbench(self):
        if self._tb:
            self._tb.close()
            self._tb = None

    @keyword("Set Testbench Pin High")
    def set_testbench_pin_high(self, pin: int):
        self._require().set_gpio(int(pin), True)

    @keyword("Set Testbench Pin Low")
    def set_testbench_pin_low(self, pin: int):
        self._require().set_gpio(int(pin), False)

    @keyword("Testbench Input Should Be")
    def testbench_input_should_be(self, pin: int, expected: bool):
        actual = self._require().get_gpio(int(pin))
        expected = str(expected).lower() in ("1", "true", "high", "yes")
        if actual != expected:
            raise AssertionError(f"tb_in_{pin}: expected {expected}, got {actual}")

    @keyword("Generate Testbench PWM")
    def generate_testbench_pwm(self, pin: int, freq_hz: int, duty_percent: int):
        self._require().set_pwm(int(pin), int(freq_hz), int(duty_percent))

    @keyword("Verify Testbench ADC Voltage")
    def verify_testbench_adc_voltage(self, pin: int, expected_mv: int, tolerance_mv: int = 50):
        actual = self._require().read_adc(int(pin))
        if abs(actual - int(expected_mv)) > int(tolerance_mv):
            raise AssertionError(
                f"tb_adc_{pin}: {actual} mV not within {tolerance_mv} mV of {expected_mv} mV")

    def _require(self) -> Testbench:
        if not self._tb:
            raise RuntimeError("Call 'Connect Testbench' first.")
        return self._tb
