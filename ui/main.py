import urllib.request
import json
import os
import ssl
from dotenv import load_dotenv
import streamlit as st

st.title('Attributes by Country - 2021/2022')
def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
load_dotenv()

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

url = 'https://attributesy20212022chat.westeurope.inference.ml.azure.com/score'
# Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
api_key = os.getenv("API_KEY")
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")


headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

user_input = st.text_input(label="Question", key="text_input")
if user_input:
    st.session_state['chat_history'].append({"role": "user", "message": user_input})
   
    body = str.encode(json.dumps({"question":user_input}))
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
    # Append API response to chat history
        result = response.read()
        parsed_data = json.loads(result)
        st.session_state['chat_history'].append({"role": "bot", "message": parsed_data.get('answer')})
        
    # Clear input after submission
        # Display chat history
        for chat in st.session_state['chat_history']:
            if chat["role"] == "user":
                st.write(f"**You:** {chat['message']}")
            else:
                st.write(f"**Bot:** {chat['message']}")
        
        
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
else:
    st.write("Please enter a question to start the conversation.")
