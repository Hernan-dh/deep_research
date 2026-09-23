import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)

UI_TEXT = {
    "English": {
        "language": "Language / Idioma",
        "prompt": "What topic would you like to research?",
        "run": "Run",
        "report": "Report",
    },
    "Español": {
        "language": "Idioma / Language",
        "prompt": "¿Qué tema querés investigar?",
        "run": "Investigar",
        "report": "Informe",
    },
}


def initialize_language(browser_language: str):
    language = "Español" if (browser_language or "").lower().startswith("es") else "English"
    return update_language(language, include_language=True)


def update_language(language: str, include_language: bool = False):
    language = language if language in UI_TEXT else "English"
    text = UI_TEXT[language]
    updates = (
        gr.update(value=language),
        gr.update(label=text["prompt"]),
        gr.update(value=text["run"]),
        gr.update(value=f"## {text['report']}"),
    )
    return updates if include_language else updates[1:]


async def run(query: str):
    async for status_update in ResearchManager().run(query):
        yield status_update


with gr.Blocks() as ui:
    language = gr.Dropdown(
        choices=["Español", "English"], value="English", show_label=False,
        label="Language / Idioma", interactive=True,
    )
    query_textbox = gr.Textbox(label=UI_TEXT["English"]["prompt"])
    run_button = gr.Button(UI_TEXT["English"]["run"], variant="primary")
    report = gr.Markdown(f"## {UI_TEXT['English']['report']}")
    
    run_button.click(run, inputs=query_textbox, outputs=report)
    query_textbox.submit(run, inputs=query_textbox, outputs=report)
    language.change(
        update_language,
        inputs=language,
        outputs=[query_textbox, run_button, report],
        js="(language) => { if (window.__deepResearchSimpleAutoLanguage) delete window.__deepResearchSimpleAutoLanguage; else try { localStorage.setItem('deep-research-simple-language', language); } catch {} return language; }",
    )
    browser_language = gr.Textbox(visible=False)
    ui.load(
        initialize_language,
        inputs=browser_language,
        outputs=[language, query_textbox, run_button, report],
        js="() => { try { const saved = localStorage.getItem('deep-research-simple-language'); if (saved === 'Español' || saved === 'English') return saved; } catch {} window.__deepResearchSimpleAutoLanguage = true; return navigator.language || ''; }",
    )

ui.launch(theme=gr.themes.Default(primary_hue="sky"))
