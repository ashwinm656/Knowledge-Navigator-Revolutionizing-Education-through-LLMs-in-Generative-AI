import streamlit as st
from PyPDF2 import PdfReader
import tempfile

class PDFComparator:
    def __init__(self):
        self.st = st

    def compare_pdfs(self, pdf_file1, pdf_file2):
        """
        Compares two PDFs and returns a similarity score based on Cosine Similarity

        Args:
            pdf_file1 (str): Path to the first PDF file
            pdf_file2 (str): Path to the second PDF file

        Returns:
            float: Similarity score between 0 (no similarity) and 1 (identical)
        """

        with open(pdf_file1, 'rb') as f:
            pdf1 = PdfReader(f)
            text1 = ""
            for page in pdf1.pages:
                text1 += page.extract_text()
            text1 = text1.lower().strip()

        with open(pdf_file2, 'rb') as f:
            pdf2 = PdfReader(f)
            text2 = ""
            for page in pdf2.pages:
                text2 += page.extract_text()
            text2 = text2.lower().strip()

        # Tokenization and similarity calculation
        tokens1 = text1.split()
        tokens2 = text2.split()
        word_counts1 = set(tokens1)
        word_counts2 = set(tokens2)
        intersection = word_counts1.intersection(word_counts2)
        union = word_counts1.union(word_counts2)
        if len(union) == 0:
            return 0
        similarity = len(intersection) / len(union)

        return similarity

    def run(self):
        """
        Streamlit application for uploading and comparing PDFs
        """
        self.st.title("PDF Similarity Checker")
        uploaded_file1 = self.st.file_uploader("Choose First PDF", type="pdf")
        uploaded_file2 = self.st.file_uploader("Choose Second PDF", type="pdf")

        if uploaded_file1 is not None and uploaded_file2 is not None:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp1:
                    temp1.write(uploaded_file1.read())
                    pdf_file1 = temp1.name

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp2:
                    temp2.write(uploaded_file2.read())
                    pdf_file2 = temp2.name

                similarity = self.compare_pdfs(pdf_file1, pdf_file2)
                self.st.write(f"Similarity Score: {similarity:.2f}")

                if similarity == 1:
                    self.st.success("You are talented like that!")
                elif similarity > 0.75:
                    self.st.success("These PDFs are highly similar.")
                elif similarity > 0.5:
                    self.st.info("These PDFs are somewhat similar.")
                else:
                    self.st.warning("These PDFs have low similarity.")

            except Exception as e:
                self.st.error(f"An error occurred while processing PDFs: {e}")
                self.st.write("Please ensure the uploaded files are valid PDFs and try again.")

if __name__ == "__main__":
    pdf_comparator = PDFComparator()
    pdf_comparator.run()
