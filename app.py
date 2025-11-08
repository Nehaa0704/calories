import streamlit as st
import pickle
import numpy as np
import pandas as pd


# Page config
st.set_page_config(
    page_title="Calorie Estimator",
    page_icon="🔥",
    layout="centered",
)

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Custom CSS styling
st.markdown("""
<style>

/* ====== DARK MODE BACKGROUND ====== */
.stApp, .block-container, body {
    background-color: #0d1117 !important;
    color: white !important;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #161b22 !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Force all text to white */
* {
    color: white !important;
}

/* Upload box container */
[data-testid="stFileUploadDropzone"] {
    background-color: #1e242c !important;
    border: 2px dashed #00c6ff !important;
    border-radius: 12px !important;
    width: 260px !important;
    height: 85px !important;
    padding: 5px !important;
    display: flex;
    align-items: center;
    justify-content: center;
}
[data-testid="stFileUploadDropzone"] * {
    color: #00c6ff !important;
    font-weight: 600 !important;
}
[data-testid="stFileUploadDropzone"] svg {
    fill: #00c6ff !important;
    stroke: #00c6ff !important;
}

/* Number input */
[data-testid="stNumberInput"] input {
    background-color: #1e242c !important;
    color: white !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    padding: 8px !important;
    font-weight: 600;
}
.stNumberInput button {
    background-color: #0a3d62 !important;
    color: white !important;
    border-radius: 6px;
}
.stNumberInput button:hover {
    background-color: #082d49 !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(120deg,#0059ff,#00bfff);
    color: white !important;
    font-size: 18px;
    padding: 12px 28px;
    font-weight: 700;
    border-radius: 10px;
    border: none;
    transition: 0.3s ease;
}
.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(120deg,#00bfff,#0059ff);
}

/* Footer */
.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: #161b22 !important;
    border-top: 1px solid #30363d;
    padding: 8px 0;
    text-align: center;
    font-size: 14px;
    font-weight: 600;
    color: white;
    z-index: 99999;
}
.footer a {
    color: #58a6ff;
    text-decoration: none;
}

/* ✅ Centered Top Heading */
.custom-top-text {
    width: 100%;
    text-align: center;
    position: fixed;
    top: 5px;
    left: 0;
    right: 0;
    color: #00c6ff !important;
    font-weight: 900 !important;
    font-size: 32px !important;
    z-index: 9999999;
    text-shadow: 0px 0px 15px rgba(0,200,255,0.8);
    font-family: 'Segoe UI', sans-serif;
    pointer-events: none;
    letter-spacing: 2px;
}

/* Remove default header bar */
header { background: transparent !important; }

</style>

<div class="footer">
👩‍💻 <b>Yourname</b> | ✉️ yourmail@gmail.com | 📞 +91-XXXXXXXXXX
</div> 
               
<div class="custom-top-text">
         FitPulse 💪🔥
</div>

""", unsafe_allow_html=True)

# Title
st.markdown(
    "<h2 style='text-align:center; color:#58a6ff;'>🔥Fitness Calorie Burn Estimator</h2>",
    unsafe_allow_html=True
)

st.write("### Enter your activity information to estimate calories burned")

# Upload Dataset
st.markdown("### 📂 Upload Your Activity Dataset")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Dataset Uploaded Successfully!")
    
    st.write("### 👀 Preview Dataset")
    st.dataframe(df.head())

    required_cols = ["Very Active Minutes", "Fairly Active Minutes", "Lightly Active Minutes", "Steps"]
    
    if all(col in df.columns for col in required_cols):
        X = df[required_cols]
        predictions = model.predict(X)
        df["Predicted Calories"] = predictions
        st.write("### 🔥 Predictions")
        st.dataframe(df)

        st.download_button(
            label="⬇️ Download Results",
            data=df.to_csv(index=False),
            file_name="calories_result.csv",
            mime="text/csv",
        )
    else:
        st.error(f"❌ Dataset must contain columns: {required_cols}")

# Sidebar inputs
st.sidebar.header("📊 Activity Input Panel")
st.sidebar.write("Adjust your activity values:")

very = st.sidebar.number_input("Very Active Minutes ⏱️", 0, 200, 30)
fair = st.sidebar.number_input("Fairly Active Minutes 🏃", 0, 200, 10)
light = st.sidebar.number_input("Lightly Active Minutes 🚶", 0, 400, 100)
steps = st.sidebar.number_input("Steps 👣", 0, 30000, 8000)

st.sidebar.subheader("ℹ️ About")
st.sidebar.markdown("""
This tool predicts calories burned based on your activity.

**How it works:**
- Enter your daily active minutes & steps
- Click **Estimate Calories Burned**
- Get AI-powered calories 🔥

**Made for fitness tracking 🏋️‍♀️**
""")

# Activity summary
st.write("### 🧮 Activity Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Very Active", f"{very} min")
col2.metric("Fairly Active", f"{fair} min")
col3.metric("Light Active", f"{light} min")
col4.metric("Steps", f"{steps}")

# Prediction Button
if st.button("✨ Estimate Calories Burned"):
    data = np.array([[very, fair, light, steps]], dtype=float)
    prediction = model.predict(data)[0]
    calories = round(prediction, 2)

    with st.spinner("Calculating calories...🔥"):
        st.success(f"🔥 Estimated Calories Burned: **{calories} kcal**")
        progress = st.progress(0)
        for i in range(100):
            progress.progress(i + 1)
        st.balloons()
