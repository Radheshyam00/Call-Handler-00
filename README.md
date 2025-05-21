# Python Project

## Project Overview
### Without GSM module
This Python project utilizes `MongoDB` for data storage and the `NumLookup API` for phone number validation. The core functionality is implemented in `call.py`, and the project dependencies are listed in `requirements.txt`.

### With GSM module
This project uses an Arduino with a `GSM module (SIM800L/SIM900)` to implement mobile number blacklisting and integrates with a public `NumLookup API` for caller identification. The system can automatically reject calls from blacklisted numbers and optionally log or display information about callers via the API.

## Features
### Without GSM module
- Integration with **MongoDB** for data management.
- Utilization of **NumLookup API** for phone number verification.
- Modular and scalable Python script (`call.py`).

### With GSM module
- **Blacklist Support:** Automatically reject calls from blacklisted numbers.
- **Number Lookup API:** Integrates with a public API to fetch caller details (e.g., location, carrier).
- **GSM Module Integration:** Uses GSM module (e.g., SIM800L) for call handling.
- **Serial Output Logging:** Displays debug and API response on Serial Monitor.
- Works on SMS and/or Call Triggers (based on implementation).

## Prerequisites
### Without GSM module
Ensure you have the following installed before running the project:

- Python (>= 3.x)
- MongoDB
- An active NumLookup API key

### With GSM module
#### Hardware Requirements

- Arduino Uno / Mega / Nano
- SIM800L or SIM900 GSM Module
- SIM Card with balance/data
- Jumper wires
- Optional: LCD for output display

##### Software Requirements

- Arduino IDE
- Libraries:
  SoftwareSerial.h

## File Descriptions
`sketch_blacklisting_mobile-numbers.ino`
- Maintains a list of blacklisted numbers.
- Reads incoming call details.
- Compares caller ID with the blacklist.
- Rejects the call if it matches.

`sketch_numlookup-api_integration.ino`
- Sends HTTP requests to a Number Lookup API (e.g., Numverify, NumlookupAPI).
- Parses and displays information such as country, carrier, and type.
- Could be triggered via SMS or button.

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

