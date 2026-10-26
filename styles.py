import streamlit as st

def inject_styles():
    st.markdown("""
<style>

body {
    background-color: #f5f7fa;
}

.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 1rem;
}

[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #e0e0e0;
}

.card {
    background-color: white;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.06);
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.06);
}

.big-title {
    font-size: 38px;
    font-weight: bold;
    color: #1b5e20;
}

.green-text {
    color: #1b5e20;
    font-weight: bold;
}

.red-text {
    color: red;
    font-weight: bold;
}

.blue-text {
    color: #1565c0;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)
