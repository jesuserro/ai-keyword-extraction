import os
import openai
from dotenv import load_dotenv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

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

def generate_bar_chart(keywords: str, output_path: str):
    """
    Genera una gráfica de barras con las palabras clave y sus frecuencias reales.
    """
    # Procesamos las palabras clave
    keywords_list = keywords.split("keywords:")[-1].strip().split("\n- ")
    keywords_list = [kw for kw in keywords_list if kw]  # Filtramos palabras vacías

    # Calculamos la frecuencia de cada palabra clave
    keyword_counts = pd.Series(keywords_list).value_counts()

    # Creamos un DataFrame con las frecuencias
    df = pd.DataFrame({'Keyword': keyword_counts.index, 'Frequency': keyword_counts.values})

    # Generamos la gráfica de barras
    plt.figure(figsize=(12, 6))
    df.plot(kind='bar', x='Keyword', y='Frequency', legend=False, color='skyblue')
    plt.title('Keyword Frequency')
    plt.xlabel('Keywords')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Guardamos la gráfica
    plt.savefig(output_path, format="jpg")
    plt.close()

def generate_pie_chart(tags: dict, output_path: str):
    """
    Genera una gráfica de pastel con las categorías extraídas y sus pesos proporcionales.
    """
    # Creamos etiquetas y valores basados en la longitud de los valores de los tags
    labels = list(tags.keys())
    sizes = [len(value) for value in tags.values()]  # Usamos la longitud del valor como peso

    # Validamos que no haya valores NaN o cero en sizes
    if not sizes or sum(sizes) == 0:
        print("Warning: No valid data for pie chart. Skipping generation.")
        return

    # Generamos la gráfica de pastel
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('Tag Distribution')
    plt.tight_layout()

    # Guardamos la gráfica
    plt.savefig(output_path, format="jpg")
    plt.close()

def generate_scatter_plot(keywords: str, output_path: str):
    """
    Genera una gráfica de dispersión con las palabras clave y su relevancia basada en la longitud.
    """
    # Procesamos las palabras clave
    keywords_list = keywords.split("keywords:")[-1].strip().split("\n- ")
    keywords_list = [kw for kw in keywords_list if kw]

    # Creamos datos para la gráfica
    x = range(len(keywords_list))
    y = [len(kw) for kw in keywords_list]  # Usamos la longitud de las palabras como relevancia

    # Generamos la gráfica de dispersión
    plt.figure(figsize=(12, 6))
    plt.scatter(x, y, color='blue', alpha=0.7)
    plt.title('Keyword Relevance')
    plt.xlabel('Keyword Index')
    plt.ylabel('Relevance (Length)')
    plt.xticks(x, keywords_list, rotation=45, ha='right')
    plt.tight_layout()

    # Guardamos la gráfica
    plt.savefig(output_path, format="jpg")
    plt.close()

def parse_tags_from_keywords(keywords: str) -> dict:
    """
    Extrae los tags (author, era, literary-genre, etc.) de la salida de la IA.
    """
    tags = {}
    for line in keywords.split("\n"):
        if ":" in line:  # Busca líneas con formato "clave: valor"
            key, value = line.split(":", 1)
            tags[key.strip()] = value.strip()
    return tags

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
    print("\n🔑 **Extracted Keywords and Tags:**")
    print("\n📌 **Keywords:**")
    for keyword in extracted_keywords.split("keywords:")[-1].strip().split("\n- "):
        if keyword:
            print(f"   - {keyword}")

    # Extraemos los tags de los keywords
    tags = parse_tags_from_keywords(extracted_keywords)
    print("\n🏷️ **Tags:**")
    for key, value in tags.items():
        print(f"   - {key}: {value}")

    # Llamamos a la función para obtener libros relacionados
    related_books = extract_related_books(input_text)
    print("\n📚 **Related Books:**")
    for book in related_books.split("\n"):
        if book:
            print(f"   - {book}")

    # Generamos la nube de palabras
    output_path_cloud = "img/tag_cloud.jpg"
    os.makedirs(os.path.dirname(output_path_cloud), exist_ok=True)
    generate_tag_cloud(extracted_keywords, output_path_cloud)
    print(f"\n🌥️ **Tag cloud saved to:** {output_path_cloud}")

    # Generamos la gráfica de barras
    output_path_bar = "img/keyword_bar_chart.jpg"
    generate_bar_chart(extracted_keywords, output_path_bar)
    print(f"\n📊 **Bar chart saved to:** {output_path_bar}")

    # Generamos la gráfica de pastel con los tags extraídos
    output_path_pie = "img/tag_pie_chart.jpg"
    generate_pie_chart(tags, output_path_pie)
    print(f"\n🥧 **Pie chart saved to:** {output_path_pie}")

    # Generamos scatter plot
    output_path_scatter = "img/keyword_scatter_plot.jpg"
    generate_scatter_plot(extracted_keywords, output_path_scatter)
    print(f"\n📈 **Scatter plot saved to:** {output_path_scatter}")

if __name__ == "__main__":
    main()