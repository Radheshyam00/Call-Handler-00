# Call-Handler-00
This Python project utilizes MongoDB for data storage and the NumLookup API for phone number validation. The core functionality is implemented in call.py, and the project dependencies are listed in requirements.txt.

## Features

1. Integration with MongoDB for data management.

2. Utilization of NumLookup API for phone number verification.

3. Modular and scalable Python script (call.py).

## Prerequisites

Ensure you have the following installed before running the project:

1. Python (>= 3.x)

2. MongoDB

3. An active NumLookup API key

## Installation

# Clone the repository
git clone <repository-url>
cd <repository-folder>

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r requirements.txt

## Configuration

# Set up MongoDB and update the connection URI in call.py
MONGO_URI = "mongodb://localhost:27017/your_database"

# Set your NumLookup API Key as an environment variable
export NUMLOOKUP_API_KEY="your_api_key"

# Or update call.py with your API key
API_KEY = "your_api_key"

## Usage

python call.py

## File Structure

project-folder/
│── call.py             # Main script
│── requirements.txt    # Required dependencies
│── README.md           # Documentation

## Dependencies

pymongo  # MongoDB driver for Python
requests  # For making API requests