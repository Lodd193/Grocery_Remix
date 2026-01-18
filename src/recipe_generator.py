"""
Recipe Generator for Grocery Remix.
Uses LMStudioClient to generate recipes and ingredient substitutions.
"""

from llm_client import LMStudioClient


class RecipeGenerator:
    """Generates recipes and ingredient substitutions using LLM."""

    RECIPE_SYSTEM_PROMPT = """You are an experienced home chef who creates practical, delicious recipes.
When given ingredients, you create a complete recipe with:

1. **Recipe Title** - A descriptive name for the dish
2. **Ingredients** - Full list with quantities (use the provided ingredients plus common pantry staples)
3. **Instructions** - Clear, numbered steps
4. **Tips** - 1-2 helpful cooking tips

Keep recipes accessible for home cooks. Be specific about cooking times and temperatures."""

    SUBSTITUTION_SYSTEM_PROMPT = """You are a knowledgeable chef who helps with ingredient substitutions.
Provide practical alternatives that maintain the dish's flavor and texture.
Be concise - give 2-3 substitution options with brief explanations of how they'll affect the dish."""

    def __init__(self, client: LMStudioClient = None):
        """
        Initialize RecipeGenerator.

        Args:
            client: LMStudioClient instance (creates one if not provided)
        """
        self.client = client if client else LMStudioClient()

    def generate_recipe(self, ingredients: list[str], dietary_filters: list[str] = None) -> str:
        """
        Generate a recipe based on available ingredients.

        Args:
            ingredients: List of ingredients to use
            dietary_filters: Optional dietary restrictions (e.g., ["vegetarian", "gluten-free"])

        Returns:
            str: Generated recipe text
        """
        ingredients_text = ", ".join(ingredients)
        prompt = f"Create a recipe using these ingredients: {ingredients_text}"

        if dietary_filters:
            filters_text = ", ".join(dietary_filters)
            prompt += f"\n\nDietary requirements: {filters_text}"

        return self.client.generate_response(
            prompt=prompt,
            system_prompt=self.RECIPE_SYSTEM_PROMPT,
            temperature=0.7,
            max_tokens=1000
        )

    def suggest_substitution(self, ingredient: str, context: str = None) -> str:
        """
        Suggest substitutions for an ingredient.

        Args:
            ingredient: The ingredient to substitute
            context: Optional context about the recipe or dish

        Returns:
            str: Substitution suggestions
        """
        prompt = f"What can I substitute for {ingredient}?"

        if context:
            prompt += f"\n\nContext: {context}"

        return self.client.generate_response(
            prompt=prompt,
            system_prompt=self.SUBSTITUTION_SYSTEM_PROMPT,
            temperature=0.5,
            max_tokens=300
        )


if __name__ == "__main__":
    print("Testing Recipe Generator...")
    print("=" * 50)

    generator = RecipeGenerator()

    # Test 1: Basic recipe generation
    print("\n[Test 1] Basic Recipe Generation")
    print("-" * 30)
    ingredients = ["chicken breast", "garlic", "lemon", "olive oil", "rosemary"]
    print(f"Ingredients: {ingredients}")
    print("\nGenerating recipe...\n")
    try:
        recipe = generator.generate_recipe(ingredients)
        print(recipe)
    except ConnectionError as e:
        print(f"Error: {e}")

    # Test 2: Recipe with dietary filters
    print("\n" + "=" * 50)
    print("\n[Test 2] Recipe with Dietary Filters")
    print("-" * 30)
    ingredients = ["tofu", "broccoli", "soy sauce", "ginger", "rice"]
    dietary_filters = ["vegan", "gluten-free"]
    print(f"Ingredients: {ingredients}")
    print(f"Dietary filters: {dietary_filters}")
    print("\nGenerating recipe...\n")
    try:
        recipe = generator.generate_recipe(ingredients, dietary_filters)
        print(recipe)
    except ConnectionError as e:
        print(f"Error: {e}")

    # Test 3: Ingredient substitution
    print("\n" + "=" * 50)
    print("\n[Test 3] Ingredient Substitution")
    print("-" * 30)
    ingredient = "heavy cream"
    context = "I'm making a pasta sauce"
    print(f"Ingredient: {ingredient}")
    print(f"Context: {context}")
    print("\nFinding substitutions...\n")
    try:
        substitution = generator.suggest_substitution(ingredient, context)
        print(substitution)
    except ConnectionError as e:
        print(f"Error: {e}")

    print("\n" + "=" * 50)
    print("Testing complete!")
