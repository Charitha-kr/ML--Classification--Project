import streamlit as st
import pandas as pd
import joblib

# Load trained model and encoders
model = joblib.load("rf_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")
target_encoder = joblib.load("target_encoder.pkl")

# Features used
selected_features = [
    "Preferred Work Environment",
    "Academic Performance (CGPA/Percentage)",
    "Motivation for Career Choice ",
    "Leadership Experience",
    "Tech-Savviness"
]

st.title("💼 Career Predictor")
st.markdown("**Find out what career suits you based on your personality and preferences!**")

# Take user input
user_input = {}

for feature in selected_features:
    if feature in label_encoders:
        options = list(label_encoders[feature].classes_)
        user_input[feature] = st.selectbox(f"{feature}", options)
    else:
        user_input[feature] = st.number_input(f"{feature}", min_value=0.0, max_value=10.0, step=0.1)

# Predict button
if st.button("🔍 Predict Career"):
    # Preprocess input
    for feature in label_encoders:
        user_input[feature] = label_encoders[feature].transform([user_input[feature]])[0]
    
    user_df = pd.DataFrame([user_input])
    user_scaled = scaler.transform(user_df)

    # Prediction
    predicted_class = model.predict(user_scaled)[0]
    predicted_proba = model.predict_proba(user_scaled).max()

    career = target_encoder.inverse_transform([predicted_class])[0]

    st.success(f"✅ Based on your input, you are most likely to become a **{career}**.")
    st.info(f"📊 Confidence: {round(predicted_proba * 100, 2)}%")
