import streamlit as st

# This is important - Streamlit needs to know this is a page
st.set_page_config(page_title="Page 2")

API_URL = "http://localhost:8000"
token = st.session_state.token

headers = {
    "Authorization" : f"Bearer {token}"
}


def get_monthly_returns():
    response = requests.get(f"{API_URL}/api/assets/annual_returns/{ticker}")
    portfolios = response.json()
    total_value = np.sum([portfolio.get("amount") for portfolio in portfolios])
    
    return len(portfolios), total_value