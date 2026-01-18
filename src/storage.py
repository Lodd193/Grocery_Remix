"""
Recipe storage for Grocery Remix.
Handles saving and loading recipes to/from JSON.
"""

import json
import os
from datetime import datetime
from pathlib import Path


class RecipeStorage:
    """Manages saving and loading recipes to JSON storage."""

    def __init__(self, storage_path: str = None):
        """
        Initialize RecipeStorage.

        Args:
            storage_path: Path to JSON file (defaults to data/saved_recipes.json)
        """
        if storage_path is None:
            # Default to data/saved_recipes.json relative to project root
            project_root = Path(__file__).parent.parent
            storage_path = project_root / "data" / "saved_recipes.json"

        self.storage_path = Path(storage_path)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Create storage file and directory if they don't exist."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.storage_path.exists():
            self._save_data({"recipes": []})

    def _load_data(self) -> dict:
        """Load data from JSON file."""
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"recipes": []}

    def _save_data(self, data: dict):
        """Save data to JSON file."""
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save_recipe(self, title: str, content: str, ingredients: list[str] = None,
                    dietary_filters: list[str] = None) -> int:
        """
        Save a recipe to storage.

        Args:
            title: Recipe title
            content: Full recipe text
            ingredients: List of ingredients used
            dietary_filters: List of dietary filters applied

        Returns:
            int: ID of the saved recipe
        """
        data = self._load_data()

        # Generate unique ID
        recipe_id = max([r.get("id", 0) for r in data["recipes"]], default=0) + 1

        recipe = {
            "id": recipe_id,
            "title": title,
            "content": content,
            "ingredients": ingredients or [],
            "dietary_filters": dietary_filters or [],
            "saved_at": datetime.now().isoformat()
        }

        data["recipes"].append(recipe)
        self._save_data(data)

        return recipe_id

    def get_all_recipes(self) -> list[dict]:
        """
        Get all saved recipes.

        Returns:
            list: List of recipe dictionaries
        """
        data = self._load_data()
        return data.get("recipes", [])

    def get_recipe(self, recipe_id: int) -> dict | None:
        """
        Get a specific recipe by ID.

        Args:
            recipe_id: ID of the recipe to retrieve

        Returns:
            dict: Recipe data or None if not found
        """
        recipes = self.get_all_recipes()
        for recipe in recipes:
            if recipe.get("id") == recipe_id:
                return recipe
        return None

    def delete_recipe(self, recipe_id: int) -> bool:
        """
        Delete a recipe by ID.

        Args:
            recipe_id: ID of the recipe to delete

        Returns:
            bool: True if deleted, False if not found
        """
        data = self._load_data()
        original_count = len(data["recipes"])

        data["recipes"] = [r for r in data["recipes"] if r.get("id") != recipe_id]

        if len(data["recipes"]) < original_count:
            self._save_data(data)
            return True
        return False

    def search_recipes(self, query: str) -> list[dict]:
        """
        Search recipes by title or ingredients.

        Args:
            query: Search term

        Returns:
            list: Matching recipes
        """
        query = query.lower()
        recipes = self.get_all_recipes()

        results = []
        for recipe in recipes:
            # Search in title
            if query in recipe.get("title", "").lower():
                results.append(recipe)
                continue
            # Search in ingredients
            for ingredient in recipe.get("ingredients", []):
                if query in ingredient.lower():
                    results.append(recipe)
                    break

        return results

    def count_recipes(self) -> int:
        """Return the number of saved recipes."""
        return len(self.get_all_recipes())


if __name__ == "__main__":
    print("Testing Recipe Storage...")
    print("=" * 50)

    storage = RecipeStorage()

    # Test 1: Save a recipe
    print("\n[Test 1] Saving a recipe...")
    recipe_id = storage.save_recipe(
        title="Lemon Garlic Chicken",
        content="A delicious chicken recipe with lemon and garlic...",
        ingredients=["chicken", "lemon", "garlic"],
        dietary_filters=["gluten-free"]
    )
    print(f"Saved recipe with ID: {recipe_id}")

    # Test 2: Get all recipes
    print("\n[Test 2] Getting all recipes...")
    recipes = storage.get_all_recipes()
    print(f"Found {len(recipes)} recipe(s)")

    # Test 3: Get specific recipe
    print("\n[Test 3] Getting recipe by ID...")
    recipe = storage.get_recipe(recipe_id)
    if recipe:
        print(f"Found: {recipe['title']}")

    # Test 4: Search recipes
    print("\n[Test 4] Searching for 'chicken'...")
    results = storage.search_recipes("chicken")
    print(f"Found {len(results)} matching recipe(s)")

    # Test 5: Delete recipe
    print("\n[Test 5] Deleting recipe...")
    deleted = storage.delete_recipe(recipe_id)
    print(f"Deleted: {deleted}")

    print("\n" + "=" * 50)
    print("Storage tests complete!")
