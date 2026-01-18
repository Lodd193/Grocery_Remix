# Grocery Remix - Progress Report

**Date Started:** 18 January 2026
**Project:** Grocery_Remix
**GitHub:** https://github.com/Lodd193/Grocery_Remix

---

## Project Overview

A local LLM-based application that suggests recipes based on ingredients you have available. Uses LMStudio with Meta Llama 3.1 8B Instruct for all recipe generation - no cloud APIs, completely local.

**Purpose:** Learn and showcase local LLM integration, prompt engineering, and building practical AI applications without relying on cloud services.

---

## Tech Stack

- **LLM:** LMStudio with Meta Llama 3.1 8B Instruct (local inference)
- **Language:** Python 3
- **Interface:** CLI (v1.0), Web UI (planned for v2.0)
- **Storage:** JSON for saved recipes
- **API:** LMStudio local server API

---

## MVP Features (v1.0)

1. **Ingredient Input** - Enter ingredients you have available
2. **Recipe Generation** - LLM suggests recipes using those ingredients
3. **Dietary Filters** - Modify for vegan, vegetarian, gluten-free, low-carb, etc.
4. **Ingredient Substitutions** - "I don't have X, what can I use instead?"
5. **Save Favourites** - Store recipes locally in JSON format

---

## Project Structure

```
Grocery_Remix/
├── src/
│   ├── llm_client.py       # LMStudio API connection
│   ├── recipe_generator.py # Recipe generation logic
│   ├── cli.py              # Command-line interface
│   └── storage.py          # Save/load recipes (JSON)
├── data/
│   └── saved_recipes.json  # User's saved recipes
├── tests/
│   └── test_llm_connection.py
├── requirements.txt
├── .gitignore
├── README.md
└── PROGRESS.md
```

---

## Session 1 - 18 January 2026

### Completed
- ✅ Created GitHub repository
- ✅ Initialized local git repository
- ✅ Connected local folder to GitHub remote
- ✅ Created PROGRESS.md
- ✅ Created project directory structure (src/, data/, tests/)
- ✅ Created .gitignore
- ✅ Created requirements.txt with dependencies
- ✅ Built LMStudio client (src/llm_client.py) with OpenAI-compatible API
- ✅ Updated README with setup instructions
- ✅ Tested LMStudio connection - working
- ✅ Installed dependencies (openai package)
- ✅ Built recipe_generator.py with:
  - RecipeGenerator class wrapping LMStudioClient
  - `generate_recipe(ingredients, dietary_filters)` - generates structured recipes
  - `suggest_substitution(ingredient, context)` - suggests ingredient alternatives
  - Chef persona system prompts for quality output
- ✅ Tested all recipe generator features - all working

### Next Steps
1. Build CLI interface (src/cli.py) - user-friendly command-line menu
2. Implement recipe saving (storage.py) - save/load favourites to JSON

---

## LMStudio Setup

**Model:** meta-llama-3.1-8b-instruct
**Status:** Installed
**API Endpoint:** http://localhost:1234/v1 (default LMStudio server)

---

## Notes

- Starting with CLI to learn LLM basics before adding web UI
- All processing happens locally - no external API calls
- Using LMStudio's OpenAI-compatible API for easy integration

---

## Future Ideas (Post-MVP)

- Web UI (Flask/FastAPI)
- Nutritional information calculation
- Cooking time estimates
- Difficulty ratings
- Recipe scaling (adjust servings)
- Shopping list generation
- Recipe search/filter functionality
- Export recipes to PDF
- Recipe rating system
