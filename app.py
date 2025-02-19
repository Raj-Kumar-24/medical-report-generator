import streamlit as st 
import openai 
import PyPDF2
from openai import OpenAI

# User input for OpenAI API Key
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

if openai_api_key:
    client = OpenAI(api_key=openai_api_key)

    def extract_text_from_pdf(uploaded_file): 
        reader = PyPDF2.PdfReader(uploaded_file) 
        text = "".join([page.extract_text() for page in reader.pages if page.extract_text()]) 
        return text

    def generate_report(prompt): 
        response = client.chat.completions.create(            
                model="gpt-3.5-turbo",            
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.6    
            )  
        #return response["choices"][0]["message"]["content"].strip()
        return response.choices[0].message.content.strip()

    st.title("MRI Report AI Assistant")
    # File uploader
    uploaded_file = st.file_uploader("Upload MRI Report (PDF)", type="pdf")
    if uploaded_file: 
        with st.spinner("Extracting text from PDF..."): 
            report_text = extract_text_from_pdf(uploaded_file) 
            st.text_area("Extracted MRI Report:", report_text, height=250)
        if st.button("Generate Reports"):
            if report_text.strip():
                st.subheader("AI-Generated Reports")
                
                summary_prompt = f"Summarize this MRI report: {report_text}"
                patient_friendly_prompt = f"Explain this MRI report in simple terms for a patient: {report_text}"
                recommendation_prompt = f"Based on this MRI report, provide recommendations for the next steps: {report_text}"
                
                with st.spinner("Generating Summary..."):
                    summary = generate_report(summary_prompt)
                    st.write("### Summary:")
                    st.write(summary)
                
                with st.spinner("Generating Patient-Friendly Report..."):
                    patient_friendly = generate_report(patient_friendly_prompt)
                    st.write("### Patient-Friendly Report:")
                    st.write(patient_friendly)
                
                with st.spinner("Generating Recommendations..."):
                    recommendation = generate_report(recommendation_prompt)
                    st.write("### Recommendations:")
                    st.write(recommendation)
                
                st.subheader("Radiologist Review")
                st.write("Rate the quality of the AI-generated reports:")
                summary_rating = st.slider("Summary Quality", 1, 5, 3)
                patient_friendly_rating = st.slider("Patient-Friendly Report Quality", 1, 5, 3)
                recommendation_rating = st.slider("Recommendation Quality", 1, 5, 3)
                
                if st.button("Submit Ratings"):
                    st.success("Ratings submitted! Thank you for your feedback.")
            else:
                st.warning("No text extracted from PDF. Please upload a valid MRI report.")
else:
    st.warning("Please enter your OpenAI API Key.")
