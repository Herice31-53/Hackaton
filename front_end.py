import streamlit as st
import requests
from datetime import datetime

def fetch_available_keys():
    url = "https://api.ghostnet.tzkt.io/v1/contracts/KT1Vt4uo8xxjScd4wLtjqhNmDC33SkkMUvvr/bigmaps/boards/keys"
    response = requests.get(url)
    if response.status_code == 200:
        keys = response.json()
        return [key['key'] for key in keys]
    else:
        st.error("Failed to fetch available keys.")
        return []

def fetch_and_display_data_history(key_name):
    url = f"https://api.ghostnet.tzkt.io/v1/contracts/KT1Vt4uo8xxjScd4wLtjqhNmDC33SkkMUvvr/bigmaps/boards/keys/{key_name}/updates"
    response = requests.get(url)

    if response.status_code == 200:
        updates = response.json()
        
        st.session_state.data_history = []

        for update in updates:
            formatted_timestamp = datetime.strptime(update['timestamp'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d/%m/%Y %H:%M')
            display_data = {
                'Timestamp': formatted_timestamp,
                'CO2 Emission': f"{str(int(update['value']['eco'])*0.001)} kg eq CO2",
                'Cost': f"{str(int(update['value']['cost'])*0.1)} €"
            }
            st.session_state.data_history.append(display_data)
        
        display_history()
    else:
        st.error(f"Failed to fetch data for '{key_name}'. Status code: {response.status_code}")

def display_history():
    """Display the history of fetched data in a structured layout, with the latest operations on top."""
    if 'data_history' in st.session_state:
        for i, data in enumerate(reversed(st.session_state.data_history), 1):
            operation_number = len(st.session_state.data_history) - i + 1
            st.markdown(f"### Operation {operation_number}")
            st.markdown(f"- **Date and Time**: {data['Timestamp']}")
            st.markdown(f"- **CO2 Emission**: {data['CO2 Emission']}")
            st.markdown(f"- **Cost**: {data['Cost']}")

st.title("Data Fetcher")

available_keys = fetch_available_keys()
key_name = st.selectbox("Choose a key to fetch data for", available_keys, help="Select a key to fetch its data history.")

if st.button(f"Fetch data history for '{key_name}'", help="Click to fetch the historical data for the specified key."):
    fetch_and_display_data_history(key_name)
