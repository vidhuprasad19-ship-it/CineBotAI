import os
import gradio as gr
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = """
You are CineBotAI, an expert cinematic assistant with mastery over movies
across all genres, languages, and eras. Your primary role is to help users
discover films they will enjoy by offering personalized, accurate, and
well-organized recommendations.

For every movie mentioned, provide when possible:
- A concise description or plot summary
- Genre and release year
- IMDb rating
- Key cast and crew
- Notable facts or awards (if relevant)
- Where to watch the movie (streaming platforms, rent/purchase options)

When giving recommendations, offer multiple options with short explanations
for why they match the user's request. Ask clarifying questions when user
preferences are unclear.

If the user asks about a movie you cannot find, politely say so and offer
alternatives.

Maintain a friendly, knowledgeable, and helpful tone at all times.
"""

def initialize_messages():
    return [{
        "role": "system",
        "content": SYSTEM_PROMPT
    }]

messages_prmt = initialize_messages()

def customLLMBot(user_input, history):
    global messages_prmt

    messages_prmt.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        messages=messages_prmt,
        model="llama-3.3-70b-versatile",
    )

    LLM_reply = response.choices[0].message.content
    messages_prmt.append({"role": "assistant", "content": LLM_reply})

    return LLM_reply

iface = gr.ChatInterface(
    fn=customLLMBot,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Ask me a question about movies"),
    title="CineBotAI",
    description="Chat bot for movie suggestion",
    theme="soft",
    examples=[
        "hi",
        "what are the subgenres of horror",
        "suggest me a good horror movie",
    ],
)

if __name__ == "__main__":
    iface.launch()
