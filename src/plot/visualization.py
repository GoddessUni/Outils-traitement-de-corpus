import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import re

def setup_nltk():
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

CSV_PATH = "arxiv_abstracts_sampled100000.csv"
TEXT_FIELD = "abstract"
TOP_N_WORDS = 30
LANGUAGE = "english"

def plot_length_distribution(df):
    lengths = df[TEXT_FIELD].dropna().apply(lambda x: len(word_tokenize(x)))
    
    plt.figure(figsize=(10, 6))
    sns.histplot(lengths, bins=50, kde=True, color="skyblue")
    plt.title("Word length distribution")
    plt.xlabel("Length")
    plt.ylabel("Articles")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("abstract_length_distribution.png")
    plt.show()

def plot_top_words(df):
    stop_words = set(stopwords.words(LANGUAGE))
    abstracts = df[TEXT_FIELD].dropna().tolist()
    
    tokens = []
    for abstract in abstracts:
        words = word_tokenize(abstract.lower())
        clean_words = [w for w in words if w.isalpha() and w not in stop_words]
        tokens.extend(clean_words)
    
    counter = Counter(tokens)
    common_words = counter.most_common(TOP_N_WORDS)
    words, freqs = zip(*common_words)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(words), y=list(freqs), palette="viridis")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Top {TOP_N_WORDS} words")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("top_words_barplot.png")
    plt.show()

def main():
    setup_nltk()
    df = pd.read_csv(CSV_PATH)
    print("Print word distribution...")
    plot_length_distribution(df)
    print("Print top words...")
    plot_top_words(df)

if __name__ == "__main__":
    main()
