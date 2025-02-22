from langchain_ibm import WatsonxLLM
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API Key and Project ID
api_key = os.getenv("WATSONX_APIKEY")

# Explicitly set API key in environment variables
os.environ["WATSONX_APIKEY"] = api_key

# Define model parameters
parameters = {
    "decoding_method": "sample",
    "max_new_tokens": 100,
    "min_new_tokens": 1,
    "temperature": 0.5,
    "top_k": 50,
    "top_p": 1,
}

# Function to connect to Watsonx LLM
def connect_llm():
    try:
        watsonx_llm = WatsonxLLM(
            model_id="ibm/granite-13b-instruct-v2",
            url="https://us-south.ml.cloud.ibm.com",
            project_id="4addd33f-df9c-4443-aa13-c4bb4d972357",
            params=parameters,
        )
        print("Connected to WatsonX!")
        print(watsonx_llm.invoke("Hi!"))
        return watsonx_llm
    except Exception as e:
        print("Error connecting to WatsonX:", e)

# Call function
connect_llm()
