
import requests
import streamlit as st

OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"

st.set_page_config(
    page_title="AI Copywriting Studio",
    page_icon="✍️",
    layout="centered"
)

st.title("✍️ Automated Copywriting & Tone Transformer")
st.caption("DecodeLabs Generative AI Internship — Project 2")
st.write(
    "Generate marketing content for LinkedIn, Instagram, or Email "
    "using a local Ollama model."
)
st.info("Free local mode: This app does not use a paid API or API key.")


def get_models():
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return [
            item.get("name", "")
            for item in data.get("models", [])
            if item.get("name")
        ]
    except requests.RequestException:
        return []


models = get_models()

if not models:
    st.error(
        "Ollama could not be reached. Open the Ollama app and "
        "make sure it is running, then refresh this page."
    )
    st.code("ollama list")
    st.stop()


with st.sidebar:
    st.header("AI Settings")

    selected_model = st.selectbox(
        "Installed Ollama model",
        models
    )

    temperature = st.slider(
        "Temperature (creativity)",
        0.0, 1.0, 0.7, 0.1
    )

    top_p = st.slider(
        "Top-P (word variety)",
        0.1, 1.0, 0.9, 0.05
    )

    st.caption("Settings are sent to your local model.")


with st.form("copywriting_form"):
    product_name = st.text_input(
        "Product Name",
        placeholder="e.g., GlowCare Face Wash"
    )

    description = st.text_area(
        "Raw Product Description",
        placeholder="Describe the product, its features, and benefits...",
        height=120
    )

    platform = st.selectbox(
        "Target Platform",
        ["LinkedIn", "Instagram", "Email"]
    )

    tone = st.selectbox(
        "Tone",
        ["Professional", "Friendly", "Creative",
         "Persuasive", "Informative"]
    )

    generate = st.form_submit_button(
        "Generate Marketing Copy",
        type="primary"
    )


if generate:
    if not product_name.strip() or not description.strip():
        st.warning(
            "Please enter both a product name and product description."
        )
    else:
        platform_instructions = {
            "LinkedIn": (
                "Write a professional LinkedIn marketing post "
                "with clear benefits and a call to action."
            ),
            "Instagram": (
                "Write an engaging Instagram caption with a call "
                "to action and a few relevant hashtags."
            ),
            "Email": (
                "Write a promotional email with a subject line, "
                "greeting, concise body, and closing."
            )
        }

        prompt = f"""
TASK: Write the actual finished marketing copy now.
Do not ask the user any questions.

PRODUCT NAME: {product_name.strip()}
PRODUCT DESCRIPTION: {description.strip()}
TARGET PLATFORM: {platform}
REQUIRED TONE: {tone}

PLATFORM INSTRUCTIONS:
{platform_instructions[platform]}

RULES:
1. Use the product name and supplied description.
2. Match the selected platform and tone.
3. Never ask for more information.
4. Do not say "I'm ready to help".
5. Do not invent prices, discounts, statistics, or features.
6. Return only the finished marketing copy.
"""

        payload = {
            "model": selected_model,
            "system": (
                "You are a marketing copywriter. Create the requested "
                "marketing content using the supplied inputs. Never ask "
                "follow-up questions. Return the finished copy only."
            ),
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "num_predict": 250
            }
        }

        try:
            with st.spinner(
                f"Generating copy with {selected_model}..."
            ):
                response = requests.post(
                    OLLAMA_GENERATE_URL,
                    json=payload,
                    timeout=300
                )
                response.raise_for_status()
                output = response.json().get("response", "").strip()

            if output:
                st.subheader("Generated Marketing Copy")
                st.markdown(output)

                st.download_button(
                    "Download Copy as TXT",
                    data=output,
                    file_name="generated_marketing_copy.txt",
                    mime="text/plain"
                )
            else:
                st.warning(
                    "The model returned an empty response. Please try again."
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Connection to Ollama failed. Open Ollama and try again."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The model took too long to respond. Please try again."
            )

        except requests.exceptions.HTTPError as error:
            st.error(
                f"Ollama returned an error: {error}. "
                "Check that the selected model is installed."
            )

        except (ValueError, KeyError):
            st.error(
                "Ollama returned an unexpected response. Please try again."
            )
