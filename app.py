import gradio
from groq import Groq
import os
client = Groq(api_key=os.environ["GROQ_API_KEY"])

def initialize_messages():
    return [{
  "role": "system",
  "content": "You are CineBotAI, an expert cinematic assistant with mastery over movies across all genres, languages, and eras. Your primary role is to help users discover films they will enjoy by offering personalized, accurate, and well-organized recommendations.\n\nFor every movie mentioned, provide:\n- A concise description or plot summary\n- Genre and release year\n- IMDb rating\n- Key cast and crew\n- Notable facts or awards (if relevant)\n- Where to watch the movie (streaming platforms, rent/purchase options)\n\nWhen giving recommendations, offer multiple options with short explanations for why they match the user's request. Ask clarifying questions when user preferences are unclear.\n\nIf the user asks about a movie you cannot find, politely say so and offer alternatives.\n\nMaintain a friendly, knowledgeable, and helpful tone at all times."
}
]
messages_prmt = initialize_messages()
print(messages_prmt)
def customLLMBot(user_input, history):
    global messages_prmt

    messages_prmt.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        messages=messages_prmt,
        model="llama-3.3-70b-versatile",
    )
    print(response)
    LLM_reply = response.choices[0].message.content
    messages_prmt.append({"role": "assistant", "content": LLM_reply})

    return LLM_reply
iface = gradio.ChatInterface(customLLMBot,
                     chatbot=gradio.Chatbot(height=300),
                     textbox=gradio.Textbox(placeholder="Ask me a question about movies"),
                     title="CineBotAI",
                     description="Chat bot for movie suggestion",
                     theme="soft",
                     examples=["hi","what are the subgenres of horror", "suggest me a good horror movie"]
                     )
