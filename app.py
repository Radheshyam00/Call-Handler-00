import streamlit as st
import requests
import json
from datetime import datetime

# API Configuration
NUMLOOKUP_API_KEY = "your_api_key_here"
NUMLOOKUP_URL = "https://www.numlookupapi.com/api/v1/validate"

# Sample Lists
whitelist = {"+11234567890", "+911234567890"}
blacklist = {"+19876543210"}
blocked_list = {"+441234567890"}

# Initialize filter rules
if "filter_rules" not in st.session_state:
    st.session_state.filter_rules = []

def validate_number(mobile_number):
    """Check if a mobile number is valid using NumLookup API."""
    params = {"apikey": NUMLOOKUP_API_KEY, "number": mobile_number}
    response = requests.get(NUMLOOKUP_URL, params=params)
    data = response.json()
    
    if response.status_code != 200 or not data.get("valid"):
        return None  # Invalid number
    return data

def check_filters(data):
    """Apply filter rules to determine if a number should be allowed or blocked."""
    country = data.get("country_code")
    location = data.get("location")
    now = datetime.now().strftime("%H:%M")
    
    for rule in st.session_state.filter_rules:
        if country in rule.get("country", []) or location in rule.get("location", []):
            return False  # Blocked by country or location
        for time_range in rule.get("time", []):
            start, end = time_range.split("-")
            if start <= now <= end:
                return False  # Blocked by time
    
    return True

st.sidebar.title("📋 Navigation")
page = st.sidebar.radio("Go to", ["Number Checker", "Filter System"])

if page == "Number Checker":
    st.title("📱 Mobile Number Checker")
    mobile_number = st.text_input("Enter Mobile Number:")
    
    if st.button("Check Number"):
        if not mobile_number:
            st.error("Please enter a mobile number.")
        elif mobile_number in blacklist or mobile_number in blocked_list:
            st.error("❌ This number is in the blacklist or blocked list.")
        elif mobile_number in whitelist:
            st.success("✅ This number is whitelisted and allowed.")
        else:
            data = validate_number(mobile_number)
            if not data:
                st.error("❌ Invalid number.")
            elif not check_filters(data):
                st.error("🚫 Number blocked based on filter rules.")
            else:
                st.success("✅ Number allowed based on filter rules.")

elif page == "Filter System":
    st.title("⚙️ Filter System Rules")
    st.write("Manage filtering rules for incoming calls:")
    
    rule_name = st.text_input("Rule Name:")
    country_values = st.text_area("Enter Blocked Countries (comma-separated)")
    location_values = st.text_area("Enter Blocked Locations (comma-separated)")
    time_values = st.text_area("Enter Restricted Time Ranges (format: HH:MM-HH:MM, comma-separated)")
    
    if st.button("Add Rule"):
        new_rule = {
            "name": rule_name,
            "country": country_values.split(",") if country_values else [],
            "location": location_values.split(",") if location_values else [],
            "time": time_values.split(",") if time_values else []
        }
        st.session_state.filter_rules.append(new_rule)
        st.success("Rule added successfully!")
    
    st.write("### Current Rules")
    for rule in st.session_state.filter_rules:
        st.write(f"**Rule Name:** {rule['name']}")
        st.write(f"Blocked Countries: {', '.join(rule['country'])}")
        st.write(f"Blocked Locations: {', '.join(rule['location'])}")
        st.write(f"Restricted Time Ranges: {', '.join(rule['time'])}")
        st.write("---")
