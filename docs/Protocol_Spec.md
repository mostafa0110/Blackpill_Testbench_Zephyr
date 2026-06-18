# Zephyr Shell Protocol Specification

This document details the command-line protocol used to communicate between the Host PC (via the Python Library) and the Blackpill Testbench. We utilize the native Zephyr Shell subsystem over UART.

## 📡 Serial Configuration
- **Baudrate**: 115200
- **Data Bits**: 8
- **Parity**: None
- **Stop Bits**: 1
- **Flow Control**: None
- **Line Ending**: `\r\n` (CRLF)

## 💬 Command Structure

The Zephyr shell uses a hierarchical command structure. We implement a custom root command named `tb` (Testbench) to keep all our commands organized.

### Syntax
```
tb <subsystem> <action> <target> [arguments...]
```

## 🔌 GPIO Commands

### Set Digital Output
Sets a specific digital output pin to HIGH (1) or LOW (0).

**Command:** `tb gpio set <pin_alias> <state>`
- `<pin_alias>`: E.g., `tb_out_1`, `tb_out_2`.
- `<state>`: `1` for HIGH, `0` for LOW.

```
uart> tb gpio set tb_out_1 1
OK
```

### Get Digital Input
Reads the current logical state of a specific digital input pin.

**Command:** `tb gpio get <pin_alias>`
- `<pin_alias>`: E.g., `tb_in_1`, `tb_in_2`.

```
uart> tb gpio get tb_in_1
VAL: 1
```

## 🎛️ PWM Commands

### Set PWM Output
Configures and starts a PWM signal on a specific pin.

**Command:** `tb pwm set <pin_alias> <frequency_hz> <duty_cycle_percent>`
- `<pin_alias>`: E.g., `tb_pwm_1`.
- `<frequency_hz>`: Frequency in Hertz (e.g., `1000` for 1kHz).
- `<duty_cycle_percent>`: Duty cycle from `0` to `100`.

```
uart> tb pwm set tb_pwm_1 1000 50
OK
```

## ⚡ ADC Commands

### Read Analog Voltage
Reads the analog voltage present on a specific ADC pin.

**Command:** `tb adc read <pin_alias>`
- `<pin_alias>`: E.g., `tb_adc_1`.

```
uart> tb adc read tb_adc_1
VAL: 1650 mV
```

## 🛡️ Error Handling
If an invalid command, invalid argument, or hardware error occurs, the Zephyr shell responds with an error message starting with `ERROR:`. The Host Python script must parse these strings to raise exceptions.

```
uart> tb gpio set invalid_pin 1
ERROR: Pin alias not found.
```
