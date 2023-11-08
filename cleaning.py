import re
import nltk
from nltk.corpus import words

# Download NLTK resources if not already downloaded
nltk.download("words")
nltk.download("punkt")

# Load a set of English words from NLTK for reference
english_words = set(words.words())

def clean_text(text):
    # Use regular expression to remove comments (text after '#')
    cleaned_text = re.sub(r'#.*', '', text)
    # Remove non-alphanumeric characters and extra whitespaces, tokenize
    tokens = nltk.word_tokenize(cleaned_text)
    # Filter out nonsense words and non-alphabetic tokens
    valid_words = [word for word in tokens if word.isalpha() and word.lower() in english_words]
    # Join the valid words back into cleaned text
    cleaned_text = ' '.join(valid_words)
    return cleaned_text



