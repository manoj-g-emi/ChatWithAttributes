
from promptflow import tool
from openai import AzureOpenAI  
import pandas as pd
import os

from dotenv import load_dotenv
import json

@tool
def qna(is_env_ready: bool, prompt:str, question: str, grounded_context: list) -> str:
    load_dotenv()
    if is_env_ready:
        endpoint = os.getenv("ENDPOINT_URL", "https://emi-ts-llm-workshop-eus-oai-paygo.openai.azure.com/")
        api_key = os.getenv("OPENAI_API_KEY")

        client = AzureOpenAI(  
              api_key= api_key,
              azure_endpoint=endpoint,  
              api_version='2024-05-01-preview' 
          )
        
        response = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
            {"role": "system", "content": prompt },
            {"role": "user", "content": "Context: " + json.dumps(grounded_context) + "\n\n Query: " + question}
        ]
        )
        return response.choices[0].message.content
    else:
        return "Environment is not ready"


def read_csv_into_dataframe(csv_name):
   df = pd.read_csv(csv_name)
   return df