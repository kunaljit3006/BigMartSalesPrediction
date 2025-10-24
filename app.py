import streamlit as st
import pickle
import numpy as np
import base64
import os

# --- Load Model ---
filename = 'bigmart_model.pkl'
try:
    model = pickle.load(open(filename, 'rb'))
except Exception as e:
    st.error(f"❌ Model loading failed: {e}")
    st.stop()

# --- Page Config ---
st.set_page_config(page_title="Big Mart Price Prediction", page_icon="🛒", layout="centered")

# --- Background Image ---
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("bg.png")

# --- Custom CSS ---
st.markdown("""
<style>
/* Layout transparency */
.main .block-container {
    background: transparent !important;
    padding-top: 2rem;
}

/* Neon title */
h1 {
    text-align: center;
    color: #00FFFF;
    text-shadow: 0 0 15px #00FFFF, 0 0 25px #007777;
    font-size: 2.8em;
    margin-bottom: 0.2em;
}
p.subtitle {
    text-align: center;
    color: #b0f0f0;
    font-size: 1.1em;
    margin-bottom: 1.8em;
}

/* Cards */
.card {
    background: rgba(10, 25, 35, 0.8);
    border: 1px solid rgba(0,255,255,0.4);
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 0 20px rgba(0,255,255,0.2);
    backdrop-filter: blur(8px);
    margin-bottom: 25px;
}

/* Inputs */
.stTextInput>div>div>input,
.stNumberInput>div>div>input,
div[data-baseweb="select"] > div {
    background-color: rgba(25, 45, 55, 0.9)!important;
    color: #E0FFFF!important;
    border: 1px solid rgba(0,255,255,0.4)!important;
    border-radius: 8px;
    box-shadow: inset 0 0 8px rgba(0,255,255,0.3);
}
div[data-baseweb="select"] span {
    color: #E0FFFF !important;
}
div[data-baseweb="popover"] {
    background-color: rgba(20,30,40,0.95)!important;
    color: #E0FFFF!important;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #00FFFF, #0077FF);
    color: black !important;
    border: none;
    border-radius: 10px;
    padding: 12px 25px;
    font-weight: bold;
    width: 100%;
    box-shadow: 0 0 15px rgba(0,255,255,0.6);
    transition: 0.3s ease-in-out;
}
.stButton>button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 25px rgba(0,255,255,0.9);
}

/* Result box */
.result {
    background: rgba(0,255,255,0.15);
    border: 1px solid rgba(0,255,255,0.5);
    border-radius: 12px;
    text-align: center;
    padding: 15px;
    margin-top: 25px;
    font-size: 1.3em;
    color: #00FFFF;
    text-shadow: 0 0 10px #00FFFF;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 40px;
    font-size: 0.85em;
    color: #66ffff;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1>🛒 Big Mart Price Prediction</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Predict sales based on item and outlet details</p>', unsafe_allow_html=True)

# --- Input Form ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📦 Item Details")
col1, col2, col3 = st.columns(3)
with col1:
    item_identifier = st.number_input("Item Identifier (0-1550)", 0, 1550, 0)
    item_weight = st.number_input("Item Weight (kg)", 1.0, 25.0, 12.5, 0.1)
with col2:
    fat_options = {"Low Fat":0, "Regular":1, "Non-Edible":2}
    item_fat = st.selectbox("Item Fat Content", fat_options.keys())
    item_visibility = st.number_input("Item Visibility", 0.0, 0.35, 0.07, 0.001)
with col3:
    item_type = st.number_input("Item Type (0-15)", 0, 15, 6)
    item_mrp = st.number_input("Item MRP", 32.0, 270.0, 150.0, 0.5)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🏬 Outlet Details")
col4, col5, col6, col7 = st.columns(4)
with col4:
    outlet_id = st.number_input("Outlet Identifier (0-9)", 0, 9, 5)
    outlet_year = st.number_input("Establishment Year", 1985, 2009, 1999)
with col5:
    size_options = {"Small":2, "Medium":1, "High":0}
    outlet_size = st.selectbox("Outlet Size", size_options.keys())
with col6:
    location_options = {"Tier 1":0, "Tier 2":1, "Tier 3":2}
    outlet_location = st.selectbox("Outlet Location Type", location_options.keys())
with col7:
    type_options = {"Grocery Store":0, "Supermarket Type1":1, "Supermarket Type2":2, "Supermarket Type3":3}
    outlet_type = st.selectbox("Outlet Type", type_options.keys())
st.markdown('</div>', unsafe_allow_html=True)

# --- Predict Button ---
if st.button("🔮 Predict Sales"):
    try:
        X = np.array([[item_identifier, item_weight, fat_options[item_fat],
                       item_visibility, item_type, item_mrp,
                       outlet_id, outlet_year,
                       size_options[outlet_size], location_options[outlet_location],
                       type_options[outlet_type]]])
        y_pred = model.predict(X)
        st.markdown(f'<div class="result">💰 Predicted Item Outlet Sales: ₹{y_pred[0]:.2f}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error during prediction: {e}")

# --- Footer ---
st.markdown('<p class="footer">Developed by <b>Kunaljit Kashyap</b></p>', unsafe_allow_html=True)
