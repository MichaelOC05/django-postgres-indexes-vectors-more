import os

import pandasai as pai
from pandasai_litellm.litellm import LiteLLM

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# from documentation not from tutorial as the package has been updated
llm = LiteLLM(model="gpt-4.1-mini", api_key=OPENAI_API_KEY)

pai.config.set({"llm": llm})

df = pai.read_csv("titanic_data.csv")

df.head()

response = df.chat("What sex was most likely to have survived?")

print(response)

males = df[df["Sex"] == "male"]

males["Survived"].sum() / len(males)

females = df[df["Sex"] == "female"]

females["Survived"].sum() / len(females)

response_1 = df.chat("What can you tell us about the class of the passenger - is there a correlation wiht survival rate?")

print(response_1)

response_2 = df.chat("Plot the histogram of survivorship of the sexes")

print(response_2)

response_3 = df.chat("Create a histogram plot based on the fare values")
print(response_3)