import streamlit as st
import requests
import json
from datetime import datetime

# API Configuration
NUMLOOKUP_API_KEY = "num_live_zo8k5QYZZ7zjPiqBMhI0s0K4B5TtMMgtbeqBzJgM"
NUMLOOKUP_URL = "https://www.numlookupapi.com/api/validate"

# Sample Lists
whitelist = {"+11234567890", "+911234567890"}
blacklist = {"+19876543210"}
blocked_list = {"+441234567890"}

# Initialize filter rules
if "filter_rules" not in st.session_state:
    st.session_state.filter_rules = []

def validate_number(mobile_number):
    """Check if a mobile number is valid using NumLookup API."""
    url = f"{NUMLOOKUP_URL}/{mobile_number}?apikey={NUMLOOKUP_API_KEY}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if not data.get("valid"):
            return None  # Invalid number
        return data
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def check_filters(data):
    """Apply filter rules to determine if a number should be allowed or blocked."""
    country = data.get("country_code", "")
    location = data.get("location", "")
    now = datetime.now().time()

    for rule in st.session_state.filter_rules:
        if country in rule.get("country", []) or location in rule.get("location", []):
            return False  # Blocked by country or location

        for time_range in rule.get("time", []):
            try:
                start, end = [datetime.strptime(t.strip(), "%H:%M").time() for t in time_range.split("-")]
                if start <= now <= end:
                    return False  # Blocked by time
            except ValueError:
                continue  # Ignore invalid time format

    return True

st.sidebar.title("📋 Navigation")
page = st.sidebar.radio("Go to", ["Number Checker", "Filter System"])

if page == "Number Checker":
    st.title("📱 Mobile Number Checker")
    mobile_number = st.text_input("Enter Mobile Number:").strip()
    
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
                st.error("❌ Invalid number or API failure.")
            elif not check_filters(data):
                st.error("🚫 Number blocked based on filter rules.")
            else:
                st.success("✅ Number allowed based on filter rules.")

elif page == "Filter System":
    st.title("⚙️ Filter System Rules")
    st.write("Manage filtering rules for incoming calls:")
    
    rule_name = st.text_input("Rule Name:").strip()
    country_values = st.text_area("Enter Blocked Countries (comma-separated)").strip()
    location_values = st.text_area("Enter Blocked Locations (comma-separated)").strip()
    time_values = st.text_area("Enter Restricted Time Ranges (HH:MM-HH:MM, comma-separated)").strip()
    
    if st.button("Add Rule"):
        if rule_name:
            new_rule = {
                "name": rule_name,
                "country": [c.strip() for c in country_values.split(",") if c.strip()],
                "location": [l.strip() for l in location_values.split(",") if l.strip()],
                "time": [t.strip() for t in time_values.split(",") if t.strip()]
            }
            st.session_state.filter_rules.append(new_rule)
            st.success(f"Rule '{rule_name}' added successfully!")
        else:
            st.error("Please provide a valid rule name.")

    st.write("### Current Rules")
    with st.expander("View Current Rules", expanded=False):
        if not st.session_state.filter_rules:
            st.write("No rules added yet.")
        else:
            for rule in st.session_state.filter_rules:
                st.markdown(f"**📌 Rule Name:** {rule['name']}")
                st.write(f"🔴 **Blocked Countries:** {', '.join(rule['country']) or 'None'}")
                st.write(f"📍 **Blocked Locations:** {', '.join(rule['location']) or 'None'}")
                st.write(f"⏳ **Restricted Time Ranges:** {', '.join(rule['time']) or 'None'}")
                st.markdown("---")
