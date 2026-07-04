import streamlit as st
import requests

st.set_page_config(layout="wide")

API_URL = "http://localhost:8000"

def login_page():
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username (Email)")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            response = requests.post(
                f"{API_URL}/api/user/token",
                data={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.token = data["access_token"]
                st.session_state.user = data["user"]
                st.rerun()
            else:
                st.error("Invalid credentials")

def register_page():
    st.title("Register")
    with st.form("register_form"):
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Register"):
            response = requests.post(
                f"{API_URL}/api/user/",
                json={"email": email, "username": username, "password": password}
            )
            if response.status_code == 200:
                st.success("Registration successful! Please head to the login page.")
            elif response.status_code == 409:
                st.error("User with this email already exists.")
            else:
                st.error(f"Registration failed: {response.text}")

if "token" not in st.session_state or st.session_state.token is None:
    pg = st.navigation([
        st.Page(login_page, title="Log in", icon=":material/login:"),
        st.Page(register_page, title="Register", icon=":material/person_add:")
    ])
else:
    with st.sidebar:
        st.toast(f"Welcome, {st.session_state.user.get('username', 'User')}!")
        if st.button("Logout"):
            del st.session_state.token
            del st.session_state.user
            st.rerun()
            
    pg = st.navigation([
        st.Page("pages/page_1.py", title="Home", icon=":material/home:"),
        st.Page("pages/page_2.py", title="Portfolios", icon="📊")
    ])

pg.run()


# Home, Portfolios (create, delete, edit, add assets...), Monte Carlo simulation (for a portfolio)
#  