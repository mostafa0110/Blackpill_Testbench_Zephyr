# Project Tasks — Work Breakdown

Split **by layer**: **Mostafa** owns firmware, **Seif** owns host + tests, the
protocol spec and integration are **shared**. This file mirrors the GitHub
**Issues** board (3 phase milestones). Check items off here or track on Issues.

Labels used on GitHub: `firmware`, `host`, `tests`, `shared`, `owner:mostafa`, `owner:seif`.

## Phase 1 — Foundation (Week 1)
| # | Task | Layer | Owner |
|---|------|-------|-------|
| 1 | Set up Zephyr/west workspace and build a hello-world for `blackpill_f401ce` | firmware | Mostafa |
| 2 | Configure USART2 + enable Zephyr Shell over UART (115200 8N1), confirm `tb` prompt | firmware | Mostafa |
| 3 | Establish `pyserial` connection + base send/parse loop (echo/prompt handling) | host | Seif |
| 4 | Finalize protocol v1 (command tree, `OK`/`VAL:`/`ERROR:` format) | shared | Both |

## Phase 2 — Hardware Control (Week 2)
| # | Task | Layer | Owner |
|---|------|-------|-------|
| 5 | Create `app.overlay` devicetree aliases (`tb_out_1..4`, `tb_in_1..4`, `tb_pwm_1..2`, `tb_adc_1..2`) | firmware | Mostafa |
| 6 | Implement `tb gpio set` / `tb gpio get` against the GPIO driver | firmware | Mostafa |
| 7 | Implement `tb pwm set` (freq + duty → period/pulse) | firmware | Mostafa |
| 8 | Implement `tb adc read` (raw → millivolts) | firmware | Mostafa |
| 9 | Implement Python API: `set_gpio` / `get_gpio` / `set_pwm` / `read_adc` + response parsing + exceptions | host | Seif |
| 10 | Add reliability: timeouts, retries, reconnect on UART drop | host | Seif |

## Phase 3 — Automation Integration (Week 3)
| # | Task | Layer | Owner |
|---|------|-------|-------|
| 11 | Build Robot Framework library wrapping the Python API | tests | Seif |
| 12 | Author high-level keywords (`Set Testbench Pin High`, `Verify Testbench ADC Voltage`, …) | tests | Seif |
| 13 | Write self-validation suite using a loopback harness | tests | Seif |
| 14 | Integration pass + documentation wrap-up + README finalize | shared | Both |
