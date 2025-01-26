from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import spacy
from spacy.matcher import PhraseMatcher
import joblib
import numpy as np
import pandas as pd
import nltk
import re

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import json


# Load spaCy's pre-trained model
nlp = spacy.load("en_core_web_sm")

# Load the pre-trained label prediction model and MultiLabelBinarizer
label_prediction_model = joblib.load("label_prediction_model.pkl")
mlb = joblib.load("multilabel_binarizer.pkl")

# Text preprocessing function
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()

    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)

    # Tokenize the text
    words = text.split()

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    # Join the words back into a string
    processed_text = ' '.join(words)

    return processed_text

# Domain knowledge base

with open("domain_knowledge.json", "r") as file:
    domain_knowledge = json.load(file)

# Create a PhraseMatcher object
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

# Add domain knowledge patterns to the matcher
for category, keywords in domain_knowledge.items():
    patterns = [nlp.make_doc(keyword) for keyword in keywords]
    matcher.add(category, patterns)

# Function to extract entities using spaCy and PhraseMatcher
def extract_entities(text):
    doc = nlp(text)
    entities = []

    # Extract domain-specific entities using PhraseMatcher
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        category = nlp.vocab.strings[match_id]
        entities.append((span.text, category))

    # Extract general entities using spaCy's NER
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    # Remove duplicates
    entities = list(set(entities))
    return entities

# Function to generate a summary (1-2 sentences)
def generate_summary(text):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    summary = " ".join(sentences[:2])  # Take the first 2 sentences as summary
    return summary

# Define the input schema for the API
class Snippet(BaseModel):
    text: str

# Initialize FastAPI app
app = FastAPI()

# Define the API endpoint
@app.post("/analyze-snippet/")
async def analyze_snippet(snippet: Snippet):
    try:
        text = snippet.text

        # Step 1: Preprocess the text
        processed_text = preprocess_text(text)

        # Step 2: Predict labels
        predicted_labels_binary = label_prediction_model.predict([processed_text])
        predicted_labels = mlb.inverse_transform(predicted_labels_binary)

        # Step 3: Extract entities
        entities = extract_entities(text)

        # Step 4: Generate summary
        summary = generate_summary(text)

        # Return the results
        return {
            "predicted_labels": predicted_labels[0],  # Flatten the list
            "extracted_entities": entities,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)