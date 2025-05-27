import streamlit as st
import datetime
import pytz
from kundli_analyzer import KundliAnalyzer
from geopy.geocoders import Nominatim

# Set page config
st.set_page_config(
    page_title="Kundli Chat Bot",
    page_icon="🔮",
    layout="wide"
)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def main():
    st.title("🔮 Kundli Chat Bot")
    st.write("Welcome to the Kundli Analysis Chat Bot! Ask me anything about your kundli.")

    # Sidebar for birth details
    with st.sidebar:
        st.header("Enter Birth Details")
        name = st.text_input("Name")
        date = st.date_input("Date of Birth", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        time = st.time_input("Time of Birth")
        place = st.text_input("Place of Birth (City, Country)")

        if st.button("Analyze Kundli"):
            try:
                geolocator = Nominatim(user_agent="kundli_bot")
                location = geolocator.geocode(place)
                if not location:
                    st.error("Could not find the location. Please enter a valid place (e.g., Guna, India or New York, USA).")
                    return

                birth_datetime = datetime.datetime.combine(date, time)

                analyzer = KundliAnalyzer(name=name, birth_datetime=birth_datetime, place=place)

                st.session_state.analyzer = analyzer
                st.session_state.chat_history.append(("System", "Kundli has been analyzed. You can now ask questions about it!"))

            except Exception as e:
                st.error(f"Error analyzing kundli: {e}")

    # Initialize user_input in session state
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    def clear_input():
        st.session_state.user_input = ""

    st.header("Chat Interface")

    for role, message in st.session_state.chat_history:
        if role == "User":
            st.write(f"👤 You: {message}")
        else:
            st.write(f"🤖 Bot: {message}")

    user_input = st.text_input("Ask a question about your kundli:", key="user_input")

    if st.button("Send"):
        if user_input.strip() == "":
            st.warning("Please type a question.")
        elif 'analyzer' not in st.session_state:
            st.warning("Please enter birth details and analyze kundli first!")
        else:
            st.session_state.chat_history.append(("User", user_input))
            response = st.session_state.analyzer.get_response(user_input)
            st.session_state.chat_history.append(("Bot", response))
            clear_input()
            st.experimental_rerun()

if __name__ == "__main__":
    main()