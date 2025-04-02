# Python Project

## Project Overview

This Python project utilizes `MongoDB` for data storage and the `NumLookup API` for phone number validation. The core functionality is implemented in `call.py`, and the project dependencies are listed in `requirements.txt`.

## Features

- Integration with **MongoDB** for data management.
- Utilization of **NumLookup API** for phone number verification.
- Modular and scalable Python script (`call.py`).

## Prerequisites

Ensure you have the following installed before running the project:

- Python (>= 3.x)
- MongoDB
- An active NumLookup API key

## Installation

```sh
# Clone the repository
git clone https://github.com/Radheshyam00/Call-Handler-00.git
cd Call-Handler-00

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Configuration

```python
# Set up MongoDB and update the connection URI in call.py
MONGO_URI = "mongodb://localhost:27017/your_database"
```

```sh
# Set your NumLookup API Key as an environment variable
export NUMLOOKUP_API_KEY="your_api_key"
```

```python
# Or update call.py with your API key
API_KEY = "your_api_key"
```

## Usage

```sh
streamlit run call.py
```

## File Structure

```
project-folder/
│── call.py             # Main script
│── requirements.txt    # Required dependencies
│── README.md           # Documentation
```

## Dependencies

```txt
pymongo  # MongoDB driver for Python
requests  # For making API requests
streamlit # For making UI
datetime # For timestamp
```

## License

This project is licensed under the MIT License.

