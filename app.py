import random
import traceback

import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager
from styles import CSS, JS, EXAMPLES, HEADER_HTML

load_dotenv(override=True)

SUGGESTED_EXAMPLES = random.sample(EXAMPLES, k=3)


async def run(query: str, _history):
    try:
        async for status_update in ResearchManager().run(query):
            yield status_update
    except Exception:
        traceback.print_exc()
        yield (
            "I couldn't complete this research request. Please try again; "
            "if the problem continues, check the server log for provider details."
        )


with gr.Blocks(title="Deep Research") as ui:
    gr.HTML(HEADER_HTML)
    gr.ChatInterface(
        fn=run,
        examples=SUGGESTED_EXAMPLES,
        chatbot=gr.Chatbot(elem_id="dr-chat", height=600),
        textbox=gr.Textbox(
            placeholder="Ask a research question...",
            submit_btn="Investigate",
        ),
        flagging_mode="never",
    )


if __name__ == "__main__":
    ui.launch(css=CSS, js=JS, theme=gr.themes.Base())
