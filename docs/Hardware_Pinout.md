# Hardware Pinout & Wiring

This document defines the default pin mapping for the STM32F401 Blackpill when used as the Testbench. The Host PC communicates with the Blackpill using a USB-to-TTL Serial adapter.

## 🔌 Host Connection (UART via USB-to-TTL)

We use `USART2` on the Blackpill for the Zephyr Shell. Connect your USB-to-TTL adapter as follows:

| Blackpill Pin | STM32 Function | USB-to-TTL Adapter |
| ------------- | -------------- | ------------------ |
| `PA2`         | `USART2_TX`    | `RX`               |
| `PA3`         | `USART2_RX`    | `TX`               |
| `GND`         | `Ground`       | `GND`              |

> [!WARNING]
> Ensure your USB-to-TTL adapter is operating at 3.3V logic levels to avoid damaging the STM32F401.

## 📌 Dedicated Testbench Pins

These pins will be aliased in the Zephyr Devicetree (`app.overlay`) so the firmware and host software can refer to them logically (e.g., `tb_out_1` instead of `PA4`).

### Digital Outputs (Testbench -> DUT)

| Logical Name | Blackpill Pin | Notes               |
| ------------ | ------------- | ------------------- |
| `tb_out_1`   | `PA4`         | General Purpose Out |
| `tb_out_2`   | `PA5`         | General Purpose Out |
| `tb_out_3`   | `PA6`         | General Purpose Out |
| `tb_out_4`   | `PA7`         | General Purpose Out |

### Digital Inputs (DUT -> Testbench)

| Logical Name | Blackpill Pin | Notes              |
| ------------ | ------------- | ------------------ |
| `tb_in_1`    | `PB12`        | General Purpose In |
| `tb_in_2`    | `PB13`        | General Purpose In |
| `tb_in_3`    | `PB14`        | General Purpose In |
| `tb_in_4`    | `PB15`        | General Purpose In |

### PWM Outputs (Testbench -> DUT)

| Logical Name | Blackpill Pin | STM32 Timer | Notes               |
| ------------ | ------------- | ----------- | ------------------- |
| `tb_pwm_1`   | `PA8`         | `TIM1_CH1`  | High-Frequency PWM  |
| `tb_pwm_2`   | `PA9`         | `TIM1_CH2`  | High-Frequency PWM  |

### Analog Inputs (DUT -> Testbench)

| Logical Name | Blackpill Pin | STM32 ADC Channel | Notes                |
| ------------ | ------------- | ----------------- | -------------------- |
| `tb_adc_1`   | `PA0`         | `ADC1_IN0`        | 0-3.3V Range, 12-bit |
| `tb_adc_2`   | `PA1`         | `ADC1_IN1`        | 0-3.3V Range, 12-bit |
