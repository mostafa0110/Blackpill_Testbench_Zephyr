"""Minimal smoke check against a connected testbench.

Usage: python basic_usage.py /dev/ttyUSB0   (or COM3 on Windows)
"""
import sys
from blackpill_testbench import Testbench

def main(port: str) -> None:
    with Testbench(port) as tb:
        tb.set_gpio(1, True)
        print("tb_in_1 reads:", tb.get_gpio(1))
        tb.set_pwm(1, freq_hz=1000, duty_percent=50)
        print("tb_adc_1:", tb.read_adc(1), "mV")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0")
