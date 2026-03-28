import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
load_dotenv()
import pandasai as pai
from pandasai_litellm.litellm import LiteLLM

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# from documentation not from tutorial as the package has been updated
llm = LiteLLM(model="gpt-4.1-mini", api_key=OPENAI_API_KEY)
pai.config.set({"llm": llm})


st.title("Prompt-driven analysis of PandasAi")

uploaded_file = st.file_uploader("Upload a CSV file for analysis", type=["csv"])

if uploaded_file is not None:
    df = pai.read_csv(uploaded_file)
    st.write(df.head(3))

    prompt = st.text_area("Enter your prompt:")

    if st.button("Generate"):
        if prompt:
            response = df.chat(prompt)

            st.write(response)
