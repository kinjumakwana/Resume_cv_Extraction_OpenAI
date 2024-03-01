import base64
import streamlit as st
from pdf2json import DocumentAnalyzer
import json

# Initialize DocumentAnalyzer
analyzer = DocumentAnalyzer()

def main():
    st.title("CV Analyzer")

    # File uploader
    uploaded_file = st.file_uploader("Upload CV (PDF or DOCX)", type=["pdf", "docx"])

    if uploaded_file is not None:
        # Analyze CV when file is uploaded
        st.write("Analyzing CV... Please wait.")
        result = analyzer.analyse_candidate(uploaded_file)
        
        print(result)
        # Display extracted information
        # st.write("### Extracted Information:")
        # st.write(f"**Name:** {result['name']}")
        # st.write(f"**Email:** {result['email']}")
        # st.write(f"**Contact No:** {result['phone']}")
        # st.write("### Summary:")
        # st.write(result['summary'])
        # st.write("### Recommended Jobs:")
        # st.write(", ".join(result['recommended_jobs']))

        # # Offer download link for JSON file
        st.markdown(get_download_link(result), unsafe_allow_html=True)

def get_download_link(data):
    """Generate a download link for the JSON file."""
    json_data = json.dumps(data, indent=4)
    b64 = base64.b64encode(json_data.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="cv_analysis.json">Download JSON File</a>'
    return href

if __name__ == "__main__":
    main()
