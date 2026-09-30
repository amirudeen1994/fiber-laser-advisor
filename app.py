import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Fiber Laser Cut Advisor", page_icon="⚡")
st.title("⚡ Fiber Laser Cut Quality & Parameter Advisor")
st.write("உங்கள் ஃபைபர் லேசர் கட்டிங் புகைப்படத்தை அப்லோட் செய்து பாராமீட்டர் மாற்றங்களை உடனடியாகப் பெறுங்கள்.")

API_KEY = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if API_KEY:
    genai.configure(api_key=API_KEY)
    
    st.sidebar.header("Cutting Setup")
    material = st.sidebar.selectbox("Material Type", ["Mild Steel (CS)", "Stainless Steel (SS)", "Aluminum", "Brass"])
    thickness = st.sidebar.number_input("Thickness (mm)", min_value=0.5, max_value=30.0, value=3.0, step=0.5)
    gas_type = st.sidebar.selectbox("Auxiliary Gas Used", ["Oxygen (O2)", "Nitrogen (N2)", "Compressed Air"])

    uploaded_file = st.file_uploader("Upload cut edge picture:", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Cutting Sample", use_column_width=True)

        if st.button("Analyze Quality 🔍"):
            with st.spinner("Analyzing cut edge defects and calculating optimal parameters..."):
                try:
                    prompt = f"""
                    You are an expert Fiber Laser Cutting Field Engineer specializing in industrial CNC software (CypCut, TubePro, BodorThinker).
                    Analyze the provided image of a sheet metal cut edge.

                    Job Details:
                    - Material: {material}
                    - Thickness: {thickness} mm
                    - Cutting Gas: {gas_type}

                    Provide a structured response in clear Tamil and English:
                    1. **Defect Identification**: What exact defect is present? (Bottom Dross, Rough Burrs, Top Slag, Striations, Incomplete Piercing).
                    2. **Root Cause Analysis**: Why did this defect happen with {gas_type} at {thickness}mm?
                    3. **Recommended Parameter Adjustments**: Provide precise relative adjustment recommendations in a table:
                       - Cutting Speed (Increase / Decrease by X%)
                       - Focus Position (Shift Up / Down by X mm)
                       - Gas Pressure (Increase / Decrease by X bar)
                       - Laser Power / Duty Cycle (%)
                    4. **Engineer Tips**: Checks for nozzle centering, protective lens cleanliness, or focus calibration.
                    """
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content([prompt, image])
                    st.success("Analysis Complete!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error analyzing image: {e}")
else:
    st.warning("Please enter your Gemini API Key in the sidebar to start.")
