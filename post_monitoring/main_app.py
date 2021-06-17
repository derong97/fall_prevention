import app0
import app1
import app2

import streamlit as st

st.set_page_config(layout="wide") #fills the whole webpage instead of centre column
header = st.beta_container()

PAGES = {
    "Insights based on Current Patients": app0,
    "Current Patient Log": app1,
    "Discharged Patient Log": app2,
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]


page.app()

