# epibox

This package is complementary to the mobile app EpiBOX (available at [EpiBOX-app](https://github.com/anascacais/epibox_app)).

Designed for use with Raspberry Pi, it acts as an autonomous recording unit - allowing for sensor connectivity and data storage. EpiBOX mobile app provides the user interaface and the near-real time visualization of the data. 

Currently, EpiBOX supports BITalino-based equipments allowing for the recording, storage and visualization of up to 12 channels simmultaneously. Nevertheless, this package can be easily integrated with other sensors, as long as a python API is provided!

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install epibox.

```bash
pip install epibox
or 
pip install --upgrade epibox
```

## Usage

```python
from epibox import mqtt_startup

# this will initiate the process - which should be continued by the user interface (EpiBOX)
mqtt_startup.main() 
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Contact
For any additional information please contact me: anascacais@gmail.com
