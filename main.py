import os
import openai
from dotenv import load_dotenv
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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
                    "You will be provided with a blurb of a famous book. Your task is to extract: 1. the "
                    "significant keywords from the blurb, "
                    "and 2. other meaningful tags (for example: the author, era, literary genre, country, if it is a classic). The all output (keywords & tags) should be in English, lowercase, and "
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

def generate_tag_cloud(keywords: str, output_path: str):
    """
    Genera una nube de palabras a partir de las palabras clave y guarda la imagen en el directorio especificado.
    """
    # Convertimos las palabras clave en texto plano
    # Extraemos solo las palabras clave después de "keywords:" y las unimos en un solo string
    keywords_list = keywords.split("keywords:")[-1].strip().split("\n- ")
    keywords_text = " ".join(keywords_list)

    # Generamos la nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(keywords_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, format="jpg")
    plt.close()

def extract_related_books(text: str) -> str:
    """
    Envía el texto a la API de OpenAI para obtener un listado de libros relacionados con su autor.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in literature and books. You will be provided with a blurb of a famous book. "
                    "Your task is to suggest a list of related books along with their authors. The output should be "
                    "formatted as a list, where each entry is in the format: 'Title - Author'."
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
    related_books = response["choices"][0]["message"]["content"].strip()
    return related_books

def main():
    # Aquí podrías tener la cadena de texto de entrada organizada en una lista legible.
    input_text = [
        "Don Quixote, written by Miguel de Cervantes and first published in 1605, is considered one of the",
        "greatest works of literature ever written. This timeless classic follows the adventures of Alonso",
        "Quixano, a nobleman who reads so many chivalric romances that he loses his sanity and decides to",
        "become a knight-errant, renaming himself Don Quixote. Accompanied by his loyal squire, Sancho Panza,",
        "he sets out on a series of misadventures, battling windmills he believes to be giants and attempting",
        "to revive chivalry in a world that has moved on. A profound exploration of idealism, reality, and the",
        "human condition, Don Quixote remains a cornerstone of Western literature."
    ]
    input_text = " ".join(input_text)  # Convertimos la lista en un solo string

    # Llamamos a la función para extraer palabras clave
    extracted_keywords = extract_keywords(input_text)

    # Imprimimos el resultado
    print("------ OUTPUT ------")
    print(extracted_keywords)

    # Llamamos a la función para obtener libros relacionados
    related_books = extract_related_books(input_text)
    print("\nRelated books:")
    print(related_books)

        # Generamos la nube de palabras y la guardamos en el folder "img/"
    output_path = "img/tag_cloud.jpg"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    generate_tag_cloud(extracted_keywords, output_path)
    print(f"\n\nTag cloud saved to {output_path}")

if __name__ == "__main__":
    main()