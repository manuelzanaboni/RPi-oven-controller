# RPi-oven-controller

This is a Python3 application that I'm developing to control a custom made oven. PyQt library has been used for GUI development.

The application will be deployed on a Raspberry Pi 4 and displayed on a touchscreen monitor.

## Getting Started

:man_technologist: WIP

### Requirements

* MAX6675 :man_technologist: WIP
* [Adafruit BMP python library](https://github.com/adafruit/Adafruit_Python_BMP). Used to control a BMP180 module. Follow link for installation guide.
* [PyQt5](https://pypi.org/project/PyQt5/) GUI development library. Precisely, version 5.13.2 has been used.

### Running the application

To run the application, simply navigate into root directory and execute:

```bash
python3 main.py
```

## Features

:man_technologist: WIP
<!-- ![](header.png) -->

## Folder structure

    .
    ├── components           # Auxiliary components (custom implementation of existing components)
    ├── controller           # Application logic files
    ├── resources            # Application resources
    ├── ui                   # Graphical user interface files
    ├── utils                # Declaration of variables (ready to import and  use)
    ├── main.py              # Application entry point
    ├── LICENSE
    └── README.md

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* [Monitor RPi temperature](https://github.com/Howchoo/pi-fan-controller)
