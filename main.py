import streamlit as st
from PyPDF2 import PdfReader
from googletrans import Translator, LANGUAGES
import gtts
import time
import os
from deep_translator import GoogleTranslator

# Set custom styles
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #87CEEB; /* Sky Blue */
        color: #000000; /* Black for better contrast */
        margin: 0;
        padding: 0;
    }

    .stApp {
        background-color: #FFFFFF; /* Solid White */
        border-radius: 15px;
        padding: 30px;
        margin-top: 50px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
    }

    h1 {
        font-size: 36px;
        text-align: center;
        color: #01928B; /* Teal Green */
        margin-bottom: 20px;
    }

    h2 {
        font-size: 24px;
        text-align: center;
        color: #FD9A02; /* Bright Orange */
        margin-bottom: 20px;
    }

    .stMarkdown {
        font-size: 16px;
        color: #774320; /* Chocolate Brown */
        text-align: center;
        margin-bottom: 30px;
    }

    .stTextInput, .stSelectbox, .stFileUploader {
        background-color: #F5F3C7; /* Soft Cream */
        border: 1px solid #01928B; /* Teal Green Border */
        color: #000000; /* Black text */
        font-size: 16px;
        padding: 12px;
        border-radius: 8px;
        margin: 0 auto;
        display: block;
        margin-bottom: 20px;
        width: 80%;
    }

    .stButton > button {
        background: #01928B; /* Teal Green */
        color: #FFFFFF; /* White text */
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        margin-top: 20px;
        transition: background 0.3s ease;
        border: none;
    }

    .stButton > button:hover {
        background: #FD9A02; /* Bright Orange on Hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subtitle
st.title("Text to Audio")
st.subheader("*🎧 From Text to Sound: Turn Your PDFs into Personalized Audiobooks!*")
st.markdown("This emphasizes the idea of a seamless transformation from text to audio and the personalization aspect.")

# Language selection
inp = st.selectbox("Choose a language to convert the PDF:", gtts.lang.tts_langs().keys())
st.write(f"You have chosen: {LANGUAGES.get(inp, 'Unknown')}")

# File uploader
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")
if uploaded_file:
    file_name = os.path.splitext(uploaded_file.name)[0]
    st.write(f"Processing file: {file_name}")

    # Output directory input
    output_dir = st.text_input("Enter output directory for storing the audio files :open_file_folder:")
    if output_dir:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        reader = PdfReader(uploaded_file)
        num_pages = len(reader.pages)
        st.write("The number of pages is", num_pages)

        # Initialize progress bar and status display
        progress_bar = st.progress(0)
        progress_status = st.empty()

        page_count = 0
        current_text = ""
        file_count = 1

        audio_file_path = None  # Initialize variable for the final audio file path

        for p in range(num_pages):
            page = reader.pages[p]
            text = page.extract_text()

            translator = GoogleTranslator(source='en', target=inp)
            translated_text = translator.translate(text)
            current_text += translated_text
            page_count += 1

            # Update progress bar incrementally
            progress = int(((p + 1) / num_pages) * 100)
            progress_bar.progress(progress)
            progress_status.text(f"Processing page {p + 1} of {num_pages}...")

            if page_count == 60 or p == num_pages - 1:
                # Save translated text to file
                text_filename = f"{file_name}_{file_count}.txt"
                text_save_path = os.path.join(output_dir, text_filename)
                with open(text_save_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(current_text)

                try:
                    # Convert text to audio
                    st.write("Please wait until we save the audio file :musical_note: ")
                    audio_filename = f"{file_name}_{file_count}.mp3"
                    save_path = os.path.join(output_dir, audio_filename)
                    converted_audio = gtts.gTTS(current_text, lang=inp, slow=False)
                    converted_audio.save(save_path)
                    st.write(f"Audio file saved at: {save_path}")

                    # Save the final audio file path to allow playback
                    audio_file_path = save_path
                except Exception as e:
                    st.error(f"Error generating audio: {e}")

                current_text = ""  # Reset for next batch
                page_count = 0
                file_count += 1

        progress_status.text("Processing complete!")  # Final status update
        st.success("All pages have been processed!")

        # Play the final audio file if available
        if audio_file_path:
            st.audio(audio_file_path, format='audio/mp3', start_time=0)

            # Provide an option to download the translated text file
            text_filename = f"{file_name}_{file_count - 1}.txt"
            text_save_path = os.path.join(output_dir, text_filename)
            
            # Button to download the translated text file
            with open(text_save_path, "r", encoding="utf-8") as text_file:
                text_content = text_file.read()

            st.download_button(
                label="Download Translated Text",
                data=text_content,
                file_name=text_filename,
                mime="text/plain"
            )

    else:
        st.warning("Please provide an output directory.")
