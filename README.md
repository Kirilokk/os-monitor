# OS Monitor

A simple system monitoring dashboard built with Streamlit.

The application displays real-time system metrics including:
- `CPU usage` 
- `GPU statistics`
- `Memory consumption`
- `Storage information`
- `Hardware sensors`  

Metrics collection is implemented as reusable services shared between a Streamlit UI and a FastAPI API.

## Screenshots

### Main dashboard + CPU

![Dashboard](docs/dashboard.png)

### GPU

![GPU](docs/gpu.png)

### Memory

![Memory](docs/memory.png)

### Sensors
![Sensors](docs/sensors.png)


## Features

- Real-time CPU monitoring
- GPU monitoring (AMD GPUs)
- Memory and storage statistics
- Hardware sensor data
- Streamlit dashboard UI
- FastAPI endpoints for retrieving metrics
- Shared service layer used by both UI and API

## Tech Stack

- Python
- Streamlit
- FastAPI
- psutil
- pyamdgpuinfo


## Limitations

Currently the application supports:

- Linux only
- AMD GPUs only

GPU metrics rely on `pyamdgpuinfo`, which is not available on Windows and does not support NVIDIA GPUs.


## Setup
#### To set up and run this application, follow these steps:
1. Clone this repository to your local machine.
2. Install the required dependencies by running: `uv sync`.
3. Start the service using `streamlit run app.py`