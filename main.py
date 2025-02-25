import streamlit as st
import google.generativeai as genai
def initialize_gemini():
    genai.configure(api_key="AIzaSyD2pu_pjTzWVhy9nqJ0hp1DBhzSQMe8ZHA")

def convert_units(value, from_unit, to_unit):
    conversion_factors = {
        ('meters', 'kilometers'): 0.001,
        ('kilometers', 'meters'): 1000,
        ('grams', 'kilograms'): 0.001,
        ('kilograms', 'grams'): 1000,
        ('celsius', 'fahrenheit'): lambda c: (c * 9/5) + 32,
        ('fahrenheit', 'celsius'): lambda f: (f - 32) * 5/9
    }
    
    if (from_unit, to_unit) in conversion_factors:
        factor = conversion_factors[(from_unit, to_unit)]
        return factor(value) if callable(factor) else value * factor
    return None

def get_gemini_response(query):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(query)
    return response.text if response else "No response from Gemini."

def main():
    st.title("Unit Converter with Gemini AI")
    
    unit_types = {
        "Length": ["meters", "kilometers"],
        "Mass": ["grams", "kilograms"],
        "Temperature": ["celsius", "fahrenheit"]
    }
    
    category = st.selectbox("Select unit category", list(unit_types.keys()))
    from_unit = st.selectbox("From", unit_types[category])
    to_unit = st.selectbox("To", unit_types[category])
    value = st.number_input("Enter value", min_value=0.0, format="%.2f")
    
    if st.button("Convert"):
        result = convert_units(value, from_unit, to_unit)
        if result is not None:
            st.success(f"Converted Value: {result} {to_unit}")
        else:
            st.error("Conversion not available")
    
    st.subheader("Ask Gemini AI")
    user_query = st.text_area("Enter your question")
    
    if st.button("Ask AI"):
        initialize_gemini()
        response = get_gemini_response(user_query)
        st.info(response)

if __name__ == "__main__":
    main()
