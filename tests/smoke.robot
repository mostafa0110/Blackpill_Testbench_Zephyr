*** Settings ***
Documentation     Self-validation suite for the Blackpill testbench.
...               Requires a loopback harness (see tests/README.md).
Library           TestbenchLibrary.py
Suite Setup       Connect Testbench    ${PORT}
Suite Teardown    Disconnect Testbench

*** Variables ***
${PORT}           /dev/ttyUSB0

*** Test Cases ***
Digital Output Drives Looped Input
    [Documentation]    tb_out_1 wired to tb_in_1.
    Set Testbench Pin High    1
    Testbench Input Should Be    1    high
    Set Testbench Pin Low     1
    Testbench Input Should Be    1    low

PWM Channel Accepts Configuration
    Generate Testbench PWM    1    1000    50

ADC Reads Expected Reference
    [Documentation]    tb_adc_1 tied to a known divider (~1.65V).
    Verify Testbench ADC Voltage    1    1650    tolerance_mv=100
