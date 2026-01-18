"""
Command-line interface for Grocery Remix.
Provides user-friendly menus for recipe generation and management.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from recipe_generator import RecipeGenerator
from storage import RecipeStorage


class GroceryRemixCLI:
    """Command-line interface for Grocery Remix."""

    DIETARY_OPTIONS = [
        "vegetarian",
        "vegan",
        "gluten-free",
        "dairy-free",
        "low-carb",
        "keto",
        "nut-free"
    ]

    def __init__(self):
        """Initialize CLI with generator and storage."""
        self.generator = None  # Lazy load to avoid connection errors at startup
        self.storage = RecipeStorage()
        self.last_recipe = None  # Store last generated recipe for saving
        self.last_ingredients = None
        self.last_filters = None

    def _ensure_generator(self) -> bool:
        """Ensure generator is initialized and connected."""
        if self.generator is None:
            print("\nConnecting to LMStudio...")
            try:
                self.generator = RecipeGenerator()
                # Test connection
                from llm_client import LMStudioClient
                client = LMStudioClient()
                if not client.test_connection():
                    print("\n[ERROR] Cannot connect to LMStudio.")
                    print("Make sure LMStudio is running with the server started.")
                    return False
                print("Connected!")
                return True
            except Exception as e:
                print(f"\n[ERROR] Failed to initialize: {e}")
                return False
        return True

    def clear_screen(self):
        """Clear terminal screen."""
        print("\n" * 50)

    def print_header(self):
        """Print application header."""
        print("=" * 60)
        print("  GROCERY REMIX - Local AI Recipe Generator")
        print("  Powered by LMStudio + Llama 3.1")
        print("=" * 60)

    def print_menu(self):
        """Print main menu options."""
        print("\n--- Main Menu ---")
        print("[1] Generate Recipe (from ingredients)")
        print("[2] Generate Recipe (from macros)")
        print("[3] Ingredient Substitution")
        print("[4] View Saved Recipes")
        print("[5] Search Recipes")
        print("[6] Delete Recipe")
        print("[0] Exit")
        print("-" * 20)

    def get_input(self, prompt: str) -> str:
        """Get user input with prompt."""
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            return ""

    def get_ingredients(self) -> list[str]:
        """Get list of ingredients from user."""
        print("\nEnter your ingredients (comma-separated):")
        print("Example: chicken, garlic, lemon, olive oil")
        user_input = self.get_input("> ")

        if not user_input:
            return []

        ingredients = [i.strip() for i in user_input.split(",") if i.strip()]
        return ingredients

    def get_dietary_filters(self) -> list[str]:
        """Get dietary filters from user."""
        print("\nDietary requirements? (optional)")
        print("Available options:")
        for i, option in enumerate(self.DIETARY_OPTIONS, 1):
            print(f"  [{i}] {option}")
        print("  [0] None / Skip")
        print("\nEnter numbers separated by commas (e.g., 1,3):")

        user_input = self.get_input("> ")

        if not user_input or user_input == "0":
            return []

        filters = []
        try:
            selections = [int(x.strip()) for x in user_input.split(",")]
            for sel in selections:
                if 1 <= sel <= len(self.DIETARY_OPTIONS):
                    filters.append(self.DIETARY_OPTIONS[sel - 1])
        except ValueError:
            pass

        return filters

    def generate_recipe(self):
        """Generate a recipe based on user ingredients."""
        if not self._ensure_generator():
            return

        ingredients = self.get_ingredients()
        if not ingredients:
            print("\nNo ingredients entered. Returning to menu.")
            return

        filters = self.get_dietary_filters()

        print(f"\nIngredients: {', '.join(ingredients)}")
        if filters:
            print(f"Dietary filters: {', '.join(filters)}")

        print("\nGenerating recipe... (this may take a moment)")
        print("-" * 40)

        try:
            recipe = self.generator.generate_recipe(ingredients, filters)
            print(recipe)
            print("-" * 40)

            # Store for potential saving
            self.last_recipe = recipe
            self.last_ingredients = ingredients
            self.last_filters = filters

            # Ask to save
            save = self.get_input("\nSave this recipe? (y/n): ")
            if save.lower() in ["y", "yes"]:
                self.save_last_recipe()

        except ConnectionError as e:
            print(f"\n[ERROR] {e}")

    def save_last_recipe(self):
        """Save the last generated recipe."""
        if not self.last_recipe:
            print("No recipe to save.")
            return

        print("\nEnter a title for this recipe:")
        title = self.get_input("> ")

        if not title:
            # Try to extract title from recipe content
            lines = self.last_recipe.strip().split("\n")
            title = lines[0].replace("#", "").replace("*", "").strip()[:50]
            if not title:
                title = "Untitled Recipe"
            print(f"Using title: {title}")

        recipe_id = self.storage.save_recipe(
            title=title,
            content=self.last_recipe,
            ingredients=self.last_ingredients,
            dietary_filters=self.last_filters
        )

        print(f"\nRecipe saved! (ID: {recipe_id})")

    def generate_from_macros(self):
        """Generate a recipe based on macro targets."""
        if not self._ensure_generator():
            return

        print("\n--- Generate from Macros ---")
        print("Enter your nutritional targets (press Enter to skip any):")

        calories = self.get_input("Calories: ")
        protein = self.get_input("Protein (g): ")
        carbs = self.get_input("Carbs (g): ")
        fat = self.get_input("Fat (g): ")

        # Validate at least one target
        if not any([calories, protein, carbs, fat]):
            print("\nPlease enter at least one macro target.")
            return

        filters = self.get_dietary_filters()

        # Build targets display
        targets = []
        if calories:
            targets.append(f"{calories} cal")
        if protein:
            targets.append(f"{protein}g protein")
        if carbs:
            targets.append(f"{carbs}g carbs")
        if fat:
            targets.append(f"{fat}g fat")

        print(f"\nTargets: {', '.join(targets)}")
        if filters:
            print(f"Dietary filters: {', '.join(filters)}")

        print("\nGenerating macro-targeted meal... (this may take a moment)")
        print("-" * 40)

        try:
            recipe = self.generator.generate_from_macros(
                calories=int(calories) if calories else None,
                protein=int(protein) if protein else None,
                carbs=int(carbs) if carbs else None,
                fat=int(fat) if fat else None,
                dietary_filters=filters
            )
            print(recipe)
            print("-" * 40)

            # Store for potential saving
            self.last_recipe = recipe
            self.last_ingredients = targets  # Use targets as "ingredients" for display
            self.last_filters = filters

            # Ask to save
            save = self.get_input("\nSave this recipe? (y/n): ")
            if save.lower() in ["y", "yes"]:
                self.save_last_recipe()

        except ConnectionError as e:
            print(f"\n[ERROR] {e}")

    def ingredient_substitution(self):
        """Get substitution suggestions for an ingredient."""
        if not self._ensure_generator():
            return

        print("\nWhat ingredient do you need to substitute?")
        ingredient = self.get_input("> ")

        if not ingredient:
            print("No ingredient entered. Returning to menu.")
            return

        print("\nWhat are you making? (optional, press Enter to skip)")
        context = self.get_input("> ")

        print(f"\nFinding substitutes for: {ingredient}")
        print("-" * 40)

        try:
            result = self.generator.suggest_substitution(ingredient, context if context else None)
            print(result)
            print("-" * 40)
        except ConnectionError as e:
            print(f"\n[ERROR] {e}")

    def view_saved_recipes(self):
        """Display all saved recipes."""
        recipes = self.storage.get_all_recipes()

        if not recipes:
            print("\nNo saved recipes yet.")
            print("Generate a recipe and save it to see it here!")
            return

        print(f"\n--- Saved Recipes ({len(recipes)}) ---")
        for recipe in recipes:
            print(f"\n[{recipe['id']}] {recipe['title']}")
            if recipe.get('ingredients'):
                print(f"    Ingredients: {', '.join(recipe['ingredients'][:5])}")
            if recipe.get('dietary_filters'):
                print(f"    Dietary: {', '.join(recipe['dietary_filters'])}")
            print(f"    Saved: {recipe.get('saved_at', 'Unknown')[:10]}")

        # Option to view full recipe
        print("\n" + "-" * 40)
        view_id = self.get_input("Enter recipe ID to view full recipe (or press Enter to go back): ")

        if view_id:
            try:
                recipe_id = int(view_id)
                recipe = self.storage.get_recipe(recipe_id)
                if recipe:
                    print(f"\n{'=' * 50}")
                    print(f"  {recipe['title']}")
                    print("=" * 50)
                    print(recipe['content'])
                    print("=" * 50)
                else:
                    print(f"Recipe #{recipe_id} not found.")
            except ValueError:
                print("Invalid ID.")

    def search_recipes(self):
        """Search saved recipes."""
        print("\nEnter search term (title or ingredient):")
        query = self.get_input("> ")

        if not query:
            print("No search term entered.")
            return

        results = self.storage.search_recipes(query)

        if not results:
            print(f"\nNo recipes found matching '{query}'")
            return

        print(f"\n--- Search Results ({len(results)}) ---")
        for recipe in results:
            print(f"[{recipe['id']}] {recipe['title']}")

    def delete_recipe(self):
        """Delete a saved recipe."""
        recipes = self.storage.get_all_recipes()

        if not recipes:
            print("\nNo saved recipes to delete.")
            return

        print("\n--- Saved Recipes ---")
        for recipe in recipes:
            print(f"[{recipe['id']}] {recipe['title']}")

        print("\nEnter recipe ID to delete:")
        recipe_id = self.get_input("> ")

        try:
            recipe_id = int(recipe_id)
            recipe = self.storage.get_recipe(recipe_id)

            if not recipe:
                print(f"Recipe #{recipe_id} not found.")
                return

            confirm = self.get_input(f"Delete '{recipe['title']}'? (y/n): ")
            if confirm.lower() in ["y", "yes"]:
                if self.storage.delete_recipe(recipe_id):
                    print("Recipe deleted.")
                else:
                    print("Failed to delete recipe.")
            else:
                print("Cancelled.")

        except ValueError:
            print("Invalid ID.")

    def run(self):
        """Run the main application loop."""
        self.print_header()

        while True:
            self.print_menu()
            choice = self.get_input("Select option: ")

            if choice == "1":
                self.generate_recipe()
            elif choice == "2":
                self.generate_from_macros()
            elif choice == "3":
                self.ingredient_substitution()
            elif choice == "4":
                self.view_saved_recipes()
            elif choice == "5":
                self.search_recipes()
            elif choice == "6":
                self.delete_recipe()
            elif choice == "0":
                print("\nGoodbye! Happy cooking!")
                break
            else:
                print("\nInvalid option. Please try again.")


def main():
    """Entry point for the CLI."""
    try:
        cli = GroceryRemixCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
