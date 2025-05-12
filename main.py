import streamlit as st
import base64
from openai import OpenAI
import os


#loading the openAI key from the .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#UI for the app
st.title("Welcome to Code Generator App!")
st.write("A place where you can generate the frontend UI code by just uploading the screenshot of a webpage.")
st.divider()


#Upload function to get the file from the user
file=st.file_uploader("Upload a webpage screenshot",type=["jpg", "jpeg", "png"])


if st.button("Generate the code"):
    if file:
        # Convert image to base64
        image_bytes = file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        #prompt for gpt model 

        prompt='''

        You are a frontend expert. Analyze the uploaded image of a web UI and generate the corresponding React JSX and CSS code.
Output only the code in clearly labeled code blocks and focus on layout/structure over exact pixel perfection.

'''

        with st.spinner("Generating the code......."):
            #creating session and sending request to openAI
            response=client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role":"system","content":"You are a React frontend developer."},
                    {"role":"user","content":[
                        {"type":"text","text":prompt},
                         {"type":"image_url","image_url":f"data:image/jpeg;base64,{base64_image}"}
                         
                    ]}
                ],
                max_tokens=2000
            )
        result = response.choices[0].message.content
        st.success("✅ React code generated:")
        st.code(result)
    else:
        st.warning("Please upload an image first.")






