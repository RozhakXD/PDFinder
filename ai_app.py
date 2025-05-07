import streamlit as st
import dashscope
from dashscope import Generation

class AIModelHandler:
    """Class untuk mengelola model AI dengan interaksi API"""
    _instance = None
    SUPPORTED_MODELS = {
        'qwen-turbo': 'Qwen Turbo',
        'qwen-plus': 'Qwen Plus',
        'qwen-max': 'Qwen Max',
        'qwen2.5-32b-instruct': 'Qwen 1.8B Chat',
        'qwen2.5-72b-instruct': 'Qwen2.5-72B-Instruct'
    }

    def __new__(cls, api_key):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(api_key)
        return cls._instance

    def _initialize(self, api_key):
        """Inisialisasi konfigurasi API"""
        dashscope.api_key = api_key
        dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

    @classmethod
    def get_available_models(cls):
        """Mengembalikan daftar model yang tersedia"""
        return list(cls.SUPPORTED_MODELS.keys())

    @staticmethod
    def generate_response(model, messages):
        """Generate response dari model AI"""
        try:
            response = Generation.call(
                model=model,
                messages=messages,
                result_format='message'
            )
            return response.output.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"API Error: {str(e)}")

class ChatAppUI:
    """Class untuk mengelola antarmuka pengguna Streamlit"""

    def __init__(self):
        self._setup_ui()
        self.api_key = 'Your API Key!'
        self.model_handler = AIModelHandler(self.api_key)

    def _setup_ui(self):
        """Mengatur tampilan antarmuka pengguna"""
        st.set_page_config(page_title="🤖 AI Chat Assistant", layout="wide")
        st.title("🤖 AI Chat Assistant")
        st.markdown("""
            <style>
                html, body, .stTextInput input, .stSelectbox select {
                    color: var(--text-color) !important;
                }

                .stButton>button {
                    transition: all 0.3s ease;
                }

                .stButton>button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                }

                .stSelectbox [data-baseweb="select"] {
                    border-radius: 20px !important;
                }
            </style>
        """, unsafe_allow_html=True)

    def _create_model_selector(self):
        """Membuat komponen pemilihan model"""
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                user_input = st.text_input("💡 Your Question:", placeholder="Ask me anything...")
            with col2:
                selected_model = st.selectbox(
                    "🤖 Select AI Model:",
                    options=self.model_handler.get_available_models(),
                    format_func=lambda x: AIModelHandler.SUPPORTED_MODELS[x]
                )
        return user_input, selected_model

    def _display_response(self, answer):
        """Menampilkan respons AI dengan styling mirip Qwen LM"""
        st.markdown("""
            <style>
                .qwen-response {
                    padding: 1.5rem;
                    margin: 1.25rem 0;
                    border-radius: 12px;
                    background: var(--qwen-bg, #f8fafc);
                    border-left: 4px solid var(--qwen-accent, #4f46e5);
                    font-family: 'Inter', sans-serif;
                    line-height: 1.7;
                    color: var(--qwen-text, #1e293b);
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                }

                @media (prefers-color-scheme: dark) {
                    .qwen-response {
                        --qwen-bg: #1e1e2d;
                        --qwen-text: #e2e8f0;
                        --qwen-accent: #818cf8;
                        --code-bg: #2d2d3d;
                    }
                }

                .qwen-response code {
                    font-family: 'JetBrains Mono', monospace;
                    background: var(--code-bg, #edf2f7);
                    padding: 0.25em 0.4em;
                    border-radius: 4px;
                    font-size: 0.9em;
                    color: var(--code-text, #334155);
                }

                .qwen-response pre {
                    background: var(--code-bg, #2d3748) !important;
                    padding: 1.25em !important;
                    border-radius: 8px !important;
                    border-left: 3px solid var(--qwen-accent) !important;
                    margin: 1em 0 !important;
                }

                .qwen-response p {
                    margin-bottom: 1em;
                }

                .qwen-response ul, 
                .qwen-response ol {
                    margin: 0.5em 0;
                    padding-left: 1.5em;
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("""
            <link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=JetBrains+Mono&display=swap' rel='stylesheet'>
        """, unsafe_allow_html=True)

        st.markdown("""<div class='qwen-response'>""", unsafe_allow_html=True)

        if "```" in answer:
            parts = answer.split("```")
            for i, part in enumerate(parts):
                if i % 2 == 1:
                    lang = (part.split("\n")[0].strip() or "python").lower()
                    code_content = "\n".join(part.split("\n")[1:])
                    st.code(code_content, language=lang, line_numbers=False)
                else:
                    text = part.replace("\n", "  \n")
                    st.markdown(text)
        else:
            st.markdown(answer.replace("\n", "  \n"))

        st.markdown("""</div>""", unsafe_allow_html=True)

    def run(self):
        """Menjalankan aplikasi utama"""
        user_input, selected_model = self._create_model_selector()

        if st.button("🚀 Get Answer", use_container_width=True, type="primary"):
            if not user_input.strip():
                st.warning("⚠️ Please enter a question first.")
            else:
                with st.spinner("💭 Thinking..."):
                    try:
                        messages = [
                            {'role': 'system', 'content': 'You are a helpful assistant'},
                            {'role': 'user', 'content': user_input}
                        ]
                        answer = self.model_handler.generate_response(
                            model=selected_model,
                            messages=messages
                        )
                        self._display_response(answer)
                    except RuntimeError as e:
                        st.error(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    app = ChatAppUI()
    app.run()