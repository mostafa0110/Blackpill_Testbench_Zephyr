# Testbench Requirements

## 🎯 Goal
Build a Hardware-in-the-Loop (HIL) testbench using an STM32F401 Blackpill board running Zephyr RTOS. The testbench acts as an I/O simulator and measurement device to automate testing of other embedded devices.

## 📋 System Requirements

### 1. Hardware
- **Core Board**: STM32F401 "Blackpill".
- **Host Connection**: USB-to-TTL Serial Adapter connecting the Host PC to the Blackpill's UART interface.
- **Interfaces**:
  - Minimum 4 Dedicated Digital Inputs.
  - Minimum 4 Dedicated Digital Outputs.
  - Minimum 2 PWM Outputs.
  - Minimum 2 Analog (ADC) Inputs.
  - *Future Extensibility*: I2C, SPI, and CAN (via external transceiver).

### 2. Firmware (Zephyr RTOS)
- **Communication**: Use the built-in **Zephyr Shell** subsystem over UART for receiving commands and sending responses.
- **Execution**: Hardware commands (GPIO toggling, ADC reading) must be executed with minimal RTOS delay.
- **Modularity**: The firmware must use Devicetree overlays to abstract the physical pins into logical testbench endpoints (e.g., `tb_out_1`).

### 3. Host Software (Python)
- **Library**: A custom Python package using `pyserial`.
- **API**: Provide a clean API to interact with the Zephyr Shell (e.g., sending `gpio set tb_out_1 1` and parsing the response).
- **Reliability**: Must handle UART connection drops, timeouts, and command retries.

### 4. Test Framework (Robot Framework)
- **Integration**: A Custom Robot Library that wraps the Python API.
- **Keywords**: Expose high-level keywords like `Set Testbench Pin High`, `Verify Testbench ADC Voltage`.

## 📈 Use Cases

### UC1: Digital I/O Validation
- The Host requests the testbench to set a specific output pin to high/low to simulate a sensor trigger.
- The Host requests the testbench to read an input pin to verify the DUT's output response.

### UC2: PWM Simulation
- The Host configures the testbench to generate a PWM signal (frequency and duty cycle) to simulate a motor encoder or analog sensor.

### UC3: Analog Measurement
- The Host commands the testbench to read an ADC channel to verify the analog voltage output of the DUT.

## 📅 Timeline

### Phase 1: Foundation (Week 1)
- Setup Zephyr workspace for the Blackpill board.
- Configure UART and the Zephyr Shell subsystem.
- Establish Python `pyserial` connection and basic command parsing.

### Phase 2: Hardware Control (Week 2)
- Create `app.overlay` for devicetree pin aliases.
- Implement GPIO set/get commands.
- Implement PWM generation commands.
- Implement ADC reading commands.

### Phase 3: Automation Integration (Week 3)
- Develop the custom Robot Framework Python library.
- Write initial Robot test cases to validate the testbench itself.
- Documentation and final wrap-up.
