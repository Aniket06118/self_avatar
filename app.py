from openai import OpenAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os
import gradio as gr

load_dotenv(override=True)


class Me:

    def __init__(self):

        self.gemini = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        self.name = "Aniket Sharma"

        reader = PdfReader(
            r"aniket resume-updated.pdf"
        )

        self.linkedin = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text

        with open(
            r"summary.txt",
            "r",
            encoding="utf-8"
        ) as f:
            self.summary = f.read()

        self.system_prompt = f"""
You are acting as {self.name}. You are answering questions on {self.name}'s website, particularly questions related to {self.name}'s career, background, skills and experience.

Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible.

You are given a summary of {self.name}'s background and profile information which you can use to answer questions.

Be professional and engaging, as if talking to a potential employer, recruiter, collaborator, or client.

Keep answers short, crisp, and direct unless the user asks for more detail.

If you do not know the answer, clearly say that the information is not available in your profile.

## Summary:
{self.summary}

## Resume:
{self.linkedin}

With this context, please chat with the user, always staying in character as {self.name}.
"""

    def chat_msg(self, message, history):

        messages = (
            [{"role": "system", "content": self.system_prompt}]
            + history
            + [{"role": "user", "content": message}]
        )

        response = self.gemini.chat.completions.create(
            model="gemini-2.5-flash",
            messages=messages
        )

        return response.choices[0].message.content


if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat_msg).launch()