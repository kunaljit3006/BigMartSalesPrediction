import streamlit as st
import pickle
import numpy as np
import base64
import os

# --- Load the model ---
filename = 'bigmart_model.pkl'
try:
    loaded_model = pickle.load(open(filename, 'rb'))
except FileNotFoundError:
    st.error(f"Error: The model file '{filename}' was not found. Please ensure it's in the same directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# --- Set page config ---
st.set_page_config(
    page_title="Big Mart Sales Prediction",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Function to set background image dynamically ---
def set_bg_image(image_file):
    current_dir = os.path.dirname(__file__)  # Get folder of the script
    bg_path = os.path.join(current_dir, image_file)
    if not os.path.exists(bg_path):
        st.error(f"Background image '{image_file}' not found in {current_dir}")
        return
    with open(bg_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Call this function with your actual file
set_bg_image("bg.png")

# --- Custom CSS for cards, text, inputs, buttons ---
custom_css = """
<style>
.main .block-container { background-color: transparent !important; padding-top: 2rem; padding-bottom: 2rem; }
.main, .stForm, header, footer { background-color: transparent !important; }

.custom-card { background-color: rgba(10, 25, 40, 0.7); border-radius: 15px; padding: 25px 35px; margin-bottom: 30px;
              box-shadow: 0 8px 16px rgba(0,0,0,0.5); border: 1px solid rgba(76, 175, 80, 0.4); backdrop-filter: blur(5px); }

h1 { color: #4CAF50 !important; text-align: center; text-shadow: 0 0 15px rgba(76,175,80,0.7); font-size:3em; margin-bottom:0.5em;}
h3 { color: #00BCD4 !important; text-align: center; margin-bottom:1.5em; font-size:1.8em; }

.footer-text { color: #78909C; text-align:center; font-size:0.85em; margin-top:30px; text-shadow:1px 1px 2px rgba(0,0,0,0.7); }

.stTextInput>div>div>input, .stNumberInput>div>div>input, div[data-baseweb="select"]>div {
    background-color: rgba(30,50,70,0.9)!important; color:#E0E0E0!important; border:1px solid #00BCD4!important;
    border-radius:8px; padding:10px 15px; box-shadow:0 2px 5px rgba(0,0,0,0.3); transition: all 0.3s ease-in-out;
}
.stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus, div[data-baseweb="select"]>div:focus-within {
    border-color: #4CAF50 !important; box-shadow:0 0 10px rgba(76,175,80,0.6);
}

.stButton>button { background-color:#4CAF50; color:white!important; border:none; border-radius:8px; padding:12px 25px;
                    font-size:1.2em; font-weight:bold; width:100%; margin-top:20px; box-shadow:0 4px 10px rgba(76,175,80,0.5);
                    transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;}
.stButton>button:hover { background-color:#5cb85c; transform:translateY(-2px); box-shadow:0 6px 15px rgba(76,175,80,0.7); }

.stSuccess { background-color: rgba(76,175,80,0.9)!important; color:white; border-radius:10px; padding:15px;
            text-align:center; font-size:1.1em; margin-top:25px; border:1px solid #4CAF50; box-shadow:0 4px 12px rgba(76,175,80,0.4);}
.stError { background-color: rgba(244,67,54,0.9)!important; color:white; border-radius:10px; padding:15px;
          text-align:center; font-size:1.1em; margin-top:25px; border:1px solid #F44336; box-shadow:0 4px 12px rgba(244,67,54,0.4);}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- App Layout ---
st.markdown("<h1>🛒 Big Mart Sales Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p>Enter the item and outlet details to predict the Item Outlet Sales.</p>", unsafe_allow_html=True)

# Item Details Card
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.markdown("<h3>Item Details</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    item_identifier = st.number_input('Item Identifier (0-1550)', 0, 1550, 0)
    item_weight = st.number_input('Item Weight (kg)', 1.0, 25.0, 12.5, 0.1)
with col2:
    fat_content_options = {"Low Fat":0, "Regular":1, "Non-Edible":2}
    item_fat_content_display = st.selectbox('Item Fat Content', list(fat_content_options.keys()))
    item_fat_content_encoded = fat_content_options[item_fat_content_display]
    item_visibility = st.number_input('Item Visibility', 0.0, 0.35, 0.07, 0.001)
with col3:
    item_type = st.number_input('Item Type (0-15)', 0, 15, 6)
    item_mrp = st.number_input('Item MRP', 32.0, 270.0, 150.0, 0.5)
st.markdown('</div>', unsafe_allow_html=True)

# Outlet Details Card
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.markdown("<h3>Outlet Details</h3>", unsafe_allow_html=True)
col4, col5, col6, col7 = st.columns(4)
with col4:
    outlet_identifier = st.number_input('Outlet Identifier (0-9)', 0, 9, 5)
    outlet_establishment_year = st.number_input('Outlet Establishment Year', 1985, 2009, 1999)
with col5:
    outlet_size_options = {"Small":2, "Medium":1, "High":0}
    outlet_size_display = st.selectbox('Outlet Size', list(outlet_size_options.keys()))
    outlet_size_encoded = outlet_size_options[outlet_size_display]
with col6:
    outlet_location_options = {"Tier 1":0, "Tier 2":1, "Tier 3":2}
    outlet_location_type_display = st.selectbox('Outlet Location Type', list(outlet_location_options.keys()))
    outlet_location_type_encoded = outlet_location_options[outlet_location_type_display]
with col7:
    outlet_type_options = {"Grocery Store":0, "Supermarket Type1":1, "Supermarket Type2":2, "Supermarket Type3":3}
    outlet_type_display = st.selectbox('Outlet Type', list(outlet_type_options.keys()))
    outlet_type_encoded = outlet_type_options[outlet_type_display]
st.markdown('</div>', unsafe_allow_html=True)

# Predict Button
st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
if st.button('Predict Sales 🏷️'):
    input_data = np.array([[item_identifier, item_weight, item_fat_content_encoded,
                            item_visibility, item_type, item_mrp,
                            outlet_identifier, outlet_establishment_year,
                            outlet_size_encoded, outlet_location_type_encoded,
                            outlet_type_encoded]])
    try:
        prediction = loaded_model.predict(input_data)
        st.success(f'💰 Predicted Item Outlet Sales: ₹{prediction[0]:.2f}')
    except Exception as e:
        st.error(f"An error occurred: {e}")
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<p class="footer-text">Developed by Kunaljit Kashyap</p>', unsafe_allow_html=True)
