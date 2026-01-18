import { useState, useEffect } from 'react'
import './App.css'

const API_URL = 'http://localhost:8000'

const DIETARY_OPTIONS = [
  'vegetarian',
  'vegan',
  'gluten-free',
  'dairy-free',
  'low-carb',
  'keto',
  'nut-free'
]

function App() {
  const [activeTab, setActiveTab] = useState('generate')
  const [ingredients, setIngredients] = useState('')
  const [dietaryFilters, setDietaryFilters] = useState([])
  const [recipe, setRecipe] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [savedRecipes, setSavedRecipes] = useState([])
  const [showSaveModal, setShowSaveModal] = useState(false)
  const [saveTitle, setSaveTitle] = useState('')
  const [viewingRecipe, setViewingRecipe] = useState(null)

  // Substitution state
  const [subIngredient, setSubIngredient] = useState('')
  const [subContext, setSubContext] = useState('')
  const [substitution, setSubstitution] = useState(null)

  // Macro state
  const [macroCalories, setMacroCalories] = useState('')
  const [macroProtein, setMacroProtein] = useState('')
  const [macroCarbs, setMacroCarbs] = useState('')
  const [macroFat, setMacroFat] = useState('')
  const [macroDietaryFilters, setMacroDietaryFilters] = useState([])
  const [macroRecipe, setMacroRecipe] = useState(null)

  useEffect(() => {
    if (activeTab === 'saved') {
      fetchSavedRecipes()
    }
  }, [activeTab])

  const fetchSavedRecipes = async () => {
    try {
      const res = await fetch(`${API_URL}/recipes`)
      const data = await res.json()
      setSavedRecipes(data.recipes || [])
    } catch (err) {
      console.error('Failed to fetch recipes:', err)
    }
  }

  const toggleFilter = (filter) => {
    setDietaryFilters(prev =>
      prev.includes(filter)
        ? prev.filter(f => f !== filter)
        : [...prev, filter]
    )
  }

  const toggleMacroFilter = (filter) => {
    setMacroDietaryFilters(prev =>
      prev.includes(filter)
        ? prev.filter(f => f !== filter)
        : [...prev, filter]
    )
  }

  const generateFromMacros = async () => {
    if (!macroCalories && !macroProtein && !macroCarbs && !macroFat) {
      setError('Please enter at least one macro target')
      return
    }

    setLoading(true)
    setError(null)
    setMacroRecipe(null)

    try {
      const res = await fetch(`${API_URL}/generate-from-macros`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          calories: macroCalories ? parseInt(macroCalories) : null,
          protein: macroProtein ? parseInt(macroProtein) : null,
          carbs: macroCarbs ? parseInt(macroCarbs) : null,
          fat: macroFat ? parseInt(macroFat) : null,
          dietary_filters: macroDietaryFilters
        })
      })

      if (!res.ok) {
        const errData = await res.json()
        throw new Error(errData.detail || 'Failed to generate recipe')
      }

      const data = await res.json()
      setMacroRecipe(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const generateRecipe = async () => {
    if (!ingredients.trim()) {
      setError('Please enter some ingredients')
      return
    }

    setLoading(true)
    setError(null)
    setRecipe(null)

    try {
      const ingredientList = ingredients.split(',').map(i => i.trim()).filter(Boolean)

      const res = await fetch(`${API_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ingredients: ingredientList,
          dietary_filters: dietaryFilters
        })
      })

      if (!res.ok) {
        const errData = await res.json()
        throw new Error(errData.detail || 'Failed to generate recipe')
      }

      const data = await res.json()
      setRecipe(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const getSubstitution = async () => {
    if (!subIngredient.trim()) {
      setError('Please enter an ingredient to substitute')
      return
    }

    setLoading(true)
    setError(null)
    setSubstitution(null)

    try {
      const res = await fetch(`${API_URL}/substitute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ingredient: subIngredient,
          context: subContext || null
        })
      })

      if (!res.ok) {
        const errData = await res.json()
        throw new Error(errData.detail || 'Failed to get substitution')
      }

      const data = await res.json()
      setSubstitution(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const saveRecipe = async () => {
    if (!recipe || !saveTitle.trim()) return

    try {
      const res = await fetch(`${API_URL}/recipes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: saveTitle,
          content: recipe.recipe,
          ingredients: recipe.ingredients,
          dietary_filters: recipe.dietary_filters
        })
      })

      if (res.ok) {
        setShowSaveModal(false)
        setSaveTitle('')
        fetchSavedRecipes()
      }
    } catch (err) {
      console.error('Failed to save recipe:', err)
    }
  }

  const deleteRecipe = async (id) => {
    if (!confirm('Delete this recipe?')) return

    try {
      await fetch(`${API_URL}/recipes/${id}`, { method: 'DELETE' })
      fetchSavedRecipes()
      if (viewingRecipe?.id === id) {
        setViewingRecipe(null)
      }
    } catch (err) {
      console.error('Failed to delete recipe:', err)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>Grocery Remix</h1>
          <p>Local AI-powered recipe generation</p>
        </header>

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'generate' ? 'active' : ''}`}
            onClick={() => setActiveTab('generate')}
          >
            Generate
          </button>
          <button
            className={`tab ${activeTab === 'macros' ? 'active' : ''}`}
            onClick={() => setActiveTab('macros')}
          >
            Macros
          </button>
          <button
            className={`tab ${activeTab === 'substitute' ? 'active' : ''}`}
            onClick={() => setActiveTab('substitute')}
          >
            Substitute
          </button>
          <button
            className={`tab ${activeTab === 'saved' ? 'active' : ''}`}
            onClick={() => setActiveTab('saved')}
          >
            Saved ({savedRecipes.length})
          </button>
        </div>

        {error && (
          <div className="status error">{error}</div>
        )}

        <main className="main-content">
          {/* Generate Tab */}
          {activeTab === 'generate' && (
            <>
              <div className="generate-section">
                <div className="card">
                  <div className="form-group">
                    <label>Ingredients</label>
                    <textarea
                      placeholder="Enter ingredients separated by commas (e.g., chicken, garlic, lemon, olive oil)"
                      value={ingredients}
                      onChange={(e) => setIngredients(e.target.value)}
                    />
                  </div>

                  <div className="form-group">
                    <label>Dietary Filters (optional)</label>
                    <div className="checkbox-group">
                      {DIETARY_OPTIONS.map(filter => (
                        <label
                          key={filter}
                          className={`checkbox-item ${dietaryFilters.includes(filter) ? 'checked' : ''}`}
                        >
                          <input
                            type="checkbox"
                            checked={dietaryFilters.includes(filter)}
                            onChange={() => toggleFilter(filter)}
                          />
                          {filter}
                        </label>
                      ))}
                    </div>
                  </div>

                  <button
                    className="btn btn-primary"
                    onClick={generateRecipe}
                    disabled={loading}
                  >
                    {loading ? 'Generating...' : 'Generate Recipe'}
                  </button>
                </div>

                <div className="card">
                  <h2>Tips</h2>
                  <ul style={{ paddingLeft: '1.5rem', lineHeight: '1.8' }}>
                    <li>Include 3-6 main ingredients</li>
                    <li>Be specific (e.g., "chicken breast" not just "chicken")</li>
                    <li>Add pantry staples like garlic, olive oil</li>
                    <li>Use dietary filters for specific needs</li>
                  </ul>
                </div>
              </div>

              {loading && (
                <div className="loading">
                  <div className="spinner"></div>
                  <span>Generating your recipe...</span>
                </div>
              )}

              {recipe && !loading && (
                <div className="recipe-output card">
                  <div className="recipe-output-header">
                    <h2>Your Recipe</h2>
                    <div className="recipe-output-actions">
                      <button
                        className="btn btn-secondary btn-small"
                        onClick={() => {
                          setSaveTitle('')
                          setShowSaveModal(true)
                        }}
                      >
                        Save Recipe
                      </button>
                    </div>
                  </div>
                  {recipe.dietary_filters?.length > 0 && (
                    <div className="tags">
                      {recipe.dietary_filters.map(f => (
                        <span key={f} className="tag">{f}</span>
                      ))}
                    </div>
                  )}
                  <div className="recipe-content" style={{ marginTop: '1rem' }}>
                    {recipe.recipe}
                  </div>
                </div>
              )}
            </>
          )}

          {/* Macros Tab */}
          {activeTab === 'macros' && (
            <>
              <div className="card">
                <h2>Generate from Macros</h2>
                <p style={{ marginBottom: '1rem', color: 'var(--color-text)' }}>
                  Enter your nutritional targets and get a recipe designed to meet them.
                </p>

                <div className="macro-inputs" style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem' }}>
                  <div className="form-group">
                    <label>Calories</label>
                    <input
                      type="number"
                      placeholder="e.g., 500"
                      value={macroCalories}
                      onChange={(e) => setMacroCalories(e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label>Protein (g)</label>
                    <input
                      type="number"
                      placeholder="e.g., 40"
                      value={macroProtein}
                      onChange={(e) => setMacroProtein(e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label>Carbs (g)</label>
                    <input
                      type="number"
                      placeholder="e.g., 50"
                      value={macroCarbs}
                      onChange={(e) => setMacroCarbs(e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label>Fat (g)</label>
                    <input
                      type="number"
                      placeholder="e.g., 20"
                      value={macroFat}
                      onChange={(e) => setMacroFat(e.target.value)}
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Dietary Filters (optional)</label>
                  <div className="checkbox-group">
                    {DIETARY_OPTIONS.map(filter => (
                      <label
                        key={filter}
                        className={`checkbox-item ${macroDietaryFilters.includes(filter) ? 'checked' : ''}`}
                      >
                        <input
                          type="checkbox"
                          checked={macroDietaryFilters.includes(filter)}
                          onChange={() => toggleMacroFilter(filter)}
                        />
                        {filter}
                      </label>
                    ))}
                  </div>
                </div>

                <button
                  className="btn btn-primary"
                  onClick={generateFromMacros}
                  disabled={loading}
                  style={{ marginTop: '1rem' }}
                >
                  {loading ? 'Generating...' : 'Generate Meal'}
                </button>
              </div>

              {loading && (
                <div className="loading">
                  <div className="spinner"></div>
                  <span>Creating your macro-targeted meal...</span>
                </div>
              )}

              {macroRecipe && !loading && (
                <div className="recipe-output card">
                  <div className="recipe-output-header">
                    <h2>Your Macro Meal</h2>
                  </div>
                  {macroRecipe.targets && (
                    <div className="tags" style={{ marginBottom: '1rem' }}>
                      {macroRecipe.targets.calories && <span className="tag">{macroRecipe.targets.calories} cal</span>}
                      {macroRecipe.targets.protein && <span className="tag">{macroRecipe.targets.protein}g protein</span>}
                      {macroRecipe.targets.carbs && <span className="tag">{macroRecipe.targets.carbs}g carbs</span>}
                      {macroRecipe.targets.fat && <span className="tag">{macroRecipe.targets.fat}g fat</span>}
                    </div>
                  )}
                  <div className="recipe-content">
                    {macroRecipe.recipe}
                  </div>
                </div>
              )}
            </>
          )}

          {/* Substitute Tab */}
          {activeTab === 'substitute' && (
            <div className="card">
              <h2>Ingredient Substitution</h2>
              <div className="substitution-form">
                <div className="form-group">
                  <label>Ingredient to substitute</label>
                  <input
                    type="text"
                    placeholder="e.g., butter, eggs, heavy cream"
                    value={subIngredient}
                    onChange={(e) => setSubIngredient(e.target.value)}
                  />
                </div>
                <div className="form-group">
                  <label>Context (optional)</label>
                  <input
                    type="text"
                    placeholder="e.g., baking cookies, making pasta sauce"
                    value={subContext}
                    onChange={(e) => setSubContext(e.target.value)}
                  />
                </div>
                <button
                  className="btn btn-primary"
                  onClick={getSubstitution}
                  disabled={loading}
                >
                  {loading ? 'Finding...' : 'Find Substitutes'}
                </button>

                {loading && (
                  <div className="loading">
                    <div className="spinner"></div>
                    <span>Finding substitutes...</span>
                  </div>
                )}

                {substitution && !loading && (
                  <div className="substitution-result">
                    <h3>Substitutes for {substitution.ingredient}</h3>
                    <div className="recipe-content" style={{ marginTop: '0.5rem' }}>
                      {substitution.suggestion}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Saved Tab */}
          {activeTab === 'saved' && (
            <div className="card">
              <h2>Saved Recipes</h2>
              {savedRecipes.length === 0 ? (
                <div className="empty-state">
                  <h3>No saved recipes yet</h3>
                  <p>Generate a recipe and save it to see it here!</p>
                </div>
              ) : (
                <div className="recipe-list">
                  {savedRecipes.map(r => (
                    <div key={r.id} className="recipe-item">
                      <div className="recipe-item-info">
                        <h3>{r.title}</h3>
                        <p>{r.ingredients?.slice(0, 4).join(', ')}{r.ingredients?.length > 4 ? '...' : ''}</p>
                        {r.dietary_filters?.length > 0 && (
                          <div className="tags">
                            {r.dietary_filters.map(f => (
                              <span key={f} className="tag">{f}</span>
                            ))}
                          </div>
                        )}
                      </div>
                      <div className="recipe-item-actions">
                        <button
                          className="btn btn-secondary btn-small"
                          onClick={() => setViewingRecipe(r)}
                        >
                          View
                        </button>
                        <button
                          className="btn btn-danger btn-small"
                          onClick={() => deleteRecipe(r.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </main>

        {/* Save Modal */}
        {showSaveModal && (
          <div className="modal-overlay" onClick={() => setShowSaveModal(false)}>
            <div className="modal" onClick={e => e.stopPropagation()}>
              <h2>Save Recipe</h2>
              <div className="save-form">
                <div className="form-group">
                  <label>Recipe Title</label>
                  <input
                    type="text"
                    placeholder="Enter a title for this recipe"
                    value={saveTitle}
                    onChange={(e) => setSaveTitle(e.target.value)}
                    autoFocus
                  />
                </div>
                <div className="modal-actions">
                  <button
                    className="btn btn-secondary"
                    onClick={() => setShowSaveModal(false)}
                  >
                    Cancel
                  </button>
                  <button
                    className="btn btn-primary"
                    onClick={saveRecipe}
                    disabled={!saveTitle.trim()}
                  >
                    Save
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* View Recipe Modal */}
        {viewingRecipe && (
          <div className="modal-overlay" onClick={() => setViewingRecipe(null)}>
            <div className="modal" onClick={e => e.stopPropagation()}>
              <h2>{viewingRecipe.title}</h2>
              {viewingRecipe.dietary_filters?.length > 0 && (
                <div className="tags" style={{ marginBottom: '1rem' }}>
                  {viewingRecipe.dietary_filters.map(f => (
                    <span key={f} className="tag">{f}</span>
                  ))}
                </div>
              )}
              <div className="recipe-content">
                {viewingRecipe.content}
              </div>
              <div className="modal-actions">
                <button
                  className="btn btn-secondary"
                  onClick={() => setViewingRecipe(null)}
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
