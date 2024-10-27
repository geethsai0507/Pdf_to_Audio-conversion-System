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

#Background colour

# Use st.markdown with the appropriate CSS to set the background color
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
#ITALIC Caption
st.subheader("*🪄 Your PDFs, now with superpowers! ‍♀️ Transform them into audiobooks and unlock the power of listening.*")
st.markdown(" > Upload your English PDF and choose a language.This tool will convert the text to spoken audio,creating downloadable audiobook chapters in your chosen language!")
# Choosing language
inp = st.selectbox("choose one of the language to convert the pdf",gtts.lang.tts_langs().keys())
#inp = (i for i in googletrans.LANGUAGES if googletrans.LANGUAGES[i]==option)
st.markdown("*you have choosen*")
st.write(googletrans.LANGUAGES.get(inp))

file_path= st.text_input("Enter file path 	:open_file_folder:")
time.sleep(15)
file_name = os.path.splitext(os.path.basename(file_path))[0]
st.write(f"Processing file: {file_name}")#
print(file_name)
file=open(file_path,'rb')
reader=PdfReader(file)
num_pages=len(reader.pages)
st.write("the number of pages are ",num_pages)
#output_filename = st.text_input("Enter output file path for translation text storage :open_file_folder:")
# Output file path input
output_dir = st.text_input("Enter output directory for storing the audio files :open_file_folder:")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)  # Create directory if it doesn't exist
page_count = 0
current_text = ""
file_count = 1
estimated_processing_time_per_page = 2
for p in range(num_pages):
    page=reader.pages[p]
    text=page.extract_text()
    #print(text)
    
    
    translator = GoogleTranslator(source='en', target=inp)
    translated_text = translator.translate(text)
    current_text += translated_text
    page_count += 1
    
    if page_count == 60  or p == num_pages - 1:
        
        #translating text
        print(current_text)
        text_filename = f"{file_name}_{file_count}.txt"
        text_save_path = os.path.join(output_dir, text_filename)
        with open(text_save_path, 'w', encoding='utf-8') as text_file:
            text_file.write(current_text)
        try:
            #converting to audio
            converted_audio = gtts.gTTS(current_text, lang=inp, slow=False)
            # Create a progress bar with clear labels and initial progress
            st.write("Generating Audio :musical_score:")
            
            # Generate unique filename with appropriate extension based on gTTS capabilities
            #'''filename = f"{file_name}{file_count}.mp3"
            #converted_audio.save(filename)'''

            audio_filename = f"{file_name}_{file_count}.mp3"
            save_path = os.path.join(output_dir, audio_filename)
            converted_audio.save(save_path)
            st.write(f"Audio file saving at: {save_path}")


        except Exception as e:
            st.write("REQUEST LIMIT REACHED")
        progress_bar = st.progress(0)
        k=0
        for i in range(100):
            # Update progress bar for each fragment
            k=k+4
            progress_bar.progress(k)
            time.sleep(2)
            if(k==100):
                break
        if(page_count-60+1 < 0):
            st.write(f"Translation to {googletrans.LANGUAGES.get(inp)} completed (Pages {1} to {page_count})")
        else:
            st.write(f"Translation to {googletrans.LANGUAGES.get(inp)} completed (Pages {page_count - 60 + 1} to {page_count})")
        st.write(f"Audio file '{audio_filename}' created\n")

        current_text = ""  # Reset for next audio file
        page_count = 0
        file_count += 1

        time.sleep(400)
