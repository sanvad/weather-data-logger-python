# Weather Data Logger

A Python application for simulating, storing, and analyzing meteorological measurements.

## Features

- Generates 24 simulated weather records.
- Stores data in a binary file using Python's `struct` module.
- Reads and validates binary records.
- Calculates average, maximum, and minimum values for temperature, humidity, and wind speed.
- Generates a daily text report.

## Technologies

- Python 3
- `struct`
- Binary file handling
- `random`

## How to Run

Make sure Python 3 is installed, then run:

```bash
python meteorologia.py
```

The application generates `datos_meteorologicos.bin` and `reporte_diario.txt` in the working directory.

## Project Purpose

Personal programming project focused on binary file handling, data validation, and report generation.
