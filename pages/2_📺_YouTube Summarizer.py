import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt= """
You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 500 words. Please provide the summary of the text given here:  
"""

def extract_transcript_details(youtube_video_url):
    try:
        video = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video)
        transcript = ""

        for i in transcript_text:
            transcript += " " + i["text"]
        
        return transcript
    
    except Exception as e:
        raise e

def generate_response(transcript_text, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt + transcript_text)
    return response.text

st.set_page_config("YouTube Summarizer")
st.header("Summarizer Any YouTube Video")
st.markdown("Have you ever needed info now, but you don't have the time to watch the whole video? With this YouTube Summarizer, you can instantly grasp the key points of any YouTube video in just 500 words or less. Whether you’re catching up on the latest tutorials, lectures, or entertainment, this tool saves you time by delivering concise and accurate summaries.")

youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video = youtube_link.split("=")[1]
    print(video)
    st.image(f"http://img.youtube.com/vi/{video}/0.jpg", use_column_width=True)

if st.button("Get Summary"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_response(transcript_text, prompt)
        st.markdown("## Summary:")
        st.write(summary)