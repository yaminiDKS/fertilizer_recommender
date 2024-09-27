import os
import streamlit as st
import google.generativeai as genai

# Configure the API key for Google Generative AI
os.environ["GEMINI_API_KEY"] = "AIzaSyBNb6Sf4w7YmdUvIUMvKyIpDvs7z3g8L4g"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model with the desired configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    # Safety settings can be adjusted as needed
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction="You are an agriculture expert. Recommend fertilizers to the crop by analyzing the crop name and the sensor data like moisture, pH, and temperature. If the name is not given, ask for it.",
)

# Start the chat session
chat_session = model.start_chat(history=[])

# Streamlit UI setup
st.title("AgriDiagnoX - Crop Fertilizer Recommendation")

# Input fields for user to provide crop name and sensor data
crop_name = st.text_input("Enter the name of the crop:", "")
moisture = st.number_input("Moisture Level (%)", min_value=0, max_value=100, value=55)
ph_level = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=6.8)
temperature = st.number_input("Temperature (°C)", min_value=-30.0, max_value=50.0, value=22.5)

# When the user clicks the button, generate a response
if st.button("Get Fertilizer Recommendation"):
    if crop_name:
        user_input = f"Crop: {crop_name}, Moisture: {moisture}%, pH: {ph_level}, Temperature: {temperature}°C"
    else:
        user_input = f"Moisture: {moisture}%, pH: {ph_level}, Temperature: {temperature}°C"

    # Send the message to the AI model
    response = chat_session.send_message(user_input)

    # Display the AI model's response
    st.markdown("### Recommendation:")
    st.write(response.text)


