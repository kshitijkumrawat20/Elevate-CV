from ibm_watsonx_ai import APIClient
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API Key and Project ID
api_key = "EYK-AZiDM5ZQTmJ3Spze6zH1qiTKBdj7lql0varU7KVk"
project_id = "d65f53f9-4250-4a2a-b9ab-0ff374b1f713"
cred = ".json/apikey.json"

authenticator = IAMAuthenticator(apikey=api_key)
client = APIClient(credentials=authenticator, project_id=project_id)

prompt = "Please list one IBM Research laboratory located in the United States. You should only output its name and location."
response = client.generate_text(
    model_id='ibm/granite-3-8b-instruct',
    input=prompt,
    parameters={
        'decoding_method': 'greedy',
        'max_new_tokens': 8192
    }
).result
print(response['generated_text'])
