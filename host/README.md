# Host Library (Python) — owner: Seif

`pyserial`-based driver that translates Python calls into the Zephyr Shell `tb`
protocol and parses the responses. See
[../docs/Protocol_Spec.md](../docs/Protocol_Spec.md).

## Install (editable)
```bash
cd host
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

## Use
```python
from blackpill_testbench import Testbench

with Testbench("/dev/ttyUSB0") as tb:   # COMx on Windows
    tb.set_gpio(1, True)            # tb gpio set tb_out_1 1
    state = tb.get_gpio(1)          # tb gpio get tb_in_1  -> bool
    tb.set_pwm(1, 1000, 50)         # tb pwm set tb_pwm_1 1000 50
    mv = tb.read_adc(1)             # tb adc read tb_adc_1 -> millivolts
```

## Status
Scaffold. Protocol methods + response parsing are implemented; reconnect-on-drop
and the retry loop are marked `TODO(host/Seif)` in `client.py`. See the GitHub
Issues board for the work breakdown.
