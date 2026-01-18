# Grocery Remix

A local LLM-based application that suggests recipes based on ingredients you have available. Uses LMStudio with Meta Llama 3.1 8B Instruct - completely local, no cloud APIs.

## Features

- 🥘 **Recipe Generation** - Get recipe suggestions based on your available ingredients
- 🌱 **Dietary Filters** - Vegan, vegetarian, gluten-free, low-carb options
- 🔄 **Ingredient Substitutions** - Find alternatives for missing ingredients
- 💾 **Save Favourites** - Store your favourite recipes locally

## Requirements

- Python 3.8+
- LMStudio with meta-llama-3.1-8b-instruct model
- ~8GB RAM (for running the LLM)

## Setup

### 1. Install LMStudio

Download from [https://lmstudio.ai](https://lmstudio.ai) and install the `meta-llama-3.1-8b-instruct` model.

### 2. Start LMStudio Server

1. Open LMStudio
2. Load the `meta-llama-3.1-8b-instruct` model
3. Click "Start Server" (default: http://localhost:1234)

### 3. Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Test Connection

```bash
python src/llm_client.py
```

You should see a successful connection message and a test recipe generation.

## Usage

Coming soon - CLI interface in development.

## Project Status

See [PROGRESS.md](PROGRESS.md) for detailed development progress.
