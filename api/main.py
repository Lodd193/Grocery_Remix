"""
FastAPI backend for Grocery Remix.
Exposes recipe generation and storage as REST API endpoints.
"""

import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from recipe_generator import RecipeGenerator
from storage import RecipeStorage

app = FastAPI(
    title="Grocery Remix API",
    description="Local AI-powered recipe generation",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
generator = None
storage = RecipeStorage()


def get_generator():
    """Lazy load the generator to avoid startup errors if LMStudio isn't running."""
    global generator
    if generator is None:
        generator = RecipeGenerator()
    return generator


# Request/Response Models
class RecipeRequest(BaseModel):
    ingredients: list[str]
    dietary_filters: list[str] = []


class SubstitutionRequest(BaseModel):
    ingredient: str
    context: str | None = None


class SaveRecipeRequest(BaseModel):
    title: str
    content: str
    ingredients: list[str] = []
    dietary_filters: list[str] = []


# Endpoints
@app.get("/")
def root():
    return {"message": "Grocery Remix API", "status": "running"}


@app.get("/health")
def health_check():
    """Check if API and LMStudio are ready."""
    try:
        gen = get_generator()
        return {"status": "healthy", "llm_connected": True}
    except Exception as e:
        return {"status": "degraded", "llm_connected": False, "error": str(e)}


@app.post("/generate")
def generate_recipe(request: RecipeRequest):
    """Generate a recipe based on ingredients."""
    if not request.ingredients:
        raise HTTPException(status_code=400, detail="No ingredients provided")

    try:
        gen = get_generator()
        recipe = gen.generate_recipe(request.ingredients, request.dietary_filters)
        return {
            "recipe": recipe,
            "ingredients": request.ingredients,
            "dietary_filters": request.dietary_filters
        }
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"LMStudio connection failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/substitute")
def suggest_substitution(request: SubstitutionRequest):
    """Get substitution suggestions for an ingredient."""
    if not request.ingredient:
        raise HTTPException(status_code=400, detail="No ingredient provided")

    try:
        gen = get_generator()
        suggestion = gen.suggest_substitution(request.ingredient, request.context)
        return {
            "ingredient": request.ingredient,
            "context": request.context,
            "suggestion": suggestion
        }
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"LMStudio connection failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/recipes")
def get_all_recipes():
    """Get all saved recipes."""
    recipes = storage.get_all_recipes()
    return {"recipes": recipes, "count": len(recipes)}


@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int):
    """Get a specific recipe by ID."""
    recipe = storage.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.post("/recipes")
def save_recipe(request: SaveRecipeRequest):
    """Save a recipe."""
    recipe_id = storage.save_recipe(
        title=request.title,
        content=request.content,
        ingredients=request.ingredients,
        dietary_filters=request.dietary_filters
    )
    return {"id": recipe_id, "message": "Recipe saved"}


@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    """Delete a recipe."""
    if storage.delete_recipe(recipe_id):
        return {"message": "Recipe deleted"}
    raise HTTPException(status_code=404, detail="Recipe not found")


@app.get("/recipes/search/{query}")
def search_recipes(query: str):
    """Search recipes by title or ingredient."""
    results = storage.search_recipes(query)
    return {"results": results, "count": len(results)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
