import streamlit as st 
from lida import Manager, TextGenerationConfig , llm  
from dotenv import load_dotenv
import os
import openai
from PIL import Image
from io import BytesIO
import base64
os.environ["OPENAI_API_KEY"] = "your_key"
# Set OpenAI API key
OPENAI_API_KEY = ""your_key"
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

class DataAnalyzer:
    def __init__(self):
        self.lida = Manager(text_gen=llm("openai"))
        self.textgen_config = TextGenerationConfig(
            n=1, temperature=0.5, model="gpt-3.5-turbo-0301", use_cache=True)
        self.library = "seaborn"

    def base64_to_image(self, base64_string):
        byte_data = base64.b64decode(base64_string)
        return Image.open(BytesIO(byte_data))

    def summarize_data(self, file_uploader):
        path_to_save = "filename.csv"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())
        summary = self.lida.summarize(
            "filename.csv", summary_method="default", textgen_config=self.textgen_config)
        st.write(summary)
        goals = self.lida.goals(summary, n=2, textgen_config=self.textgen_config)
        for goal in goals:
            st.write(goal)
        i = 0
        textgen_config = TextGenerationConfig(
            n=1, temperature=0.2, use_cache=True)
        charts = self.lida.visualize(
            summary=summary, goal=goals[i], textgen_config=self.textgen_config, library=self.library)
        img_base64_string = charts[0].raster
        img = self.base64_to_image(img_base64_string)
        st.image(img)

    def generate_graph(self, file_uploader, text_area):
        path_to_save = "filename1.csv"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())
        if len(text_area) > 0:
            st.info("Your Query: " + text_area)
            textgen_config = TextGenerationConfig(
                n=1, temperature=0.2, use_cache=True)
            summary = self.lida.summarize(
                "filename1.csv", summary_method="default", textgen_config=textgen_config)
            user_query = text_area
            charts = self.lida.visualize(
                summary=summary, goal=user_query, textgen_config=textgen_config)
            image_base64 = charts[0].raster
            img = self.base64_to_image(image_base64)
            st.image(img)


def main():
    data_analyzer = DataAnalyzer()
    menu = st.sidebar.selectbox(
        "Choose an Option", ["Summarize", "Question based Graph"])

    if menu == "Summarize":
        st.subheader("Visualization with CSV 📊🗒️")
        file_uploader = st.file_uploader("Upload your CSV", type="csv")
        if file_uploader is not None:
            data_analyzer.summarize_data(file_uploader)

    elif menu == "Question based Graph":
        st.subheader("Query your Data to Generate Graph")
        file_uploader = st.file_uploader("Upload your CSV", type="csv")
        if file_uploader is not None:
            text_area = st.text_area(
                "Query your Data to Generate Graph", height=200)
            if st.button("Generate Graph"):
                data_analyzer.generate_graph(file_uploader, text_area)


if __name__ == "__main__":
    main()