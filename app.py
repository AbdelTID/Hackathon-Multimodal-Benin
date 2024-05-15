import streamlit as st
from st_audiorec import st_audiorec
import replicate
# import pypiwin32pip 
# from audio_recorder_streamlit import audio_recorder
# from bokeh.models.widgets import Button
# from bokeh.models import CustomJS
# from streamlit_bokeh_events import streamlit_bokeh_events
# from streamlit_mic_recorder import mic_recorder
import pyttsx3
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests
import zipfile
import time
import sys
import io
# from utils import icon
from streamlit_image_select import image_select
load_dotenv() ##load all the nevironment variables

from transformers import pipeline

# Create a speech recognition pipeline using a pre-trained model
# pipe = pipeline("automatic-speech-recognition", model="chrisjay/fonxlsr")

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
REPLICATE_MODEL_ENDPOINTSTABILITY = os.getenv("REPLICATE_MODEL_ENDPOINTSTABILITY")
NUM_IMAGES_PER_ROW = 3
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat(history=[])
def get_gemini_response(question):
    
    response =chat.send_message(question,stream=True)
    return response

def display_chat_messages() -> None:
    """Print message history
    @returns None
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "images" in message:
                for i in range(0, len(message["images"]), NUM_IMAGES_PER_ROW):
                    cols = st.columns(NUM_IMAGES_PER_ROW)
                    for j in range(NUM_IMAGES_PER_ROW):
                        if i + j < len(message["images"]):
                            cols[j].image(message["images"][i + j], width=200)


st.set_page_config(page_title="Nùɖúɖú",
                   page_icon="",
                   layout="wide")

# Title
st.title("Nùɖúɖú")


with st.sidebar:
    st.title("Nùɖúɖú")
    st.subheader("Benin Food Chat")
    st.markdown(
        """Nùɖúɖú is a chatbot built for anyone interested in exploring and enjoying the rich culinary heritage of Benin. 
        It offers  speech to image  as well as text to image generation about the local food of Benin (Atassi, Amiwo, telibo wo)"""
    )
    uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'aac',"opus"])
    submit = st.button("Submit & Process")
    
    st.divider()
    st.markdown(
        """
        ---
        LinkedIn → [Abdel Tidjani](https://www.linkedin.com/in/abdelanlah-tidjani/)
        LinkedIn → [Abdel Tidjani](https://www.linkedin.com/in/abdelanlah-tidjani/)
        LinkedIn → [Abdel Tidjani](https://www.linkedin.com/in/abdelanlah-tidjani/)
        LinkedIn → [Abdel Tidjani](https://www.linkedin.com/in/abdelanlah-tidjani/)
        LinkedIn → [Abdel Tidjani](https://www.linkedin.com/in/abdelanlah-tidjani/)
        LinkedIn → [Abdel Tidjani](https://www.linkedin.com/in/abdelanlah-tidjani/)

        """
    )
# Information
with st.expander("Built for the Benin Multimodal AI Hackathon 2024"):
    st.markdown(
        """
        This project is a submission for the [Benin Multimodal AI Hackathon 2024](https://lablab.ai/event/benin-multimodal-ai-hackathon).
        
        Benin Food Chat uses 
        You can find the submission in this [GitHub repo]()
        """
    )
    st.subheader("Role")
    st.markdown(
        """
- Dish Visualization: Provide users with an authentic platform to unleash their creativity and showcase their culinary ideas by accurately generating images of local dishes through AI technology.

- Recipe Sharing: Provide users with authentic recipes for traditional Beninese dishes, complete with cooking tips and ingredient lists.

- Cultural Education: Educate users about the history and cultural significance of various Beninese foods, connecting culinary practices with local traditions and festivals.

- Restaurant Recommendations: Suggest local or international restaurants that serve Beninese cuisine, potentially integrating location-based services to direct users to nearby dining options.

- Language Integration: Help non-native speakers learn culinary-related terms and phrases in local languages such as Fon or Yoruba, enhancing their dining and cooking experiences.

 """
    )


col1, col2, col3 = st.columns([0.2, 0.5, 0.2])

# col2.image("./img/anim.gif")

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text: str):
    """Convert text to speech and return audio file."""
    engine.save_to_file(text, 'speech.mp3')
    engine.runAndWait()
    with open("speech.mp3", "rb") as audio_file:
        audio_data = audio_file.read()
    return audio_data



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.greetings = False

# Display chat messages from history on app rerun
display_chat_messages()

# Greet user
if not st.session_state.greetings:
    with st.chat_message("assistant"):
        intro = "Hey! I am Nùɖúɖú, your assistant for exploring and enjoying traditional Beninese dishes, Let's get started!"
        st.markdown(intro)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": intro})
        st.session_state.greetings = True

# Example prompts
example_prompts = [
    "Benin dish Amiwo",
    "Amiwo  kpo do xwévi",
    "Amiwo dish with chicken-leg",
]

example_prompts_help = [
    "Food photography",
    "Editorial Photography, Photography, Shot on 70mm lens, Depth of Field",
    "White Balance, 32k, Super-Resolution, white background",
]

button_cols = st.columns(3)
button_cols_2 = st.columns(3)

button_pressed = ""


if button_cols[0].button(example_prompts[0], help=example_prompts_help[0]):
    button_pressed = example_prompts[0]
elif button_cols[1].button(example_prompts[1], help=example_prompts_help[1]):
    button_pressed = example_prompts[1]
elif button_cols[2].button(example_prompts[2], help=example_prompts_help[2]):
    button_pressed = example_prompts[2]



# wav_audio_data = st_audiorec() # tadaaaa! yes, that's it! :D


if prompt := (st.chat_input("What dish are you looking for? Express your mind!") or button_pressed ):
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    

    if submit:
        st.audio(uploaded_file.read(), format='audio/wav')



    # prompt = prompt.replace('"', "").replace("'", "")


    # Placeholders for images and gallery
    generated_images_placeholder = st.empty()
    # gallery_placeholder = st.empty() # will be add later

    images = []
    if prompt != "":
        # query = prompt.strip().lower()
        with st.status('👩🏾‍🍳 Whipping up your words into art...', expanded=True) as status:
            st.write("⚙️ Model initiated")
            st.write("🙆‍♀️ Stand up and strecth in the meantime")
            try:
                
                input1=prompt+" benin dish recipe"
                response=get_gemini_response(input1)
                st.subheader("The Recipe is")
                for chunk in response:
                    print(st.write(chunk.text))
                    print("_"*80)
                
                # st.write(chat.history)

                # Only call the API if the "Submit" button was pressed
                if prompt is not None :
                    # Calling the replicate API to get the image
                    with generated_images_placeholder.container():
                        all_images = []  # List to store all generated images
                        output = replicate.run(
                            "abdeltid/foodlocalbenin:e0868ed242d6478a91aa7fc4dc92917f1856a60c6c4c708f83b0d8ea98dffac1",
                            input={
                                # "seed": 13,
                                "width": 512,
                                "height": 512,
                                "prompt": prompt,
                                "refine": "no_refiner",
                                "scheduler": "K_EULER",
                                "lora_scale": 0.6,
                                "num_outputs": 1,
                                "guidance_scale": 7.5,
                                "apply_watermark": True,
                                "high_noise_frac": 0.8,
                                "negative_prompt": "the absolute worst quality, distorted features",
                                "prompt_strength": 0.8,
                                "num_inference_steps": 50
                            }
                        )
                        print(output)
                        if output:
                            st.toast(
                                'Your image has been generated!', icon='😍')
                            # Save generated image to session state
                            st.session_state.generated_image = output

                            # Displaying the image
                            for image in st.session_state.generated_image:
                                with st.container():
                                    st.image(image, caption="Generated Image 🎈", use_column_width=False)
                    status.update(label="✅ Images generated!",state="complete", expanded=False)
                st.session_state.messages.append(
                {"role": "assistant", "content": response, "images": image}
            )
                st.experimental_rerun()
            except Exception as e:
                print(e)
                st.error(f'Encountered an error: {e}', icon="🚨")

    # If not submitted, chill here 🍹
    else:
        pass

        