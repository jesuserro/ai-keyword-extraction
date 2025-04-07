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
    # Ajusta el modelo según tu plan/disponibilidad (p.ej. "gpt-3.5-turbo" o "gpt-4")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You will be provided with a block of text, and your task is "
                    "to extract a list of keywords from it. Respond only with the keywords."
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
    Black-on-black ware is a 20th- and 21st-century pottery tradition developed 
    by the Puebloan Native American ceramic artists in Northern New Mexico. Traditional 
    reduction-fired blackware has been made for centuries by pueblo artists. Black-on-black 
    ware of the past century is produced with a smooth surface, with the designs applied 
    through selective burnishing or the application of refractory slip. Another style involves 
    carving or incising designs and selectively polishing the raised areas. For generations 
    several families from Kha'po Owingeh and P'ohwhóge Owingeh pueblos have been making 
    black-on-black ware with the techniques passed down from matriarch potters. Artists from 
    other pueblos have also produced black-on-black ware. Several contemporary artists have 
    created works honoring the pottery of their ancestors.
    """

    # Llamamos a la función para extraer palabras clave
    extracted_keywords = extract_keywords(input_text)

    # Imprimimos el resultado
    print("Palabras clave extraídas:")
    print(extracted_keywords)

if __name__ == "__main__":
    main()
