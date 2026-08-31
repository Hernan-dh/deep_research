import random
import traceback
import os

import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager
from styles import CSS, JS, EXAMPLES, HEADER_HTML, SPANISH_EXAMPLES

load_dotenv(override=True)

SUGGESTED_INDICES = random.sample(range(len(EXAMPLES)), k=3)


def suggested_examples(language: str) -> list[list[str]]:
    source = SPANISH_EXAMPLES if language == "Español" else EXAMPLES
    return [[source[index]] for index in SUGGESTED_INDICES]


def localized_ui(language: str):
    subtitle = "Investigación web con múltiples búsquedas" if language == "Español" else "Multi-search web investigation"
    header = HEADER_HTML.replace("Multi-search web investigation", subtitle)
    return header, gr.Group(visible=language == "English"), gr.Group(visible=language == "Español")


async def run(query: str, _history, language: str):
    try:
        async for status_update in ResearchManager().run(query, language):
            yield status_update
    except Exception:
        traceback.print_exc()
        if language == "Español":
            yield "No pude completar la investigación. Intentá nuevamente o revisá el log del servidor."
        else:
            yield "I couldn't complete this research request. Please try again or check the server log."


async def run_english(query: str, history):
    async for update in run(query, history, "English"):
        yield update


async def run_spanish(query: str, history):
    async for update in run(query, history, "Español"):
        yield update


with gr.Blocks(title="Deep Research") as ui:
    with gr.Row(elem_id="title-row"):
        with gr.Column(scale=1, min_width=0, elem_id="header-copy"):
            header = gr.HTML(HEADER_HTML)
        with gr.Column(scale=0, min_width=180, elem_id="language-control"):
            gr.Markdown("Language / Idioma:", elem_id="language-label")
            language = gr.Dropdown(
                choices=["English", "Español"],
                value="English",
                show_label=False,
                container=False,
                interactive=True,
                scale=0,
                min_width=180,
                elem_id="language-selector",
            )
    with gr.Group(visible=True) as english_chat:
        gr.ChatInterface(
            fn=run_english,
            examples=[item[0] for item in suggested_examples("English")],
            chatbot=gr.Chatbot(elem_id="dr-chat-en", height=470),
            textbox=gr.Textbox(
                placeholder="Ask a research question...",
                submit_btn="Investigate",
            ),
            flagging_mode="never",
        )
    with gr.Group(visible=False) as spanish_chat:
        gr.ChatInterface(
            fn=run_spanish,
            examples=[item[0] for item in suggested_examples("Español")],
            chatbot=gr.Chatbot(elem_id="dr-chat-es", height=470),
            textbox=gr.Textbox(
                placeholder="Hacé una pregunta de investigación...",
                submit_btn="Investigar",
            ),
            flagging_mode="never",
        )
    language.change(
        fn=localized_ui,
        inputs=language,
        outputs=[header, english_chat, spanish_chat],
    )
    detect_language = ui.load(
        fn=None,
        outputs=language,
        js="() => navigator.language.toLowerCase().startsWith('es') ? 'Español' : 'English'",
    )
    detect_language.then(
        fn=localized_ui,
        inputs=language,
        outputs=[header, english_chat, spanish_chat],
    )


if __name__ == "__main__":
    ui.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", "7860")),
        css=CSS,
        js=JS,
        theme=gr.themes.Base(),
    )
