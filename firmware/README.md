# Firmware (Zephyr RTOS) — owner: Mostafa

Zephyr application that turns the STM32F401 Blackpill into the testbench. Exposes
hardware control through the Zephyr Shell `tb` command tree (see
[../docs/Protocol_Spec.md](../docs/Protocol_Spec.md)).

## Layout
| File | Purpose |
|---|---|
| `prj.conf` | Enables Shell, UART, GPIO, PWM, ADC |
| `app.overlay` | Maps physical pins to logical aliases (`tb_out_1` …) via the `zephyr,user` node |
| `src/main.c` | Boot + readiness log |
| `src/tb_shell.c` | `tb gpio/pwm/adc` shell command handlers |

## Build & flash
```bash
# One-time: west workspace with Zephyr + STM32 HAL
west init -m https://github.com/zephyrproject-rtos/zephyr --mr main zephyr-ws
cd zephyr-ws && west update && west zephyr-export

# Build for your Blackpill variant (f401cc = 256K, f401ce = 512K)
west build -b blackpill_f401ce path/to/blackpill-testbench/firmware

# Flash (DFU over USB, or ST-Link)
west flash
```

## Status
Scaffold. Handlers validate arguments and emit the protocol responses
(`OK` / `VAL:` / `ERROR:`); the actual GPIO/PWM/ADC driver calls are marked
`TODO(firmware/Mostafa)`. See the GitHub Issues board for the work breakdown.
