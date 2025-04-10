import os
import openai
from dotenv import load_dotenv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Descargar recursos de nltk
nltk.download('stopwords')
nltk.download('wordnet')

# Cargamos variables de entorno del archivo .env si existe.
load_dotenv()

# Configura tu API Key:
openai.api_key = os.getenv("OPENAI_API_KEY")  # Alternativamente, puedes asignarla directamente aquí.

# Stop words personalizadas
CUSTOM_STOPWORDS = set(stopwords.words('english')).union({
    "de", "don", "genre", "tags", "author", "era", "literature"
})

# Lematizador
lemmatizer = WordNetLemmatizer()

# Lista de nombres propios comunes en español
SPANISH_PROPER_NAMES = {
    "miguel", "juan", "carlos", "maria", "jose", "pedro", "luis", "ana", "francisco", "antonio",
    "manuel", "carmen", "javier", "rafael", "fernando", "diego", "alejandro", "pablo", "andres"
}

def generate_tag_cloud(keywords: str, output_path: str):
    """
    Genera una nube de palabras a partir de las palabras clave y guarda la imagen en el directorio especificado.
    Filtra las stop words, nombres propios y lematiza las palabras clave.
    """
    # Convertimos las palabras clave en texto plano
    keywords_list = keywords.split("keywords:")[-1].strip().split("\n- ")
    keywords_list = [kw.strip() for kw in keywords_list if kw.strip()]  # Filtramos palabras vacías y espacios

    # Eliminamos líneas no válidas como "### tags" o caracteres extraños
    keywords_list = [kw.split("###")[0].strip() for kw in keywords_list if "###" not in kw.lower()]

    # Procesamos los valores de los tags para extraer solo el contenido después de ":"
    processed_keywords = []
    for kw in keywords_list:
        if ":" in kw:  # Si es un tag con formato "clave: valor"
            _, value = kw.split(":", 1)
            processed_keywords.append(value.strip())  # Agregamos solo el valor
        else:
            processed_keywords.append(kw)  # Agregamos la palabra clave tal cual

    # Normalizamos las stop words (minúsculas y lematización)
    normalized_stopwords = {lemmatizer.lemmatize(word.lower()) for word in CUSTOM_STOPWORDS}

    # Filtramos stop words, nombres propios y lematizamos las palabras clave
    filtered_keywords = []
    for word in processed_keywords:
        if "-" in word:
            # Dividimos la palabra en sus componentes y eliminamos stop words y nombres propios
            components = word.split("-")
            filtered_components = [
                lemmatizer.lemmatize(w.lower()) for w in components
                if lemmatizer.lemmatize(w.lower()) not in normalized_stopwords
                and w.lower() not in SPANISH_PROPER_NAMES
            ]
            # Si quedan componentes válidos, los unimos con guiones
            if filtered_components:
                normalized_word = "-".join(filtered_components)
                filtered_keywords.append(normalized_word)
        else:
            # Procesamos palabras sin guiones
            normalized_word = lemmatizer.lemmatize(word.lower())
            if normalized_word not in normalized_stopwords and normalized_word not in SPANISH_PROPER_NAMES:
                filtered_keywords.append(normalized_word)

    # Depuración: Imprimir listas para verificar el filtrado
    print(f"\nOriginal Keywords List: {keywords_list}")
    print(f"\nProcessed Keywords List: {processed_keywords}")
    print(f"\nNormalized Stopwords: {normalized_stopwords}")
    print(f"\nFiltered Keywords List: {filtered_keywords}")

    # Verificamos si hay palabras clave después del filtrado
    if not filtered_keywords:
        print("Warning: No valid keywords after filtering. Skipping tag cloud generation.")
        return

    # Unimos las palabras filtradas en un solo string
    keywords_text = " ".join(filtered_keywords)

    # Generamos la nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(keywords_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, format="jpg")
    plt.close()

# Definimos el contenido del mensaje como una constante
KEYWORDS_PROMPT = [
    "You are an expert in literature and books, particularly blurbs of classic works.",
    "You will be provided with a blurb of a famous book.",
    "Your task is to extract:",
    "1. The significant keywords from the blurb.",
    "2. Other meaningful tags (for example: the author, era, literary genre, country, if it is a classic).",
    "The output (both 1. keywords & 2. tags) should be an 'unordered Markdown list', in English, lowercase, and spaces should be replaced with hyphens."
]

# Parámetros de configuración para la llamada a la API
API_PARAMETERS = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.3,
    "max_tokens": 128
}

def extract_keywords(text: str) -> str:
    """
    Envía el texto a la API de OpenAI para extraer palabras clave.
    Retorna la lista de palabras clave propuesta por el modelo.
    """
    # Unimos las condiciones del prompt en un solo string
    system_content = " ".join(KEYWORDS_PROMPT)

    # Llamada a la API de OpenAI
    response = openai.ChatCompletion.create(
        model=API_PARAMETERS["model"],
        messages=[
            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=API_PARAMETERS["temperature"],
        max_tokens=API_PARAMETERS["max_tokens"]
    )

    # El texto devuelto por el modelo:
    keywords = response["choices"][0]["message"]["content"].strip()
    return keywords

    # El texto devuelto por el modelo:
    keywords = response["choices"][0]["message"]["content"].strip()
    return keywords

# Definimos el contenido del mensaje como una constante
SYSTEM_PROMPT = [
    "You are an expert in literature and books.",
    "You will be provided with a blurb of a famous book.",
    "Your task is to suggest a list of related books along with their authors.",
    "The output should be formatted as a 'unordered markdown list', where each entry is in the format: 'Title (Author)'."
]

def extract_related_books(text: str) -> str:
    """
    Envía el texto a la API de OpenAI para obtener un listado de libros relacionados con su autor.
    """
    # Unimos las condiciones del prompt en un solo string
    system_content = " ".join(SYSTEM_PROMPT)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_content
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
    Genera una gráfica de barras mejorada con las palabras clave y sus frecuencias reales.
    """
    # Procesamos las palabras clave
    keywords_list = keywords.split("keywords:")[-1].strip().split("\n- ")
    keywords_list = [kw for kw in keywords_list if kw]  # Filtramos palabras vacías

    # Calculamos la frecuencia de cada palabra clave
    keyword_counts = pd.Series(keywords_list).value_counts()

    # Creamos un DataFrame con las frecuencias
    df = pd.DataFrame({'Keyword': keyword_counts.index, 'Frequency': keyword_counts.values})

    # Generamos la gráfica de barras mejorada
    plt.figure(figsize=(12, 6))
    bars = plt.bar(df['Keyword'], df['Frequency'], color='skyblue', edgecolor='black')
    plt.title('Keyword Frequency', fontsize=16)
    plt.xlabel('Keywords', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)

    # Agregamos etiquetas de valores encima de las barras
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 0.5,
                 str(bar.get_height()), ha='center', va='bottom', fontsize=10, color='black')

    plt.tight_layout()

    # Guardamos la gráfica
    plt.savefig(output_path, format="jpg")
    plt.close()

def generate_pie_chart(tags: dict, output_path: str):
    """
    Genera una gráfica de pastel mejorada con las categorías extraídas y sus pesos proporcionales.
    """
    # Creamos etiquetas y valores basados en la longitud de los valores de los tags
    labels = list(tags.keys())
    sizes = [len(value) for value in tags.values()]  # Usamos la longitud del valor como peso

    # Validamos que no haya valores NaN o cero en sizes
    if not sizes or sum(sizes) == 0:
        print("Warning: No valid data for pie chart. Skipping generation.")
        return

    # Generamos la gráfica de pastel mejorada
    plt.figure(figsize=(8, 8))
    colors = plt.cm.Paired.colors  # Colores atractivos
    wedges, texts, autotexts = plt.pie(
        sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors,
        textprops={'fontsize': 12}, pctdistance=0.85
    )

    # Mejoramos el diseño
    plt.setp(autotexts, size=10, weight="bold", color="white")
    plt.title('Tag Distribution', fontsize=16)
    plt.tight_layout()

    # Guardamos la gráfica
    plt.savefig(output_path, format="jpg")
    plt.close()

def generate_scatter_plot(keywords: str, output_path: str):
    """
    Genera una gráfica de dispersión mejorada con las palabras clave y su relevancia basada en la longitud.
    Incluye líneas de cuadrícula para mayor claridad.
    """
    # Procesamos las palabras clave
    keywords_list = keywords.split("keywords:")[-1].strip().split("\n- ")
    keywords_list = [kw for kw in keywords_list if kw]

    # Creamos datos para la gráfica
    x = range(len(keywords_list))
    y = [len(kw) for kw in keywords_list]  # Usamos la longitud de las palabras como relevancia

    # Generamos la gráfica de dispersión mejorada
    plt.figure(figsize=(12, 6))
    plt.scatter(x, y, color='blue', alpha=0.7, edgecolor='black', s=100)
    plt.title('Keyword Relevance', fontsize=16)
    plt.xlabel('Keyword Index', fontsize=14)
    plt.ylabel('Relevance (Length)', fontsize=14)
    plt.xticks(x, keywords_list, rotation=45, ha='right', fontsize=12)

    # Añadimos líneas de cuadrícula en color gris
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    # Agregamos etiquetas a los puntos más relevantes
    for i, kw in enumerate(keywords_list):
        if y[i] > 5:  # Etiquetamos solo palabras clave con longitud mayor a 5
            plt.text(i, y[i] + 0.5, kw, fontsize=10, ha='center')

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
    print("\n📌 Extracted Keywords and Tags:")
    print(f"\n{extracted_keywords}")

    # Extraemos los tags de los keywords
    tags = parse_tags_from_keywords(extracted_keywords)

    # Llamamos a la función para obtener libros relacionados
    related_books = extract_related_books(input_text)
    print("\n📚 Related Books:")
    print(f"{related_books}")

    # Generamos la nube de palabras
    output_path_cloud = "img/tag_cloud.jpg"
    os.makedirs(os.path.dirname(output_path_cloud), exist_ok=True)
    generate_tag_cloud(extracted_keywords, output_path_cloud)
    print(f"\n🌥️ Tag cloud saved to: {output_path_cloud}")

    # Generamos la gráfica de barras
    output_path_bar = "img/keyword_bar_chart.jpg"
    generate_bar_chart(extracted_keywords, output_path_bar)
    print(f"📊 Bar chart saved to: {output_path_bar}")

    # Generamos la gráfica de pastel con los tags extraídos
    output_path_pie = "img/tag_pie_chart.jpg"
    generate_pie_chart(tags, output_path_pie)
    print(f"🥧 Pie chart saved to: {output_path_pie}")

    # Generamos scatter plot
    output_path_scatter = "img/keyword_scatter_plot.jpg"
    generate_scatter_plot(extracted_keywords, output_path_scatter)
    print(f"📈 Scatter plot saved to: {output_path_scatter}")

if __name__ == "__main__":
    main()