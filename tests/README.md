# Test Suite (Robot Framework) — owner: Seif

Custom Robot Framework library that wraps the host driver into readable keywords,
plus a self-validation suite that exercises the testbench against a loopback harness.

## Install & run
```bash
pip install robotframework
# from the repo root, with the host package installed (pip install -e host)
robot --variable PORT:/dev/ttyUSB0 tests/smoke.robot
```

## Loopback harness
The smoke suite assumes a self-test wiring so the board can validate itself:
- `tb_out_1` (PA4) → `tb_in_1` (PB12)
- A known resistor divider (~1.65 V) → `tb_adc_1` (PA0)

## Keywords
`Connect Testbench`, `Disconnect Testbench`, `Set Testbench Pin High/Low`,
`Testbench Input Should Be`, `Generate Testbench PWM`, `Verify Testbench ADC Voltage`.
