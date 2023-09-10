import streamlit as st
import os
from gtts import gTTS

from workflow_text_to_text import generate_story_from_text

@st.cache_data(persist=True)
def generate_audio_from_story(text):
    speech = gTTS(text=text, lang='en', slow=False)
    speech.save("story.mp3")
    return "story.mp3"

st.set_page_config(
    page_title="AI Story Generator", layout="wide", page_icon="📖"
)


st.sidebar.markdown("### Select the genre/theme of the story:")

story_theme = st.sidebar.radio("Genre", ("Horror :ghost:", "Action :man-running:", "Romance :heart:", "Comedy :laughing:", "Historical :hourglass_flowing_sand:", "Science Fiction :rocket:"))

selected_theme = story_theme.split(":")[0].strip()

theme_based_prompts = {
    "Horror": "Write a horror story that ends mysteriously using: ",
    "Action": "Write a story with lots of action using: ",
    "Romance": "Write a romantic story using: ",
    "Comedy": "Write a funny story using: ",
    "Historical": "Write a story based on a historical event with the help of the input: ",
    "Science Fiction": "Write a science fiction story using: "
}

st.markdown("# AI Story Generator :book:")

with st.expander("About this app :bulb:", expanded=False):
    st.markdown("This app uses the **Clarifai AI** engine to generate stories based on the input you provide using **LLM** models. You can either upload an image or enter some text to get started. The app will then generate a story based on the input you provide. The story will be generated using the theme you choose, you can select the theme from the sidebar. The app will also generate an **audio file** of the story for you to listen to. You can **download the story as a text file or an audio file (mp3)**.")

st.markdown("## Choose the input type for generating the story")

input_type = st.radio("Input type", ("Text :pencil:", "Image"))

if input_type == "Text :pencil:":

    st.markdown("### Enter the sentences you want to have your story revolve around: ")

    input_text = st.text_area("Enter the text here", height=100)

    theme_based_input = theme_based_prompts[selected_theme] + " " + input_text

    if st.button("Generate story"):
        with st.status("Generating story...", expanded=True) as status_text:

            st.write("Fusing your story elements together...")
            st.write("This may take about 30-40 seconds (more if runnung the first time), please hang tight...")

            story = generate_story_from_text(theme_based_input)

            status_text.update(label="Story created!")
        
        st.markdown("### Your Story based on your input!")
        st.download_button('Download story as text file', story, 'story.txt')

        story_lines = story.split('\n')
        formatted_story = "\n".join(["##### " + line for line in story_lines])
        
        with st.expander("View story", expanded=True):
            st.markdown(formatted_story)
        
        with st.status("Generating audio...", expanded=True) as status_audio:

            st.write("Generating your audio file...")
            st.write("This may take about 10-20 seconds")

            generate_audio_from_story(story)
            
            status_audio.update(label="Audio generated...")
        
        st.audio("story.mp3")
        st.download_button('Download story as mp3 file', 'story.mp3', 'story.mp3')


            

if input_type == "Image":
    st.markdown("### Upload the image you want to start with")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=False, width=300)    
        if st.button("Generate story"):
            st.write("Story will be generated here")

