from langchain_ibm import WatsonxLLM
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API Key and Project ID
api_key = os.getenv("WATSONX_APIKEY")
project_id = os.getenv("PROJECT_ID")

# Explicitly set API key in environment variables
os.environ["WATSONX_APIKEY"] = api_key


# Define model parameters
parameters = {
    "temperature": 0.7,
    "top_p": 0.7,
    "top_k": 50,
    "max_new_tokens": 8192,  # Increase token limit for longer responses
    "min_new_tokens": 0,    # Set minimum tokens to ensure complete responses
    "repetition_penalty": 1.1,
    "stop_sequences": ["\n\n\n"]  # Stop sequence to properly end responses
}

# Function to connect to Watsonx LLM
def connect_llm():
    try:
        watsonx_llm = WatsonxLLM(
            model_id="ibm/granite-3-8b-instruct",
            # model_id="ibm/granite-20b-multilingual",
            # model_id="ibm/granite-34b-code-instruct",
            
            # model_id="meta-llama/llama-3-3-70b-instruct",
            url="https://us-south.ml.cloud.ibm.com",
            project_id=project_id,
            params=parameters,
        )
        print("Connected to WatsonX!")
        return watsonx_llm
    except Exception as e:
        print("Error connecting to WatsonX:", e)

# # Call function
# connect_llm()
