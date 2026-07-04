import streamlit as st
import requests
import numpy as np
import pandas as pd

st.set_page_config(page_title="Page 1")


API_URL = "http://localhost:8000"
token = st.session_state.token
st.session_state.error=None

headers = {
    "Authorization" : f"Bearer {token}"
}

@st.cache_data
def getStatsPortfolio():
    response = requests.get(f"{API_URL}/api/portfolios/current", headers=headers)
    portfolios = response.json()
    total_value = np.sum([portfolio.get("amount") for portfolio in portfolios])
    
    return len(portfolios), total_value



@st.dialog("Create a portfolio")
def createPortfolio():

    name = st.text_input("Name")
    initial_deposit = st.text_input("Initial Deposit")
    description = st.text_input("Description")

    if st.button("Create"):
        response = requests.post(f"{API_URL}/api/portfolios/", json={
            "name" : name,
            "initial_deposit" : initial_deposit,
            "description" : description if description is not None else ""
        }, headers=headers)
        st.write(response.json())
        getPortfolios.clear()
        getStatsPortfolio.clear()
        st.rerun()
    

@st.cache_data
def getPortfolios():
    response = requests.get(f"{API_URL}/api/portfolios/current", headers=headers)
    portfolios = response.json()

    return portfolios


def showPortfolios():
    assets_db = get_assets()
    portfolios = getPortfolios()
    col1, col2, col3 = st.columns(3)
    for i, portfolio in enumerate(portfolios):
        with [col1, col2, col3][i % 3]:
            with st.container(border=True):
                st.write(f"**Name:** {portfolio.get('name')}")
                st.caption(f"**Initial Deposit:** ${portfolio.get('initial_deposit', 0):,.2f}")
                st.write(f"**Value:** ${portfolio.get('amount', 0):,.2f}")
                with st.expander(f"**Description:**") :
                    st.write(f"{portfolio.get("description") if portfolio.get("description") else "Empty"}")
                with st.expander(f"**Assets:**"):
                    assets = portfolio.get("assets")
                    data = {
                        "Ticker": [asset.get("ticker") for asset in assets],
                        "Quantity": [asset.get("quantity") for asset in assets]
                    }
                    st.table(data)
                addAssetButton = st.button("Add Assets", key=f"addAsset{i}")
                if addAssetButton :
                    st.session_state.selected_portfolio = portfolio.get("id")
                    addAsset(assets_db)
                

@st.cache_data
def get_assets():
    response = requests.get(f"{API_URL}/api/assets/", headers=headers)
    assets = response.json()
    return assets



@st.dialog("Add an asset")
def addAsset(assets):
    assets = pd.DataFrame(assets)
    asset_names = assets["name"]
    asset = st.selectbox("Ticker", asset_names)
    ticker = assets[assets["name"]==asset]["ticker"].iloc[0]
    quantity = st.text_input("Quantity")

    if st.button("Add"):
        response = requests.put(
                    f"{API_URL}/api/portfolios/current/{st.session_state.selected_portfolio}/{ticker}/{quantity}",
                    headers=headers
                )
        st.session_state.error = response.json()
        getPortfolios.clear()
        getStatsPortfolio.clear()
        st.rerun()
    
        




def layout():
    n, total_value = getStatsPortfolio()
    
    left_top, right_top = st.columns([1,3])

    with left_top :
        with st.container():
            col = st.columns(1,vertical_alignment="center")
            create = st.button("Create Portfolio", type="primary", use_container_width=True)
    with right_top:  
        with st.container(border=True):
            col1, col2 = st.columns(2,vertical_alignment="center")
            col1.metric("Number of Portfolios", n)
            col2.metric("Total Value", f"${total_value:,.2f}")
    
    if create:
        createPortfolio()

    showPortfolios()


layout()

if "selected_portfolio" in st.session_state:
    st.write("### Selected Portfolio Details:")
    st.write(st.session_state.selected_portfolio)
    
if "error" in st.session_state : 
    st.write(st.session_state.error)