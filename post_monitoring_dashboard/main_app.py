import visualisation
import current_patient
import discharged_patient
import streamlit as st


st.set_page_config(layout="wide") #fills the whole webpage instead of centre column
header = st.beta_container()

PAGES = {
    "Insights based on Current Patients": visualisation,
    "Current Patient Log": current_patient,
    "Discharged Patient Log": discharged_patient,
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]


page.app()

