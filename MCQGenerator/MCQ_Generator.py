import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from MCQGenerator import generate_evaluate_chain
from utils import read_file, get_table_data
from langchain_openai import ChatOpenAI

load_dotenv()

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
                background: url("page_bg.jpg");
            }
            .sidebar .sidebar-content {
                background: url("page_bg.jpg");
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

if __name__ == "__main__":
    app = MCQGeneratorApp()
    app.load_response_json()
    app.run()
