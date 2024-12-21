import streamlit as st
from PyPDF2 import PdfReader
from googletrans import Translator
import googletrans
import gtts
import time
from deep_translator import GoogleTranslator
import io
from gtts import gTTS
import os

# Background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFCBCB;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Text to Audio")
# Italic Caption
st.subheader("*🪄 Your PDFs, now with superpowers! ‍ﺄ Transform them into audiobooks and unlock the power of listening.*")
st.markdown("> Upload your English PDF and choose a language. This tool will convert the text to spoken audio, creating downloadable audiobook chapters in your chosen language!")

# Choosing language
inp = st.selectbox("Choose one of the languages to convert the PDF", gtts.lang.tts_langs().keys())
st.markdown("*You have chosen*")
st.write(googletrans.LANGUAGES.get(inp))

# File uploader
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")
if uploaded_file is not None:
    file_name = os.path.splitext(uploaded_file.name)[0]
    st.write(f"Processing file: {file_name}")

    reader = PdfReader(uploaded_file)
    num_pages = len(reader.pages)
    st.write("The number of pages is", num_pages)

    # Output directory input
    output_dir = st.text_input("Enter output directory for storing the audio files :open_file_folder:")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create directory if it doesn't exist

    page_count = 0
    current_text = ""
    file_count = 1
    estimated_processing_time_per_page = 2

    for p in range(num_pages):
        page = reader.pages[p]
        text = page.extract_text()

        translator = GoogleTranslator(source='en', target=inp)
        translated_text = translator.translate(text)
        current_text += translated_text
        page_count += 1

        if page_count == 60 or p == num_pages - 1:
            # Translating text
            text_filename = f"{file_name}_{file_count}.txt"
            text_save_path = os.path.join(output_dir, text_filename)
            with open(text_save_path, 'w', encoding='utf-8') as text_file:
                text_file.write(current_text)

            try:
                # Converting to audio
                converted_audio = gtts.gTTS(current_text, lang=inp, slow=False)
                st.write("Generating Audio :musical_score:")

                # Generate unique filename
                audio_filename = f"{file_name}_{file_count}.mp3"
                save_path = os.path.join(output_dir, audio_filename)
                converted_audio.save(save_path)
                st.write(f"Audio file saving at: {save_path}")

            except Exception as e:
                st.write("REQUEST LIMIT REACHED")

            progress_bar = st.progress(0)
            k = 0
            for i in range(100):
                # Update progress bar for each fragment
                k = k + 4
                progress_bar.progress(k)
                time.sleep(2)
                if k == 100:
                    break

            if page_count - 60 + 1 < 0:
                st.write(f"Translation to {googletrans.LANGUAGES.get(inp)} completed (Pages {1} to {page_count})")
            else:
                st.write(f"Translation to {googletrans.LANGUAGES.get(inp)} completed (Pages {page_count - 60 + 1} to {page_count})")

            st.write(f"Audio file '{audio_filename}' created\n")

            current_text = ""  # Reset for next audio file
            page_count = 0
            file_count += 1

            time.sleep(400)
