EXAMPLES = [
    "Most popular AI Agent frameworks in 2026",
    "Most commercially successful Agentic AI implementations in 2026",
    "How are companies using AI agents in customer support in 2026?",
    "Which AI coding agents offer the best value for small development teams?",
    "What are the main security risks of autonomous AI agents?",
    "Compare OpenAI Agents SDK, LangGraph, CrewAI, and Google ADK",
    "What industries are adopting agentic AI most rapidly in 2026?",
    "What are the practical differences between MCP and traditional APIs?",
    "Which open-source AI agent frameworks have the strongest communities?",
    "What evidence exists that four-day workweeks improve productivity?",
    "Which cities are leading the transition to renewable energy?",
]

SPANISH_EXAMPLES = [
    "Frameworks de agentes de IA más populares en 2026",
    "Implementaciones comerciales de IA agéntica más exitosas en 2026",
    "¿Cómo usan las empresas agentes de IA en atención al cliente en 2026?",
    "¿Qué agentes de programación ofrecen más valor para equipos pequeños?",
    "¿Cuáles son los principales riesgos de seguridad de los agentes autónomos?",
    "Compará OpenAI Agents SDK, LangGraph, CrewAI y Google ADK",
    "¿Qué industrias están adoptando IA agéntica más rápidamente en 2026?",
    "¿Cuáles son las diferencias prácticas entre MCP y las API tradicionales?",
    "¿Qué frameworks open source de agentes de IA tienen las comunidades más sólidas?",
    "¿Qué evidencia existe de que la semana laboral de cuatro días mejora la productividad?",
    "¿Qué ciudades lideran la transición hacia la energía renovable?",
]

HEADER_HTML = """
<div class="dr-brand">
    <div class="dr-mark">
        <span class="dr-bar dr-bar-1"></span>
        <span class="dr-bar dr-bar-2"></span>
        <span class="dr-bar dr-bar-3"></span>
    </div>
    <div class="dr-titles">
        <h1>Deep<span class="dr-sep">/</span>Research</h1>
        <p id="dr-subtitle">Multi-search web investigation</p>
    </div>
</div>
"""

CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Manrope:wght@400;500;600;700&display=swap');

.gradio-container {
    --dr-bg: #fafaf7;
    --dr-surface: #ffffff;
    --dr-line: #0c0c0d;
    --dr-line-soft: #e1e1da;
    --dr-text: #0c0c0d;
    --dr-muted: #6f6f72;
    --dr-amber: #ecad0a;
    --dr-blue: #209dd7;
    --dr-purple: #753991;

    width: 100% !important;
    max-width: 1080px !important;
    min-width: 0 !important;
    margin: 0 auto !important;
    padding: 2.5rem 2rem 4rem !important;
    background: var(--dr-bg) !important;
    color: var(--dr-text) !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif !important;
}

.gradio-container *,
.gradio-container .main,
.gradio-container .contain,
.gradio-container .wrap {
    min-width: 0;
}

.gradio-container .main,
.gradio-container .contain,
.gradio-container .wrap {
    width: 100% !important;
    max-width: 100% !important;
}

.gradio-container.dark,
.dark .gradio-container,
body.dark .gradio-container,
html.dark .gradio-container {
    --dr-bg: #0b0b0c;
    --dr-surface: #161618;
    --dr-line: #f1f1ec;
    --dr-line-soft: #2a2a2d;
    --dr-text: #f1f1ec;
    --dr-muted: #8a8a8e;
}

body { background: var(--dr-bg, #fafaf7); }

/* === HEADER === */
.dr-brand {
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: center;
    gap: 1.4rem;
    padding-bottom: 1.25rem;
    border-bottom: 3px solid var(--dr-line);
    margin-bottom: 2.5rem;
}

.dr-mark {
    display: flex;
    flex-direction: column;
    gap: 5px;
    width: 38px;
}

.dr-bar { height: 7px; display: block; }
.dr-bar-1 { background: var(--dr-amber);  width: 100%; }
.dr-bar-2 { background: var(--dr-blue);   width: 70%;  }
.dr-bar-3 { background: var(--dr-purple); width: 45%;  }

.dr-titles h1 {
    font-size: clamp(1.8rem, 4vw, 2.6rem);
    font-weight: 900;
    letter-spacing: -0.045em;
    margin: 0;
    line-height: 0.95;
    text-transform: uppercase;
    color: var(--dr-text);
}

.dr-sep {
    color: var(--dr-amber);
    font-weight: 300;
    margin: 0 0.04em;
}

.dr-titles p {
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace;
    font-size: 0.7rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin: 0.55rem 0 0;
    color: var(--dr-muted);
}

/* === QUERY ROW === */
.dr-query-row {
    gap: 0 !important;
    align-items: stretch !important;
}

#dr-query, #dr-query > div, #dr-query .wrap, #dr-query .form, #dr-query .block {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    border-radius: 0 !important;
}

#dr-query textarea, #dr-query input {
    background: var(--dr-surface) !important;
    color: var(--dr-text) !important;
    border: 2px solid var(--dr-line) !important;
    border-radius: 0 !important;
    padding: 1.05rem 1.2rem !important;
    font-size: 1.05rem !important;
    font-family: inherit !important;
    box-shadow: none !important;
    line-height: 1.45 !important;
    resize: none !important;
    min-height: 56px !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}

#dr-query textarea:focus, #dr-query input:focus {
    outline: none !important;
    border-color: var(--dr-blue) !important;
    box-shadow: 6px 6px 0 0 var(--dr-blue) !important;
}

#dr-query textarea::placeholder, #dr-query input::placeholder {
    color: var(--dr-muted) !important;
    opacity: 1 !important;
}

#dr-run {
    background: var(--dr-amber) !important;
    color: #0c0c0d !important;
    border: 2px solid var(--dr-line) !important;
    border-left: none !important;
    border-radius: 0 !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
    font-size: 0.85rem !important;
    box-shadow: none !important;
    transition: background 0.15s, color 0.15s, transform 0.08s !important;
    min-width: 150px !important;
    padding: 1rem 1.5rem !important;
}

#dr-run:hover {
    background: var(--dr-purple) !important;
    color: #ffffff !important;
}

#dr-run:active { transform: translate(2px, 2px) !important; }

/* === EXAMPLES === */
.dr-examples-label {
    font-family: ui-monospace, SFMono-Regular, monospace;
    font-size: 0.65rem;
    letter-spacing: 0.28em;
    color: var(--dr-muted);
    text-transform: uppercase;
    margin: 2rem 0 0.85rem 0;
    display: flex;
    align-items: center;
    gap: 0.85rem;
}

.dr-examples-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--dr-line-soft);
}

#dr-examples, #dr-examples > div, #dr-examples .wrap, #dr-examples .block {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
}

#dr-examples label, #dr-examples .label-wrap, #dr-examples > div > .label-wrap {
    display: none !important;
}

#dr-examples table {
    border-collapse: separate !important;
    border-spacing: 0 !important;
    width: auto !important;
    background: transparent !important;
    border: none !important;
}

#dr-examples thead { display: none !important; }

#dr-examples tbody { background: transparent !important; }

#dr-examples tr {
    background: transparent !important;
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    border: none !important;
}

#dr-examples td, #dr-examples button {
    background: var(--dr-surface) !important;
    border: 1.5px solid var(--dr-line-soft) !important;
    padding: 0.7rem 1.05rem !important;
    cursor: pointer !important;
    transition: border-color 0.15s, color 0.15s, transform 0.1s !important;
    font-size: 0.9rem !important;
    color: var(--dr-text) !important;
    border-radius: 0 !important;
    margin: 0 !important;
    text-align: left !important;
    box-shadow: none !important;
}

#dr-examples td:hover, #dr-examples button:hover {
    border-color: var(--dr-purple) !important;
    color: var(--dr-purple) !important;
    transform: translateY(-1px);
}

/* === REPORT === */
#dr-report {
    margin-top: 2.5rem !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: var(--dr-text) !important;
    min-height: 40px;
}

#dr-report > div, #dr-report .prose {
    background: transparent !important;
    color: var(--dr-text) !important;
}

#dr-report:not(:empty) {
    border-top: 1px solid var(--dr-line-soft) !important;
    padding-top: 1.75rem !important;
}

#dr-report h1 {
    font-size: 1.85rem;
    font-weight: 900;
    color: var(--dr-blue);
    border-bottom: 2px solid var(--dr-line);
    padding-bottom: 0.45rem;
    margin: 1.5rem 0 1rem;
    letter-spacing: -0.025em;
}

#dr-report h2 {
    font-size: 1.35rem;
    color: var(--dr-purple);
    font-weight: 800;
    margin-top: 1.75rem;
    letter-spacing: -0.015em;
}

#dr-report h3 {
    font-size: 1.1rem;
    color: var(--dr-text);
    font-weight: 800;
    margin-top: 1.5rem;
}

#dr-report p { line-height: 1.7; }

#dr-report a {
    color: var(--dr-blue);
    text-decoration: underline;
    text-decoration-thickness: 2px;
    text-underline-offset: 3px;
}

#dr-report a:hover { color: var(--dr-amber); }

#dr-report code {
    background: var(--dr-surface);
    border: 1px solid var(--dr-line-soft);
    padding: 0.1rem 0.4rem;
    font-size: 0.92em;
    border-radius: 0;
}

#dr-report pre {
    background: var(--dr-surface);
    border: 1.5px solid var(--dr-line-soft);
    border-radius: 0;
    padding: 1rem 1.25rem;
}

#dr-report blockquote {
    border-left: none !important;
    background: var(--dr-surface);
    padding: 1rem 1.25rem;
    margin: 1rem 0;
    color: var(--dr-text);
}

#dr-report ul, #dr-report ol { padding-left: 1.5rem; }
#dr-report li { margin: 0.3rem 0; line-height: 1.6; }

#dr-report table {
    border-collapse: collapse;
    border: 1.5px solid var(--dr-line);
}

#dr-report th, #dr-report td {
    border: 1px solid var(--dr-line-soft);
    padding: 0.5rem 0.85rem;
    text-align: left;
}

#dr-report th {
    background: var(--dr-surface);
    font-weight: 800;
    color: var(--dr-blue);
}

/* === AGENTIC TWIN VISUAL SYSTEM === */
.gradio-container {
    --dr-bg: #111412;
    --dr-surface: #181c19;
    --dr-line: #343a35;
    --dr-line-soft: #343a35;
    --dr-text: #e9e9e3;
    --dr-muted: #909690;
    --dr-acid: #c7ff37;
    --dr-orange: #ff6947;
    max-width: 920px !important;
    padding: 34px 24px 48px !important;
    background: transparent !important;
    font-family: "Manrope", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}

html, body, gradio-app { background: var(--dr-bg) !important; color-scheme: dark; }
body {
    background-image: linear-gradient(rgb(255 255 255 / 2.5%) 1px, transparent 1px), linear-gradient(90deg, rgb(255 255 255 / 2.5%) 1px, transparent 1px) !important;
    background-size: 42px 42px !important;
}

#title-row {
    align-items: center !important;
    flex-wrap: nowrap !important;
    gap: 28px !important;
    margin-bottom: 22px !important;
    padding-bottom: 1.25rem !important;
    border-bottom: 3px solid var(--dr-text) !important;
}

.dr-brand { margin: 0; padding: 0; border: 0; }
#header-copy { gap: 0 !important; }
#language-control { width: 170px !important; min-width: 170px !important; max-width: 170px !important; flex: 0 0 170px !important; gap: 5px !important; margin-left: auto !important; }
#language-label, #language-selector { width: 100% !important; margin: 0 !important; padding: 0 !important; }
#language-label p { margin: 0 !important; color: var(--dr-muted) !important; font: 400 9px ui-monospace, monospace !important; letter-spacing: .08em; text-transform: uppercase; }
#language-selector input { height: 34px !important; min-height: 34px !important; padding: 5px 9px !important; font: 400 11px ui-monospace, monospace !important; }
#language-selector button { width: 34px !important; height: 34px !important; min-height: 34px !important; padding: 0 !important; }

.block, .form { background: transparent !important; box-shadow: none !important; }
.chatbot, .chatbot *, .block, .form, button, input, textarea { border-radius: 0 !important; }
.chatbot > .block-label, .chatbot > label, .chatbot .label-wrap, .chatbot .block-label, .chatbot > .label-container { display: none !important; }

.chatbot, .chatbot.block {
    height: 470px !important;
    min-height: 470px !important;
    border: 1px solid var(--dr-line) !important;
    background: rgb(24 28 25 / 94%) !important;
    box-shadow: 18px 18px 0 rgb(0 0 0 / 18%) !important;
}

.message-row, .message-row > div, .message-row .role, .message-wrap, .bubble-wrap { border: 0 !important; background: transparent !important; box-shadow: none !important; }
.message-row .message, .message-row .message-bubble, .message-row .bubble { padding: 10px 13px !important; border: 0 !important; box-shadow: none !important; font-size: 14px !important; line-height: 1.6 !important; }
.message-row.user-row .message, .message-row.user-row .message-bubble, .message-row.user-row .bubble, .message-row[data-role='user'] .message, .message-row[data-role='user'] .message-bubble { background: var(--dr-acid) !important; color: var(--dr-bg) !important; }
.message-row.bot-row .message, .message-row.bot-row .message-bubble, .message-row.bot-row .bubble, .message-row[data-role='assistant'] .message, .message-row[data-role='assistant'] .message-bubble, .message-row[data-role='assistant'] .bubble { border-left: 2px solid var(--dr-orange) !important; background: #202522 !important; color: var(--dr-text) !important; }
.message-row .message a, .message-row .message-bubble a { color: var(--dr-acid) !important; text-decoration: underline; text-underline-offset: 3px; }

textarea, input[type='text'] { min-height: 50px !important; padding: 13px 14px !important; border: 1px solid var(--dr-line) !important; background: var(--dr-surface) !important; color: var(--dr-text) !important; font-size: 14px !important; }
textarea:focus, input[type='text']:focus { border-color: var(--dr-acid) !important; outline: none !important; box-shadow: 0 0 0 1px var(--dr-acid) !important; }

button { min-height: 50px !important; border: 1px solid var(--dr-line) !important; background: var(--dr-surface) !important; color: var(--dr-text) !important; border-radius: 0 !important; }
button:hover { border-color: var(--dr-acid) !important; color: var(--dr-acid) !important; }
button.primary, button[variant='primary'], button.submit, button.submit-button, .submit-button, button.lg.primary { border-color: var(--dr-acid) !important; background: var(--dr-acid) !important; color: var(--dr-bg) !important; }
.icon-button, .chatbot .icon-button { min-height: 0 !important; padding: 4px !important; border: 0 !important; background: transparent !important; color: var(--dr-muted) !important; }

footer { display: none !important; }

@media (max-width: 700px) {
    .gradio-container { padding: 1.5rem 1rem 3rem !important; }
    #title-row { align-items: flex-start !important; flex-direction: column !important; gap: 16px !important; }
    #language-control { width: 100% !important; max-width: 170px !important; margin-left: 0 !important; }
    .dr-query-row { flex-direction: column !important; }
    #dr-run {
        border-left: 2px solid var(--dr-line) !important;
        border-top: none !important;
        width: 100% !important;
    }
}
"""

JS = """
() => {
    const focus = () => {
        const el = document.querySelector("#dr-query textarea, #dr-query input");
        if (el) { el.focus(); return true; }
        return false;
    };
    if (!focus()) {
        let tries = 0;
        const i = setInterval(() => {
            if (focus() || ++tries > 20) clearInterval(i);
        }, 100);
    }
}
"""
