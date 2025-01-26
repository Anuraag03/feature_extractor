# feature_extractor
An end-end NLP based feature extraction and label prediction model

This project provides a Dockerized FastAPI service for text classification and entity extraction. It uses a pre-trained machine learning model to predict labels for input text and extracts domain-specific entities using spaCy and NLTK.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Service](#running-the-service)
- [Testing the API](#testing-the-api)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

## Features

- **Text Classification:** Predicts labels for input text using a pre-trained machine learning model.
- **Entity Extraction:** Extracts domain-specific entities using spaCy and a custom PhraseMatcher.
- **Text Summarization:** Generates a 1-2 sentence summary of the input text.
- **Dockerized:** Easy to set up and run using Docker.

## Prerequisites

Before running the service, ensure you have the following installed:

- **Docker:** Install [Docker](https://www.docker.com/)
- **Git:** Install [Git](https://git-scm.com/)
- **Python (optional):** Install [Python](https://www.python.org/) for local development

## Setup

Follow these steps to set up the project:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Build the Docker Image

Build the Docker image using the provided Dockerfile:

```bash
docker build -t fastapi-label-prediction .
```

## Running the Service

Once the Docker image is built, you can run the service using Docker.

### 1. Run the Docker Container

Start the container with the following command:

```bash
docker run -d -p 8000:8000 --name label-prediction-api fastapi-label-prediction
```

- `-d`: Runs the container in detached mode (in the background).
- `-p 8000:8000`: Maps port 8000 on your local machine to port 8000 in the container.
- `--name label-prediction-api`: Names the container `label-prediction-api`.
- `fastapi-label-prediction`: Specifies the Docker image to use.

### 2. Verify the Service is Running

Check the logs to ensure the service is running:

```bash
docker logs label-prediction-api
```

You should see output similar to:

```
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
```

## Testing the API

The FastAPI service provides a single endpoint for analyzing text snippets.

### API Endpoint

- **URL:** `http://localhost:8000/analyze-snippet/`
- **Method:** `POST`
- **Input:** JSON object with a `text` field.
- **Output:** JSON object with predicted labels, extracted entities, and a summary.

### Sample curl Command

```bash
curl -X POST -H "Content-Type: application/json" -d '{"text": "This is a new text snippet about CompetitorX and AI engine."}' http://localhost:8000/analyze-snippet/
```

### Sample Response

```json
{
  "predicted_labels": ["competitors", "features"],
  "extracted_entities": [
    ["CompetitorX", "competitors"],
    ["AI engine", "features"]
  ],
  "summary": "This is a new text snippet about CompetitorX and AI engine."
}
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- **FastAPI** for the web framework.
- **spaCy** for entity extraction.
- **NLTK** for text preprocessing.
- **Docker** for containerization.

## Contact

For questions or feedback, please contact:

- **Your Name:** [akellaanuraag8@gmail.com](mailto\:akellaanuraag8@gmail.com)
- **GitHub:** [Anuraag03](https://github.com/Anuraag03)

