# RAG Application

## Overview

This application uses a Retrieval-Augmented Generation (RAG) approach to provide insights from World Bank data and GEM reports. It leverages Hugging Face's embeddings and language models, and integrates with Streamlit for user interaction.

## Features

- Fetches World Bank data for Brazil and global statistics on poverty, internet usage, and unemployment.
- Retrieves and processes GEM reports in PDF format.
- Uses Hugging Face's embeddings and language models for text-based queries.
- Provides a web interface for querying and interacting with the processed data.

## Requirements

- Python 3.7 or higher
- `requests` - For fetching data from APIs
- `pypdf` - For extracting text from PDF reports
- `pandas` - For data handling (optional, if needed)
- `streamlit` - For the web interface
- `langchain` - For handling text and embeddings
- `huggingface_hub` - For interacting with Hugging Face models

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/RAG.git
   cd RAG

2. Install the required packages
   ```bash
    pip install -r requirements.txt

3. Set up your Hugging Face API token:

Replace HUGGINGFACEHUB_API_TOKEN in app.py with your actual API token.

4. Fetch World Bank data and GEM report:
   ```bash
   python datafetcher.py

5. Run the Streamlit app.
   ```bash
   streamlit run app.py

