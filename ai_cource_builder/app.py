import streamlit as st
import PyPDF2
import ollama
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()
youtube_key = os.getenv("YOUTUBE_API_KEY")

# Extract PDF Text
def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text[:6000] # Local models prefer shorter chunks for speed


def get_video(query):
    try:
        youtube = build("youtube", "v3", developerKey=youtube_key)
        request = youtube.search().list(q=query, part="snippet", maxResults=1, type="video")
        res = request.execute()
        return f"https://www.youtube.com/watch?v={res['items'][0]['id']['videoId']}"
    except:
        return None


st.title(" Local AI Course Builder")
st.caption("Running fully offline with Ollama")

uploaded_file = st.file_uploader("Upload Study PDF", type="pdf")

if uploaded_file and st.button("Generate Local Course"):
    with st.spinner("Your local AI is thinking..."):
        context = extract_text(uploaded_file)
        
        
        response = ollama.chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': f"Create a simple 3-module syllabus with titles based on this: {context}",
            },
        ])
        
        syllabus = response['message']['content']
        st.success("Course Created!")
        st.markdown(syllabus)
        
        
        video_url = get_video(syllabus[:50])
        if video_url:
            st.video(video_url)