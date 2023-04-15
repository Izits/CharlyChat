import json
import streamlit as st
from streamlit_chat import message
import openai
from config.config import open_api_key

openai.api_key = open_api_key

# Load JSON data
with open('data/whatName.json') as f:
    questions = json.load(f)

# OpenAI code
def openai_create(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        n=1,
        stop=None
    )
    return response.choices[0].text


def charly_chat(input, history):
    history = history or []
    s = list(sum(history, ()))
    print(s)
    s.append(input)
    inp = ' '.join(s)
    for q in questions:
        if input.lower() == q["question"].lower():
            output = "Mi nombre es Charly. ¿En qué más puedo ayudarte?"
            break
    else:
        output = openai_create(inp)
    history.append((input, output))
    return history, history

# Streamlit App
st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto",
    page_title="Charly",
    page_icon="🤖"
)

st.header("Charly Demo")

history_input = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text 

user_input = get_text()

if user_input:
    output = charly_chat(user_input, history_input)
    history_input.append([user_input, output])
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output[0])

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
