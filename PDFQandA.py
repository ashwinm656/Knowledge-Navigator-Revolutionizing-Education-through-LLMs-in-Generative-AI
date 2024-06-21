import streamlit as st
import os
import csv
from PyPDF2 import PdfReader
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import TokenTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI

class PDFQuestionAnsweringSystem:
    def __init__(self):
        # Set OpenAI API key
        os.environ["OPENAI_API_KEY"] = "your_key"

        # Set up Streamlit page layout
        #st.set_page_config(layout="wide")

    def file_processing(self, file_path):
        loader = PyPDFLoader(file_path)
        data = loader.load()

        question_gen = ''

        for page in data:
            question_gen += page.page_content

        splitter_ques_gen = TokenTextSplitter(
            model_name='gpt-3.5-turbo',
            chunk_size=10000,
            chunk_overlap=200
        )

        chunks_ques_gen = splitter_ques_gen.split_text(question_gen)

        document_ques_gen = [Document(page_content=t) for t in chunks_ques_gen]

        splitter_ans_gen = TokenTextSplitter(
            model_name='gpt-3.5-turbo',
            chunk_size=1000,
            chunk_overlap=100
        )

        document_answer_gen = splitter_ans_gen.split_documents(document_ques_gen)

        return document_ques_gen, document_answer_gen

    def llm_pipeline(self, file_path):
        document_ques_gen, document_answer_gen = self.file_processing(file_path)

        llm_ques_gen_pipeline = ChatOpenAI(
            temperature=0.3,
            model="gpt-3.5-turbo"
        )

        prompt_template = """
        You are an expert at creating questions based on study materials and reference guides.
        Your goal is to prepare a student or teacher for their exam and tests.
        You do this by asking questions about the text below:

        ------------
        {text}
        ------------

        Create questions that will prepare the students or teachers for their tests.
        Make sure not to lose any important information.

        QUESTIONS:
        """

        PROMPT_QUESTIONS = PromptTemplate(template=prompt_template, input_variables=["text"])

        refine_template = ("""
        You are an expert at creating practice questions based on study material and documentation.
        Your goal is to help a student or teacher for thier exam and tests.
        We have received some practice questions to a certain extent: {existing_answer}.
        We have the option to refine the existing questions or add new ones.
        (only if necessary) with some more context below.
        ------------
        {text}
        ------------

        Given the new context, refine the original questions in English.
        If the context is not helpful, please provide the original questions.
        QUESTIONS:
        """
        )

        REFINE_PROMPT_QUESTIONS = PromptTemplate(
            input_variables=["existing_answer", "text"],
            template=refine_template,
        )

        ques_gen_chain = load_summarize_chain(llm=llm_ques_gen_pipeline,
                                              chain_type="refine",
                                              verbose=True,
                                              question_prompt=PROMPT_QUESTIONS,
                                              refine_prompt=REFINE_PROMPT_QUESTIONS)

        ques = ques_gen_chain.run(document_ques_gen)

        embeddings = OpenAIEmbeddings()

        vector_store = FAISS.from_documents(document_answer_gen, embeddings)

        llm_answer_gen = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")

        ques_list = ques.split("\n")
        filtered_ques_list = [element for element in ques_list if element.endswith('?') or element.endswith('.')]

        answer_generation_chain = RetrievalQA.from_chain_type(llm=llm_answer_gen,
                                                              chain_type="stuff",
                                                              retriever=vector_store.as_retriever())

        return answer_generation_chain, filtered_ques_list

    def get_csv(self, file_path):
        answer_generation_chain, ques_list = self.llm_pipeline(file_path)
	  #Path to store the output CSV file
        base_folder = r'Destination_path'

        if not os.path.isdir(base_folder):
            os.mkdir(base_folder)
        output_file = os.path.join(base_folder, "QA.csv")
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Question", "Answer"])  # Writing the header row

            for question in ques_list:
                answer = answer_generation_chain.run(question)
                csv_writer.writerow([question, answer])

        return output_file

    def main(self):
        st.title("PDF Question Answering System")
        st.write("Upload a PDF file to generate questions and answers.")

        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

        if uploaded_file:
            if st.button("Generate Questions and Answers"):
                temp_pdf_file = "temp.pdf"
                with open(temp_pdf_file, "wb") as f:
                    f.write(uploaded_file.read())  # Write the content of the uploaded file directly

                output_file = self.get_csv(temp_pdf_file)
                st.write(f"Questions and answers generated successfully. [Download CSV file]({output_file})")

                # Clean up temporary PDF file
                os.remove(temp_pdf_file)

if __name__ == "__main__":
    pdf_qa_system = PDFQuestionAnsweringSystem()
    pdf_qa_system.main()