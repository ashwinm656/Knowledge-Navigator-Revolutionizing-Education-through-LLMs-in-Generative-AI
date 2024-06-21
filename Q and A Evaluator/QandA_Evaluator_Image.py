import streamlit as st
from PIL import Image
import pytesseract

class QAEvaluator:
    def __init__(self, tesseract_path):
        self.tesseract_path = tesseract_path
        self.pytesseract = pytesseract

    def get_image_text(self, image_file):
        try:
            image = Image.open(image_file)
            self.pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
            text = self.pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"Error processing image: {e}")
            return ""

    def compare_text_similarity(self, text1, text2):
        intersection = len(set(text1.split()) & set(text2.split()))
        union = len(set(text1.split()) | set(text2.split()))
        if not union:
            return 0  
        return intersection / union

    def run(self):
        st.title("Question and Answer Evaluator")

        uploaded_file1 = st.file_uploader("Upload the Script", type=["jpg", "jpeg", "png"])
        uploaded_file2 = st.file_uploader("Upload the actual script", type=["jpg", "jpeg", "png"])

        if uploaded_file1 is not None and uploaded_file2 is not None:
            text1 = self.get_image_text(uploaded_file1)
            text2 = self.get_image_text(uploaded_file2)

            similarity_score = self.compare_text_similarity(text1, text2)

            st.header("Extracted Text:")
            st.write("**Content hidden for privacy.**")

            st.header("Text Similarity Score")
            st.write(f"{similarity_score:.2f}")

            interpretation_message = ""
            if similarity_score >= 0.9:
                interpretation_message = "🎉 Congratulations on your exceptional performance in your recent assessments! 🌟 I want to take a moment to commend you for your hard work and commitment to your studies. 💪 Your dedication is truly admirable, and it's evident that you've put in a lot of effort to achieve such outstanding results. 📚 Your grasp of grammar and attention to detail are particularly impressive, reflecting a deep understanding of the subject matter. 💡 Keep up the fantastic work, and continue to strive for excellence. 🚀 I have no doubt that with your determination and talent, you'll continue to achieve great things in your academic journey. 👏 Well done, and keep shining bright! ✨."
            elif similarity_score >= 0.7:
                interpretation_message = "Congratulations on your recent assessments! 🎉 Your dedication to your studies is truly admirable, and it's evident that you've been putting in a lot of effort. 📚 While your performance is commendable, there are always areas where we can strive to improve. 💪 I encourage you to pay attention to areas where you may have faced challenges and work on strengthening them. Whether it's refining your understanding of certain concepts or sharpening your skills in specific areas, remember that growth comes from continuous improvement. 👍 Keep up the hard work and maintain your positive attitude towards learning. I'm confident that with your determination to improve, you'll reach even greater heights. Well done, and keep pushing yourself to be the best you can be"
            elif similarity_score >= 0.5:
                interpretation_message = "Congratulations on your recent assessments! 🎉 Your efforts have shown in your recent performance, reflecting a solid average score. 📚 While it's not the highest score, it's important to recognize the progress you've made and the effort you've put in. 💪 Remember, improvement is a journey, and every step forward counts. Take this as an opportunity to reflect on areas where you can enhance your understanding and skills. 👍 Keep up the hard work and stay committed to your studies. With determination and persistence, you'll continue to progress and achieve your goals. Well done, and keep pushing yourself towards excellence!"
            else:
                interpretation_message = "Let's talk about your recent assessments. While your performance has shown effort, it's clear that there's room for improvement. 📚 Don't be discouraged—every setback is an opportunity to learn and grow. 💪 Take some time to reflect on where you may have faced challenges and what steps you can take to overcome them. Remember, progress is a journey, and it's okay to take it one step at a time. 👣 Stay focused on your goals, and don't hesitate to reach out for support if needed. With dedication and perseverance, you have the potential to turn your weaknesses into strengths. Keep pushing yourself, and never stop striving for improvement. You've got this!"

            st.write(interpretation_message)
        else:
            st.info("Please upload both scripts to evaluate")

if __name__ == "__main__":
    TESSERACT_PATH = "tesseract.exe" 
    qa_evaluator = QAEvaluator(TESSERACT_PATH)
    qa_evaluator.run()
