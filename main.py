import os
import openai
from dotenv import load_dotenv

# Cargamos variables de entorno del archivo .env si existe.
load_dotenv()

# Configura tu API Key:
openai.api_key = os.getenv("OPENAI_API_KEY")  # Alternativamente, puedes asignarla directamente aquí.

def extract_keywords(text: str) -> str:
    """
    Envía el texto a la API de OpenAI para extraer palabras clave.
    Retorna la lista de palabras clave propuesta por el modelo.
    """
    # Aquí usamos la nueva endpoint ChatCompletion, con el modelo GPT-3.5 o GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in literature and books, particularly blurbs of classic works. "
                    "You will be provided with a blurb of a famous book. Your task is to extract the "
                    "significant keywords from the blurb, along with the author, era, literary genre, "
                    "and other meaningful tags. The output tags should be in English, lowercase, and "
                    "spaces should be replaced with hyphens."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3,
        max_tokens=128
    )

    # El texto devuelto por el modelo:
    keywords = response["choices"][0]["message"]["content"].strip()
    return keywords

def main():
    # Aquí podrías tener la cadena de texto de entrada.
    input_text = """
    Don Quixote, written by Miguel de Cervantes and first published in 1605, is considered one of the 
    greatest works of literature ever written. This timeless classic follows the adventures of Alonso 
    Quixano, a nobleman who reads so many chivalric romances that he loses his sanity and decides to 
    become a knight-errant, renaming himself Don Quixote. Accompanied by his loyal squire, Sancho Panza, 
    he sets out on a series of misadventures, battling windmills he believes to be giants and attempting 
    to revive chivalry in a world that has moved on. A profound exploration of idealism, reality, and the 
    human condition, Don Quixote remains a cornerstone of Western literature.
    """

    # Llamamos a la función para extraer palabras clave
    extracted_keywords = extract_keywords(input_text)

    # Imprimimos el resultado
    print("Extracted keywords:")
    print(extracted_keywords)

if __name__ == "__main__":
    main()
