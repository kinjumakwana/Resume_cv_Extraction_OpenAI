import base64
import streamlit as st
from pdf2json import DocumentAnalyzer
import json

# Initialize DocumentAnalyzer
analyzer = DocumentAnalyzer()

def main():
    st.title("CV Analyzer")

    # File uploader for multiple files
    uploaded_files = st.file_uploader("Upload CV (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

    if uploaded_files:
        # Analyze each uploaded CV
        for uploaded_file in uploaded_files:
            st.write(f"Analyzing {uploaded_file.name}... Please wait.")
            result = analyzer.analyse_candidate(uploaded_file)
            st.write(result)

            print(result)

            # Offer download link for JSON file
            st.markdown(get_download_link(result, uploaded_file.name), unsafe_allow_html=True)
    
    # Accept Single Cv Code 
    # uploaded_file = st.file_uploader("Upload CV (PDF or DOCX)", type=["pdf", "docx"])

    # if uploaded_file is not None:
    #     # Analyze CV when file is uploaded
    #     st.write("Analyzing CV... Please wait.")
    #     result = analyzer.analyse_candidate(uploaded_file)
        
    #     print(result)
        
    #     # # Offer download link for JSON file
    #     st.markdown(get_download_link(result), unsafe_allow_html=True)

# single Cv
# def get_download_link(data):
#     """Generate a download link for the JSON file."""
#     json_data = json.dumps(data, indent=4)
#     b64 = base64.b64encode(json_data.encode()).decode()
#     href = f'<a href="data:application/json;base64,{b64}" download="cv_analysis.json">Download JSON File</a>'
#     return href

# Multiple Cv
def get_download_link(data, file_name):
    """Generate a download link for the JSON file."""
    json_data = json.dumps(data, indent=4)
    b64 = base64.b64encode(json_data.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="{file_name}_analysis.json">Download JSON File</a>'
    return href

if __name__ == "__main__":
    main()
