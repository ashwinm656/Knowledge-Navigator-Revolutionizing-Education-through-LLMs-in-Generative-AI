import streamlit as st

class KnowledgeNavigator:
    BANNER = "Banner.png"

    def home_page(self):
        st.image(self.BANNER)
        st.write("""
            ## Welcome to Knowledge Navigator

            Knowledge Navigator is an innovative tool designed to streamline your information management and research processes. Our platform offers a range of modules to cater to various needs, ensuring an efficient and comprehensive experience.

            ### Modules Included:

            1. **Data Visualization with CSV:**
               - This module allows users to interact with CSV (Comma Separated Values) files through a Visualization.
               - Instructions:
                 - Upload your CSV file.
                 - You have two tasks: summarizing the data and creating a graph based on questions.
                 - Ask questions or give commands related to data manipulation.
                 - Receive instant responses and perform operations seamlessly.

            2. **Question Answering System:**
               - Our advanced Question Answering System empowers users to ask queries and receive precise answers from a vast knowledge base.
               - Instructions:
                 - Input your query in natural language.
                 - Explore accurate and relevant answers extracted from our extensive database.
                 - Enjoy quick access to information without tedious searches.

            3. **MCQ Generator:**
               - Simplify the process of generating multiple-choice questions with our MCQ Generator module.
               - Instructions:
                 - Specify the topic or subject.
                 - Set desired parameters such as difficulty level and number of questions.
                 - Obtain a set of well-crafted MCQs ready for use in assessments or learning materials.

            4. **Research Bot:**
               - The Research Bot module is your virtual assistant for conducting research tasks efficiently.
               - Instructions:
                 - Describe your research topic or query.
                 - Let the bot gather relevant resources, articles, and data points.
                 - Enhance your research process with curated information tailored to your needs.

                
            5. **Q and A Evaluvator:**
               - The Q&A evaluator streamlines the assessment process by automating the comparison between written responses and the answer key. This saves time compared to manual evaluation.
               - Instructions:
                 - Determine whether the material containing questions and answers is in image format or PDF format.
                 - If the material is in image format, upload the image containing the questions and answers. If it's in PDF format, upload the PDF document.
                 - Upload the written script containing your answers to the questions, as well as the answer key.
                 - The system will evaluate your written script against the answer key and provide a score based on how closely your responses match the correct answers.  

            ## Start Exploring

            Experience the power of knowledge at your fingertips with Knowledge Navigator. Whether you're managing data, seeking answers, generating quizzes, or conducting research, our platform offers the tools you need to succeed.

            """)
    def run(self):
        self.home_page()

# Instantiate the KnowledgeNavigator class and run the application
navigator = KnowledgeNavigator()
navigator.run()
