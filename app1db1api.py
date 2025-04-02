import streamlit as st
import requests
import pymongo
from datetime import datetime

# MongoDB Configuration (Replace with your MongoDB URI)
MONGO_URI = "mongodb+srv://radheshyamjanwa666:TPo5T91ldKNiWWCM@cluster0.bdfxa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "call_filter_db"
FILTER_COLLECTION = "filter_rules"
LISTS_COLLECTION = "phone_lists"
API_HISTORY_COLLECTION = "api_history"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
rules_collection = db[FILTER_COLLECTION]
lists_collection = db[LISTS_COLLECTION]
api_history_collection = db[API_HISTORY_COLLECTION]

# API Configuration
NUMLOOKUP_API_KEY = "num_live_zo8k5QYZZ7zjPiqBMhI0s0K4B5TtMMgtbeqBzJgM"

def validate_number(mobile_number):
    """Check if a mobile number is valid using NumLookup API and store result in MongoDB."""
    url = f"https://www.numlookupapi.com/api/validate/{mobile_number}?apikey={NUMLOOKUP_API_KEY}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("valid"):
            return None  # Invalid number
        
        # Store API response in MongoDB
        api_history_collection.insert_one({
            "number": mobile_number,
            "response": data,
            "timestamp": datetime.now()
        })
        
        return data
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

def get_api_history():
    """Retrieve stored API call data from MongoDB."""
    return list(api_history_collection.find({}, {"_id": 0}))

def get_phone_list(list_name):
    """Retrieve phone numbers from MongoDB list (whitelist, blacklist, blocked)."""
    result = lists_collection.find_one({"list_name": list_name})
    return set(result["numbers"]) if result else set()

def update_phone_list(list_name, phone_number, action="add"):
    """Add or remove a phone number from a specified list (whitelist, blacklist, blocked)."""
    if action == "add":
        lists_collection.update_one(
            {"list_name": list_name},
            {"$addToSet": {"numbers": phone_number}},
            upsert=True
        )
    elif action == "remove":
        lists_collection.update_one(
            {"list_name": list_name},
            {"$pull": {"numbers": phone_number}}
        )

def get_all_filter_rules():
    """Retrieve all filter rules from MongoDB."""
    return list(rules_collection.find({}, {"_id": 0}))

def add_filter_rule(rule):
    """Insert a new filter rule into MongoDB."""
    rules_collection.insert_one(rule)

def check_filters(data):
    """Apply filter rules from MongoDB to determine if a number should be allowed or blocked."""
    country = data.get("country_code", "")
    location = data.get("location", "")
    now = datetime.now().time()
    
    filter_rules = get_all_filter_rules()

    for rule in filter_rules:
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
page = st.sidebar.radio("Go to", ["Number Checker", "Filter System", "Manage Lists", "API Data List"])

if page == "Number Checker":
    st.title("📱 Mobile Number Checker")
    mobile_number = st.text_input("Enter Mobile Number:").strip()

    if st.button("Check Number"):
        whitelist = get_phone_list("whitelist")
        blacklist = get_phone_list("blacklist")
        blocked_list = get_phone_list("blocked")

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
                st.json(data)

elif page == "Filter System":
    st.title("⚙️ Filter System Rules")
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
            add_filter_rule(new_rule)
            st.success(f"Rule '{rule_name}' added successfully!")
        else:
            st.error("Please provide a valid rule name.")

    st.write("### Current Rules")
    with st.expander("View Current Rules", expanded=False):
        filter_rules = get_all_filter_rules()
        if not filter_rules:
            st.write("No rules added yet.")
        else:
            for rule in filter_rules:
                st.markdown(f"**📌 Rule Name:** {rule['name']}")
                st.write(f"🔴 **Blocked Countries:** {', '.join(rule['country']) or 'None'}")
                st.write(f"📍 **Blocked Locations:** {', '.join(rule['location']) or 'None'}")
                st.write(f"⏳ **Restricted Time Ranges:** {', '.join(rule['time']) or 'None'}")
                st.markdown("---")

elif page == "Manage Lists":
    st.title("📜 Manage Whitelist, Blacklist, and Blocked List")

    list_type = st.selectbox("Select List Type", ["Whitelist", "Blacklist", "Blocked"])
    phone_number = st.text_input("Enter Phone Number:").strip()
    
    if st.button("Add to List"):
        if phone_number:
            update_phone_list(list_type.lower(), phone_number, action="add")
            st.success(f"✅ Added {phone_number} to {list_type}.")
        else:
            st.error("Please enter a valid phone number.")

    if st.button("Remove from List"):
        if phone_number:
            update_phone_list(list_type.lower(), phone_number, action="remove")
            st.success(f"🚫 Removed {phone_number} from {list_type}.")
        else:
            st.error("Please enter a valid phone number.")

    st.write(f"### Current {list_type}")
    with st.expander(f"View {list_type}", expanded=False):
        phone_list = get_phone_list(list_type.lower())
        if not phone_list:
            st.write(f"No numbers in {list_type}.")
        else:
            for num in phone_list:
                st.write(f"📞 {num}")

elif page == "API Data List":
    st.title("📜 API Data List (Stored Lookup History)")
    
    with st.expander("🔍 Search API History", expanded=False):
        search_number = st.text_input("Search by Number:").strip()
        if st.button("Search"):
            api_history = [record for record in get_api_history() if search_number in record["number"]]
        else:
            api_history = get_api_history()

    if not api_history:
        st.write("No API data stored yet.")
    else:
        for record in api_history:
            st.markdown(f"### 📞 **Number:** {record['number']}")
            st.write(f"📅 **Lookup Time:** {record['timestamp']}")
            st.json(record["response"])
            st.markdown("---")
