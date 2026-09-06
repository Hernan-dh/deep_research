import random
import traceback
import os

import gradio as gr
from report_export import download_controls, empty_download
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
    initial_status = "**Research Planner** está analizando la consulta y preparando un plan estructurado de búsquedas web." if language == "Espa\u00f1ol" else "**Research Planner** is analyzing the question and preparing a structured web-search plan."
    yield initial_status, None, empty_download()
    try:
        report = None
        async for status_update in ResearchManager().run(query, language):
            report = status_update
            yield status_update, None, empty_download()
        if report:
            yield report, report, empty_download()
    except Exception:
        traceback.print_exc()
        error = "No pude completar la investigaci\u00f3n. Intent\u00e1 nuevamente." if language == "Espa\u00f1ol" else "I couldn't complete this research request. Please try again."
        yield error, None, empty_download()


async def run_english(query: str, history):
    async for update in run(query, history, "English"):
        yield update


async def run_spanish(query: str, history):
    async for update in run(query, history, "Español"):
        yield update


with gr.Blocks(title="Deep Research", delete_cache=(3600, 86400)) as ui:
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
        english_chatbot = gr.Chatbot(elem_id="dr-chat-en", height=470)
        english_report, english_download = download_controls("English")
        gr.ChatInterface(
            fn=run_english,
            show_progress="hidden",
            examples=[item[0] for item in suggested_examples("English")],
            chatbot=english_chatbot,
            additional_outputs=[english_report, english_download],
            textbox=gr.Textbox(
                placeholder="Ask a research question...",
                submit_btn="Investigate",
            ),
            flagging_mode="never",
        )
        english_chatbot.clear(lambda: (None, empty_download()), outputs=[english_report, english_download], queue=False)
    with gr.Group(visible=False) as spanish_chat:
        spanish_chatbot = gr.Chatbot(elem_id="dr-chat-es", height=470)
        spanish_report, spanish_download = download_controls("Español")
        gr.ChatInterface(
            fn=run_spanish,
            show_progress="hidden",
            examples=[item[0] for item in suggested_examples("Español")],
            chatbot=spanish_chatbot,
            additional_outputs=[spanish_report, spanish_download],
            textbox=gr.Textbox(
                placeholder="Hacé una pregunta de investigación...",
                submit_btn="Investigar",
            ),
            flagging_mode="never",
        )
        spanish_chatbot.clear(lambda: (None, empty_download()), outputs=[spanish_report, spanish_download], queue=False)
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
