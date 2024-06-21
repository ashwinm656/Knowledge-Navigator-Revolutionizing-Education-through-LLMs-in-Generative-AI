import streamlit as st
import os
from Visualisation_with_CSV import DataAnalyzer
from PDFQandA import PDFQuestionAnsweringSystem
from QandA_Evaluator_PDF import PDFComparator
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from langchain_community.callbacks import get_openai_callback
from MCQGenerator.MCQGenerator_Prompt import generate_evaluate_chain
from MCQGENERATOR.utils import read_file, get_table_data
from langchain_openai import ChatOpenAI
from Research_Bot import ResearchBot
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import base64
from HomePage import KnowledgeNavigator
from QandA_Evaluator_Image import QAEvaluator
import pytesseract
from PyPDF2 import PdfFileReader  # Import PyPDF2 for PDF processing

# Load credentials and configurations from YAML file
with open('Login_Credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Authenticate user
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
BACKGROUNDD ="Login_image.jpg"
def set_page_background(png_file):
    @st.cache_data()
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
        
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
                
            }}
        </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_page_background(BACKGROUNDD)
# Perform authentication
authentication_status = authenticator.login(fields={'Login': 'Proceed'})

# Handle authentication status
if st.session_state["authentication_status"] == False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] == None:
    st.warning("Please enter your username and password")
elif st.session_state["authentication_status"] == True:
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    load_dotenv()
    BACKGROUND ="Page_bg.jpg"
    def set_page_background(png_file):
        @st.cache_data()
        def get_base64_of_bin_file(bin_file):
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        
        bin_str = get_base64_of_bin_file(png_file)
        page_bg_img = f'''
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: cover;
                
                }}
            </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)

    set_page_background(BACKGROUND)
    class MCQGeneratorApp:
        def __init__(self):
            self.RESPONSE_JSON = None
            self.llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-3.5-turbo", temperature=0.5)

        def load_response_json(self):
            with open('Response.json', 'r') as file:
                self.RESPONSE_JSON = json.load(file)

        def run(self):
            st.markdown(
                """
                <style>
                .reportview-container {
                    background: url("bg.jpg");
                }
                .sidebar .sidebar-content {
                    background: url("bg.jpg");
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.title("MCQ Generator with LangChain")

            with st.form("user_inputs"):
                uploaded_file = st.file_uploader("Upload a PDF or Text file")
                mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
                subject = st.text_input("Insert Subjects", max_chars=20)
                tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")
                button = st.form_submit_button("Create MCQs")

                if button and uploaded_file is not None and mcq_count and subject and tone:
                    with st.spinner("Loading...."):
                        try:
                            # Replace PDF processing using PyPDF2
                            if uploaded_file.type == "application/pdf":
                                pdf_reader = PdfFileReader(uploaded_file)
                                text = ""
                                for page_num in range(pdf_reader.numPages):
                                    page = pdf_reader.getPage(page_num)
                                    text += page.extract_text()
                            else:
                                text = read_file(uploaded_file)

                            with get_openai_callback() as cb:
                                response = generate_evaluate_chain(
                                    {
                                        "text": text,
                                        "number": mcq_count,
                                        "subject": subject,
                                        "tone": tone,
                                        "response_json": json.dumps(self.RESPONSE_JSON)
                                    }
                                )
                        except Exception as e:
                            traceback.print_exception(type(e), e, e.__traceback__)
                            st.error("Error")
                        else:
                            print(f"Total Tokens:{cb.total_tokens}")
                            print(f"Prompt Tokens:{cb.prompt_tokens}")
                            print(f"Completion Tokens:{cb.completion_tokens}")
                            print(f"Total Cost:{cb.total_cost}")
                            if isinstance(response, dict):
                                quiz = response.get("quiz", None)
                                if quiz is not None:
                                    table_data = get_table_data(quiz)
                                    if table_data is not None:
                                        df = pd.DataFrame(table_data)
                                        df.index = df.index + 1
                                        st.table(df)
                                        st.text_area(label="Review", value=response["review"])
                                    else:
                                        st.error("Error in the table data")
                            else:
                                st.write(response)

    def main():
        st.title("Knowledge Navigator🌐")
        home_page = KnowledgeNavigator()
        analyzer = DataAnalyzer()
        qa_system = PDFQuestionAnsweringSystem()
        mcq_generator = MCQGeneratorApp()  
        bot = ResearchBot()
        oc = QAEvaluator("tesseract.exe")
        # Remove fitz-related PDFComparator import and usage


        menu = st.sidebar.selectbox(
            "Choose an Option",
            ["Home Page", "Data Visualization with CSV", "Question Answering System", "MCQ Generator", "Research Bot", "Q and A Evaluvator","Logout"]  # Add "Logout" option
        )

        if menu == "Data Visualization with CSV":
            st.subheader("Visualization with CSV 🗒️")
            option = st.radio("Select an option", ["summarize_data", "Question based Graph"])
            
            if option == "summarize_data":
                file_uploader = st.file_uploader("Upload your CSV", type="csv", key="csv_uploader")
                if file_uploader is not None:
                    analyzer.summarize_data(file_uploader)
            
            if option == "Question based Graph":
                st.subheader("Generate Graph")
                file_uploader_graph = st.file_uploader("Upload your CSV", type="csv", key="csv_uploader_graph")
                text_area = st.text_area(
                    "Query your Data to Generate Graph", height=200)
                if st.button("Generate Graph"):
                    analyzer.generate_graph(file_uploader_graph, text_area)

        elif menu == "Question Answering System":
            st.subheader("PDF Question Answering System")
            uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
            if uploaded_file:
                if st.button("Generate Questions and Answers"):
                    temp_pdf_file = "temp.pdf"
                    with open(temp_pdf_file, "wb") as f:
                        f.write(uploaded_file.read())  # Write the content of the uploaded file directly

                    output_file = qa_system.get_csv(temp_pdf_file)
                    st.write(f"Questions and answers generated successfully. [Download CSV file]({output_file})")

                    # Clean up temporary PDF file
                    os.remove(temp_pdf_file)
        elif menu == "MCQ Generator":  # Add MCQ Generator option
            mcq_generator.load_response_json()
            mcq_generator.run()
        elif menu == "Research Bot":
            bot.run()
        elif menu == "Logout":
            if st.button("Click to Log Out"):
                st.session_state.authentication_status = None
                st.rerun()
        elif menu == "Home Page":
            st.sidebar.markdown("---")
            st.sidebar.markdown("Developed by:")
            st.sidebar.markdown("")
            st.sidebar.markdown("**USER1**")
            st.sidebar.markdown("[LinkedIn Profile](<LINKEDIN_LINK>)")
            st.sidebar.markdown("---")
            st.sidebar.markdown("**USER2**")
            st.sidebar.markdown("[LinkedIn Profile](<LINKEDIN_LINK>)")
            st.sidebar.markdown("---")
            st.sidebar.markdown("Please feel free to contact us.")
            st.sidebar.text("© 2024 Knowledge Navigator Team.")


            # Developer info

            home_page.run()
        elif menu == "Q and A Evaluvator":
            option = st.radio("Select an option", ["Upload in image", "Upload in pdf"])
            if option == "Upload in image":
                oc.run()
            if option == "Upload in pdf":
                pdff.run()

    if __name__ == "__main__":
        main()
