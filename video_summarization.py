import os
import google.generativeai as genai
import time  

GoogleApi_key = os.environ.get("GOOGLE_API_KEY")
print(GoogleApi_key)

#video_file_name = "VBRamesh.mp4" # Please set your video file with the path.
video_file_name = "/Users/ravi/projects/Gemini-Grounding-demo/testing-9sec.mp4" # Please set your video file with the path.
display_name = "sampleDisplayName" # Please set the display name of the uploaded file on Gemini. The file is searched from the file list using this value.

#genai.configure(api_key=GoogleApi_key)
genai.configure(api_key=GoogleApi_key)

# Get file list in Gemini
fileList = genai.list_files(page_size=100)

# Check uploaded file.
video_file = next((f for f in fileList if f.display_name == display_name), None)
if video_file is None:
    print(f"Uploading file...")
    video_file = genai.upload_file(path=video_file_name, display_name=display_name, resumable=True)
    print(f"Completed upload: {video_file.uri}")
else:
    print(f"File URI: {video_file.uri}")

# Check the state of the uploaded file.
while video_file.state.name == "PROCESSING":
    print(".", end="")
    time.sleep(10)
    video_file = genai.get_file(video_file.name)

if video_file.state.name == "FAILED":
    raise ValueError(video_file.state.name)

# Generate content using the uploaded file.
prompt = "Describe this video."
model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
# model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
print("Making LLM inference request...")
response = model.generate_content([video_file, prompt], request_options={"timeout": 600})
print(response.text)
genai.delete_file(video_file.name)
