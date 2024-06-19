from openai import OpenAI

# init client and connect to localhost server
client = OpenAI(
    api_key="1234",
    base_url="http://localhost:8050/v1" # change the default port if needed
)

stream = True

# call API
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "What is meaning of life",
        }
    ],
    model="llama3-70b-8192",
    stream=stream
)

if stream == False:
    print(chat_completion.choices[0].message.content)

if stream == True:
    for chunk in chat_completion:
        print(chunk.choices[0].delta.content, end = "", flush=True)
