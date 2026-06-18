# 🚀 STM32F401 Blackpill Testbench

A **Hardware-in-the-Loop (HIL) testbench** built on the STM32F401 "Blackpill"
running **Zephyr RTOS**. It acts as an I/O simulator and measurement device to
automate testing of other embedded devices using **Python** and **Robot Framework**.

The host PC sends text commands over UART to the board's **Zephyr Shell**; the
board drives/reads GPIO, PWM, and ADC pins wired to the Device Under Test (DUT).

## 🧱 Architecture (three layers)

```
Robot Framework  ──►  Python driver (pyserial)  ──►  USB-TTL  ──►  Zephyr Shell ──► GPIO / PWM / ADC ──► DUT
   tests/                   host/                                      firmware/
```

| Layer | Folder | Owner |
|---|---|---|
| Real-time hardware (Zephyr RTOS firmware) | [`firmware/`](firmware/) | **Mostafa** |
| Host communication (Python `pyserial` driver) | [`host/`](host/) | **Seif** |
| Test automation (Robot Framework library + suites) | [`tests/`](tests/) | **Seif** |
| Protocol spec + integration | [`docs/`](docs/) | **Shared** |

## 📁 Repository layout

```
blackpill-testbench/
├── docs/         # Requirements, Architecture, Hardware Pinout, Protocol Spec
├── firmware/     # Zephyr application (Shell `tb` command tree, devicetree overlay)
├── host/         # Python package: blackpill_testbench driver + examples
├── tests/        # Robot Framework keyword library + self-validation suite
└── PROJECT_TASKS.md  # Work breakdown (mirrors the GitHub Issues board)
```

## 📚 Documentation
- [Requirements](docs/Requirements.md) — goal, hardware/software requirements, use cases, timeline
- [Architecture](docs/Architecture.md) — three-layer design and ownership
- [Hardware Pinout](docs/Hardware_Pinout.md) — wiring and logical pin aliases
- [Protocol Spec](docs/Protocol_Spec.md) — the `tb` Zephyr Shell command protocol

## ⚡ Quick reference (protocol)

| Action | Command | Response |
|---|---|---|
| Set output high | `tb gpio set tb_out_1 1` | `OK` |
| Read input | `tb gpio get tb_in_1` | `VAL: 1` |
| Start PWM | `tb pwm set tb_pwm_1 1000 50` | `OK` |
| Read ADC | `tb adc read tb_adc_1` | `VAL: 1650 mV` |

## 🏁 Getting started
1. **Firmware** — flash the Blackpill: see [firmware/README.md](firmware/README.md).
2. **Host** — `pip install -e host`, then drive it from Python: see [host/README.md](host/README.md).
3. **Tests** — `robot --variable PORT:/dev/ttyUSB0 tests/smoke.robot`: see [tests/README.md](tests/README.md).

## 👥 Team & tasks
Work is split by layer — Mostafa owns firmware, Seif owns host + tests, the
protocol and integration are shared. The full breakdown lives in
[PROJECT_TASKS.md](PROJECT_TASKS.md) and on the repo's **Issues** board
(grouped into three phase milestones).

## 📅 Phases
1. **Foundation** — Zephyr workspace, UART + Shell, pyserial connection.
2. **Hardware Control** — devicetree overlay, GPIO/PWM/ADC commands, Python API.
3. **Automation Integration** — Robot library, keywords, self-validation suite.
