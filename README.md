# 🔑 AI-Powered Keyword Extraction with OpenAI

Welcome to the **Keyword Extraction Project**, where we use the power of OpenAI's ChatCompletion API to extract keywords from any given text. This repository contains a simple Python script that demonstrates how to interact with the API and retrieve keywords efficiently.

![Tag Cloud](img/tag_cloud.jpg)

## 🖥️ Example Output

When running the script, you will see the following output in the terminal:

```plaintext
🔑 **Extracted Keywords and Tags:**

📌 **Keywords:**
   - don-quixote
   - miguel-de-cervantes
   - literature
   - nobleman
   - chivalric-romances
   - knight-errant
   - sancho-panza
   - windmills
   - giants
   - chivalry
   - idealism
   - reality
   - human-condition
   - western-literature

🏷️ **Tags:**
   - author: miguel-de-cervantes
   - era: 1605
   - literary-genre: classic
   - country: spain

📚 **Related Books:**
   - "The Canterbury Tales" - Geoffrey Chaucer
   - "Gulliver's Travels" - Jonathan Swift
   - "Pilgrim's Progress" - John Bunyan
   - "Robinson Crusoe" - Daniel Defoe
   - "Moby-Dick" - Herman Melville

🌥️ **Tag cloud saved to:** [tag_cloud.jpg](http://_vscodecontentref_/3)
📊 **Bar chart saved to:** [keyword_bar_chart.jpg](http://_vscodecontentref_/4)
🥧 **Pie chart saved to:** [tag_pie_chart.jpg](http://_vscodecontentref_/5)
📈 **Scatter plot saved to:** [keyword_scatter_plot.jpg](http://_vscodecontentref_/6)
```

## ✨ Features

- **Keyword Extraction**: Provide a block of text, get back its main keywords.
- **Lightweight & Minimal**: Only a few dependencies needed.
- **Easily Customizable**: Adjust the model, temperature, and prompt instructions.

## ⚙️ Installation

1. **Clone this repository**:
  
   ```bash
   git clone https://github.com/your-username/keyword-extraction-project.git
   cd keyword-extraction-project
   ```

2. **Set up your virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies**:
  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key**:
   - Create a file named `.env` in the project root directory with the line:

     ``` text
     OPENAI_API_KEY=YOUR_SECRET_KEY
     ```

     **OR** export it directly in your shell:

     ```bash
     export OPENAI_API_KEY=YOUR_SECRET_KEY
     ```

---

## 🚀 Usage

1. **Run the main script**:
  
   ```bash
   python main.py
   ```

2. **Observe the output**: You will see a printed list of keywords extracted from the sample text in `main.py`.

3. **Customize**:
   - Modify the `input_text` variable in `main.py` with your own text.
   - Adjust parameters such as `model`, `temperature`, and `max_tokens` inside the `extract_keywords` function to fit your needs.
   - If you prefer to run it in a Jupyter Notebook, simply copy the relevant code into a `.ipynb` file.

## 📂 Project Structure

``` text
keyword-extraction-project/
├── README.md          # Project documentation
├── requirements.txt   # Python dependencies
├── main.py            # Main script with API call
└── .env               # (Optional) Store your OpenAI API Key here
```

---

## 💡 Contributing

If you’d like to contribute to this project:

1. Fork this repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Make your changes and commit: `git commit -m "Add your feature"`.
4. Push to your fork: `git push origin feature/your-feature`.
5. Create a Pull Request.

---

## 📜 License

This project is released under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use and modify this template to suit your needs!
