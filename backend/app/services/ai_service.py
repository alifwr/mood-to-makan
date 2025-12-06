from typing import List, Optional
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from app.models.store import Store
from app.models.food import Food
from app.models.user_food_history import UserFoodHistory
from sqlalchemy import text, func, and_
from sqlalchemy.orm import Session

# Initialize AI clients (supports both OpenRouter and Gemini)
embeddings = None
llm = None

# Try OpenRouter first
if settings.OPENROUTER_API_KEY:
    try:
        embeddings = OpenAIEmbeddings(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            model=settings.OPENROUTER_EMBEDDING_MODEL
        )
        llm = ChatOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            model=settings.OPENROUTER_MODEL
        )
        print("✅ AI Service initialized with OpenRouter")
    except Exception as e:
        print(f"⚠️ OpenRouter initialization failed: {e}")

# Fallback to Gemini if OpenRouter not available
if not llm and settings.GEMINI_API_KEY:
    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.GEMINI_EMBEDDING_MODEL,
            google_api_key=settings.GEMINI_API_KEY
        )
        llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GEMINI_API_KEY
        )
        print("✅ AI Service initialized with Gemini")
    except Exception as e:
        print(f"⚠️ Gemini initialization failed: {e}")

if not llm:
    print("⚠️ No AI provider configured. Set either OPENROUTER_API_KEY or GEMINI_API_KEY in .env")




def generate_embedding(text_content: str) -> List[float]:
    """Generate embedding vector, padding to 1536 dimensions if needed"""
    if not embeddings:
        # Mock for dev/test
        return [0.0] * 1536
    
    try:
        # Clean text
        cleaned_text = text_content.replace("\n", " ")
        embedding_vector = embeddings.embed_query(cleaned_text)
        
        # Pad to 1536 dimensions if needed (for Gemini which returns 768)
        if len(embedding_vector) < 1536:
            padding = [0.0] * (1536 - len(embedding_vector))
            embedding_vector = embedding_vector + padding
        # Truncate if longer (shouldn't happen but just in case)
        elif len(embedding_vector) > 1536:
            embedding_vector = embedding_vector[:1536]
            
        return embedding_vector
    except Exception as e:
        print(f"Embedding Error: {e}")
        return [0.0] * 1536


def search_stores_by_vector(query: str, db, limit: int = 5):
    query_vector = generate_embedding(query)
    
    # pgvector search using cosine distance (<=>)
    # We search both stores and products? 
    # Let's start with Stores.
    
    # SQL alchemy with pgvector
    # Note: We need to cast the list to a vector string representation for raw SQL if needed,
    # or use the ORM's order_by with the operator.
    
    # Using ORM:
    stores = db.query(Store).order_by(
        Store.embedding.cosine_distance(query_vector)
    ).limit(limit).all()
    
    return stores

def recommend_food(user_preferences: str, db):
    if not llm:
        return "AI service not configured."
        
    # 1. Search for relevant stores/products first (RAG)
    # For simplicity, let's just search stores based on preferences
    relevant_stores = search_stores_by_vector(user_preferences, db, limit=3)
    
    context = "\n".join([f"- {s.name}: {s.description} ({s.address})" for s in relevant_stores])
    
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful food recommendation assistant for 'Mood2Makan'.
    
    User Preferences: {preferences}
    
    Here are some nearby/relevant stores found in our database:
    {context}
    
    Based on the user's preferences and the available stores, suggest where they should eat and what they might like.
    If no stores seem relevant, give a general suggestion but mention we might not have a perfect match nearby.
    """)
    
    chain = prompt | llm | StrOutputParser()
    
    return chain.invoke({"preferences": user_preferences, "context": context})


# ========== FOOD-SPECIFIC FUNCTIONS ==========

def generate_food_embedding(food_data: dict) -> List[float]:
    """Generate embedding from food attributes"""
    # Combine all relevant food attributes into a rich text description
    text_parts = [
        f"Food: {food_data.get('name', '')}",
        f"Description: {food_data.get('description', '')}",
        f"Category: {food_data.get('category', '')}",
        f"Ingredients: {', '.join(food_data.get('main_ingredients', []))}",
        f"Taste: {', '.join(food_data.get('taste_profile', []))}",
        f"Texture: {', '.join(food_data.get('texture', []))}",
        f"Mood: {', '.join(food_data.get('mood_tags', []))}"
    ]
    
    combined_text = " | ".join(text_parts)
    return generate_embedding(combined_text)


def search_foods_by_vector(query: str, db: Session, limit: int = 10, 
                           category: Optional[str] = None,
                           max_calories: Optional[float] = None) -> List[Food]:
    """Search foods using vector similarity"""
    try:
        query_vector = generate_embedding(query)
        
        # Build query with optional filters
        foods_query = db.query(Food)
        
        if category:
            foods_query = foods_query.filter(Food.category == category)
        
        if max_calories:
            foods_query = foods_query.filter(Food.calories <= max_calories)
        
        # Order by similarity
        foods = foods_query.order_by(
            Food.embedding.cosine_distance(query_vector)
        ).limit(limit).all()
        
        return foods
    except Exception as e:
        print(f"Error in search_foods_by_vector: {e}")
        # Fallback: return foods without vector search
        foods_query = db.query(Food)
        if category:
            foods_query = foods_query.filter(Food.category == category)
        if max_calories:
            foods_query = foods_query.filter(Food.calories <= max_calories)
        return foods_query.limit(limit).all()


def recommend_foods_by_mood(mood_description: str, db: Session, 
                            user_id: Optional[int] = None,
                            limit: int = 10) -> dict:
    """Get AI-powered food recommendations based on mood/preferences"""
    if not llm:
        # Fallback to vector search only
        foods = search_foods_by_vector(mood_description, db, limit=limit)
        return {
            "recommendations": foods,
            "explanation": "AI service not configured. Showing similar foods based on your description."
        }
    
    # 1. Get relevant foods using vector search
    relevant_foods = search_foods_by_vector(mood_description, db, limit=20)
    
    # 2. Get user history if available
    user_context = ""
    if user_id:
        user_history = db.query(UserFoodHistory).filter(
            UserFoodHistory.user_id == user_id
        ).order_by(UserFoodHistory.created_at.desc()).limit(10).all()
        
        if user_history:
            liked_foods = [h.food.name for h in user_history if h.rating and h.rating >= 4]
            if liked_foods:
                user_context = f"\nUser previously enjoyed: {', '.join(liked_foods[:5])}"
    
    # 3. Build context from relevant foods
    food_context = "\n".join([
        f"- {f.name} ({f.category}): {f.description or 'No description'}\n"
        f"  Taste: {', '.join(f.taste_profile)}, Texture: {', '.join(f.texture)}\n"
        f"  Mood tags: {', '.join(f.mood_tags or [])}"
        for f in relevant_foods[:10]
    ])
    
    # 4. Use LLM to generate personalized recommendations
    prompt = ChatPromptTemplate.from_template("""
    You are a food recommendation expert for 'Mood2Makan'.
    
    User's mood/preferences: {mood_description}
    {user_context}
    
    Available foods in our database:
    {food_context}
    
    Based on the user's mood and preferences, recommend 3-5 foods from the list above.
    For each recommendation, explain why it matches their mood/preferences.
    Be empathetic and consider how different foods can affect mood and satisfaction.
    
    Format your response as a friendly, conversational recommendation.
    """)
    
    chain = prompt | llm | StrOutputParser()
    
    explanation = chain.invoke({
        "mood_description": mood_description,
        "user_context": user_context,
        "food_context": food_context
    })
    
    return {
        "recommendations": relevant_foods[:limit],
        "explanation": explanation
    }


def get_personalized_recommendations(user_id: int, db: Session, limit: int = 10) -> List[Food]:
    """Get personalized food recommendations based on user history"""
    try:
        # Get user's interaction history
        user_history = db.query(UserFoodHistory).filter(
            UserFoodHistory.user_id == user_id
        ).all()
        
        if not user_history:
            # No history, return popular foods
            return db.query(Food).limit(limit).all()
        
        # Analyze user preferences
        liked_food_ids = [h.food_id for h in user_history if h.rating and h.rating >= 4]
        
        if not liked_food_ids:
            # No highly rated foods, use all interactions
            liked_food_ids = [h.food_id for h in user_history]
        
        if not liked_food_ids:
            # Still no foods, return random
            return db.query(Food).limit(limit).all()
        
        # Get liked foods
        liked_foods = db.query(Food).filter(Food.id.in_(liked_food_ids)).all()
        
        if not liked_foods:
            return db.query(Food).limit(limit).all()
        
        # Extract common attributes
        all_taste_profiles = []
        all_mood_tags = []
        all_categories = []
        
        for food in liked_foods:
            if food.taste_profile:
                all_taste_profiles.extend(food.taste_profile)
            if food.mood_tags:
                all_mood_tags.extend(food.mood_tags)
            if food.category:
                all_categories.append(food.category)
        
        # Find foods with similar attributes that user hasn't tried
        tried_food_ids = [h.food_id for h in user_history]
        
        # Build query for similar foods
        similar_foods = db.query(Food).filter(
            ~Food.id.in_(tried_food_ids)
        )
        
        # Filter by common categories or taste profiles
        if all_categories:
            most_common_category = max(set(all_categories), key=all_categories.count)
            similar_foods = similar_foods.filter(Food.category == most_common_category)
        
        return similar_foods.limit(limit).all()
    except Exception as e:
        print(f"Error in get_personalized_recommendations: {e}")
        # Fallback: return random foods
        return db.query(Food).limit(limit).all()


# ========== FOOD DESCRIPTION GENERATION FUNCTIONS ==========

def generate_food_description(
    name: str,
    category: str,
    main_ingredients: Optional[List[str]] = None,
    taste_profile: Optional[List[str]] = None,
    texture: Optional[List[str]] = None,
    region: Optional[str] = None,
    selling_points: Optional[List[str]] = None,
    style: str = "promotional",
    language: str = "en",
    db: Optional[Session] = None
) -> dict:
    """
    Generate compelling food descriptions using AI.
    Returns short description, long description, selling points, and flavor characteristics.
    """
    if not llm:
        return {
            "short_description": f"{name} - A delicious {category.replace('_', ' ')}",
            "long_description": f"{name} is a wonderful {category.replace('_', ' ')} that you'll love.",
            "selling_points": selling_points or [],
            "flavor_characteristics": {}
        }
    
    # Get promotional keywords if db is available
    promotional_keywords = []
    if db:
        from app.models.promotional_keyword import PromotionalKeyword
        keywords_data = db.query(PromotionalKeyword).filter(
            PromotionalKeyword.category.in_([category, "all"])
        ).all()
        for kw in keywords_data:
            promotional_keywords.extend(kw.keywords)
    
    # Build context
    context_parts = [f"Food Name: {name}", f"Category: {category.replace('_', ' ')}"]
    
    if main_ingredients:
        context_parts.append(f"Main Ingredients: {', '.join(main_ingredients)}")
    if taste_profile:
        context_parts.append(f"Taste Profile: {', '.join(taste_profile)}")
    if texture:
        context_parts.append(f"Texture: {', '.join(texture)}")
    if region:
        context_parts.append(f"Region of Origin: {region}")
    if selling_points:
        context_parts.append(f"Key Selling Points: {', '.join(selling_points)}")
    
    context = "\n".join(context_parts)
    
    # Determine style instructions
    style_instructions = {
        "promotional": "Write in an engaging, marketing-focused style that highlights the food's appeal and makes people want to try it.",
        "informational": "Write in a clear, factual style that educates readers about the food.",
        "casual": "Write in a friendly, conversational style as if recommending to a friend."
    }
    
    style_instruction = style_instructions.get(style, style_instructions["promotional"])
    
    # Create prompt
    prompt = ChatPromptTemplate.from_template("""
    You are an expert food writer and marketing copywriter. Generate compelling food descriptions.
    
    Food Information:
    {context}
    
    Available Promotional Keywords (use naturally if relevant): {keywords}
    
    Style: {style_instruction}
    Language: {language}
    
    Generate the following:
    
    1. SHORT DESCRIPTION (1-2 sentences, ~30-50 words):
    - Concise and impactful
    - Highlight the most appealing aspects
    - Perfect for menus or quick listings
    
    2. LONG DESCRIPTION (1 paragraph, ~80-120 words):
    - Detailed and evocative
    - Tell a story about the food
    - Include sensory details (taste, aroma, texture, appearance)
    - Mention preparation method if relevant
    - Create desire and appetite appeal
    
    3. SELLING POINTS (3-5 bullet points):
    - Key features that make this food special
    - What sets it apart
    - Benefits to the customer
    
    4. FLAVOR CHARACTERISTICS:
    - Primary flavors
    - Secondary flavors
    - Texture description
    - Aroma notes
    
    Format your response as JSON:
    {{
        "short_description": "...",
        "long_description": "...",
        "selling_points": ["...", "...", "..."],
        "flavor_characteristics": {{
            "primary_flavors": ["...", "..."],
            "secondary_flavors": ["...", "..."],
            "texture_description": "...",
            "aroma_notes": "..."
        }}
    }}
    """)
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        result = chain.invoke({
            "context": context,
            "keywords": ", ".join(promotional_keywords[:15]) if promotional_keywords else "N/A",
            "style_instruction": style_instruction,
            "language": language
        })
        
        # Parse JSON response
        import json
        # Try to extract JSON from response
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0].strip()
        elif "```" in result:
            result = result.split("```")[1].split("```")[0].strip()
        
        parsed = json.loads(result)
        return parsed
        
    except Exception as e:
        print(f"Description generation error: {e}")
        # Fallback
        return {
            "short_description": f"Delicious {name} from {region or 'our kitchen'}. {' '.join(taste_profile[:2]) if taste_profile else 'A must-try dish'}.",
            "long_description": f"Experience the authentic taste of {name}, a {category.replace('_', ' ')} that combines {', '.join(main_ingredients[:3]) if main_ingredients else 'quality ingredients'}. {'Featuring ' + ', '.join(taste_profile) if taste_profile else 'Perfectly prepared'} to deliver an unforgettable dining experience.",
            "selling_points": selling_points or ["High quality ingredients", "Expertly prepared", "Authentic recipe"],
            "flavor_characteristics": {
                "primary_flavors": taste_profile[:2] if taste_profile else [],
                "secondary_flavors": taste_profile[2:] if taste_profile and len(taste_profile) > 2 else [],
                "texture_description": ", ".join(texture) if texture else "Perfect texture",
                "aroma_notes": "Aromatic and inviting"
            }
        }


def enhance_food_description(
    current_description: str,
    food_name: str,
    category: str,
    enhance_for: str = "promotional",
    additional_info: Optional[dict] = None
) -> str:
    """
    Enhance an existing food description using AI.
    """
    if not llm:
        return current_description
    
    enhancement_goals = {
        "promotional": "Make it more engaging and marketing-focused to drive sales",
        "seo": "Optimize for search engines while maintaining readability and appeal",
        "detailed": "Add more sensory details and descriptive language"
    }
    
    goal = enhancement_goals.get(enhance_for, enhancement_goals["promotional"])
    
    additional_context = ""
    if additional_info:
        additional_context = "\n".join([f"{k}: {v}" for k, v in additional_info.items()])
    
    prompt = ChatPromptTemplate.from_template("""
    You are an expert food writer. Enhance the following food description.
    
    Food Name: {food_name}
    Category: {category}
    Current Description: {current_description}
    
    {additional_context}
    
    Enhancement Goal: {goal}
    
    Rewrite the description to be more compelling, vivid, and appealing.
    Maintain accuracy but enhance the language to be more evocative and appetizing.
    Keep the same general length but improve quality and impact.
    
    Enhanced Description:
    """)
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        enhanced = chain.invoke({
            "food_name": food_name,
            "category": category,
            "current_description": current_description,
            "additional_context": additional_context,
            "goal": goal
        })
        return enhanced.strip()
    except Exception as e:
        print(f"Enhancement error: {e}")
        return current_description


def generate_description_from_image(
    image_data: bytes,
    name: str,
    category: str,
    region: Optional[str] = None,
    style: str = "promotional"
) -> dict:
    """
    Generate food description from an image using vision-capable LLM.
    Note: Requires vision-capable model like GPT-4 Vision or Gemini Vision.
    """
    # This is a placeholder - actual implementation would use vision models
    # For now, return a basic description
    if not llm:
        return {
            "short_description": f"{name} - A delicious {category.replace('_', ' ')}",
            "long_description": f"This appetizing {name} looks absolutely delicious.",
            "selling_points": ["Visually appealing", "Fresh ingredients", "Expertly presented"],
            "flavor_characteristics": {}
        }
    
    # TODO: Implement actual vision model integration
    # This would involve:
    # 1. Encoding image to base64
    # 2. Using vision-capable model (GPT-4V, Gemini Vision, etc.)
    # 3. Analyzing the image for ingredients, presentation, colors, etc.
    # 4. Generating description based on visual analysis
    
    return {
        "short_description": f"Beautifully presented {name} that looks as good as it tastes",
        "long_description": f"This stunning {name} showcases the artistry of {region or 'our'} cuisine. The careful presentation and vibrant colors promise a delightful culinary experience.",
        "selling_points": ["Instagram-worthy presentation", "Fresh, quality ingredients", "Authentic preparation"],
        "flavor_characteristics": {
            "primary_flavors": [],
            "secondary_flavors": [],
            "texture_description": "Appealing texture",
            "aroma_notes": "Aromatic"
        },
        "note": "Image analysis feature coming soon - using basic description for now"
    }


def get_promotional_keywords_for_category(category: str, db: Session) -> dict:
    """
    Retrieve promotional keywords grouped by type for a specific category.
    """
    from app.models.promotional_keyword import PromotionalKeyword
    
    keywords_data = db.query(PromotionalKeyword).filter(
        PromotionalKeyword.category.in_([category, "all"])
    ).all()
    
    grouped = {
        "selling_points": [],
        "flavors": [],
        "textures": [],
        "moods": [],
        "general": []
    }
    
    for kw in keywords_data:
        keyword_type = kw.keyword_type
        if keyword_type == "selling_point":
            grouped["selling_points"].extend(kw.keywords)
        elif keyword_type == "flavor":
            grouped["flavors"].extend(kw.keywords)
        elif keyword_type == "texture":
            grouped["textures"].extend(kw.keywords)
        elif keyword_type == "mood":
            grouped["moods"].extend(kw.keywords)
        else:
            grouped["general"].extend(kw.keywords)
    
    return grouped


# ========== REVIEW ANALYSIS FUNCTIONS ==========

def analyze_review_sentiment(review_text: str, rating: int) -> dict:
    """
    Analyze sentiment of a review using AI.
    Returns sentiment score, label, and confidence.
    """
    if not llm:
        # Fallback based on rating
        if rating >= 4:
            return {"score": 0.7, "label": "positive", "confidence": 0.6}
        elif rating <= 2:
            return {"score": -0.7, "label": "negative", "confidence": 0.6}
        else:
            return {"score": 0.0, "label": "neutral", "confidence": 0.6}
    
    prompt = ChatPromptTemplate.from_template("""
    Analyze the sentiment of this customer review.
    
    Review Text: {review_text}
    Rating: {rating}/5
    
    Provide sentiment analysis in JSON format:
    {{
        "score": <float from -1.0 (very negative) to 1.0 (very positive)>,
        "label": "<positive|neutral|negative>",
        "confidence": <float from 0.0 to 1.0>,
        "reasoning": "<brief explanation>"
    }}
    
    Consider both the text and the rating. The score should reflect the overall sentiment.
    """)
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        result = chain.invoke({"review_text": review_text, "rating": rating})
        
        import json
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0].strip()
        elif "```" in result:
            result = result.split("```")[1].split("```")[0].strip()
        
        parsed = json.loads(result)
        return parsed
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        # Fallback
        score = (rating - 3) / 2  # Convert 1-5 rating to -1 to 1 scale
        label = "positive" if score > 0.3 else ("negative" if score < -0.3 else "neutral")
        return {"score": score, "label": label, "confidence": 0.5}


def categorize_review_problems(review_text: str, rating: int, db: Session) -> list:
    """
    Identify problem categories in a review.
    Returns list of detected problems with severity and confidence.
    """
    from app.models.problem_category import ProblemCategory
    
    # Get active problem categories
    categories = db.query(ProblemCategory).filter(ProblemCategory.is_active == True).all()
    
    if not categories or not llm:
        return []
    
    # Build category descriptions
    category_info = "\n".join([
        f"- {cat.category_key}: {cat.description} (Keywords: {', '.join(cat.keywords[:5])})"
        for cat in categories
    ])
    
    prompt = ChatPromptTemplate.from_template("""
    Analyze this customer review and identify any problems mentioned.
    
    Review Text: {review_text}
    Rating: {rating}/5
    
    Available Problem Categories:
    {categories}
    
    For each problem you detect, provide:
    - category: the category_key
    - severity: 0.0 to 1.0 (how serious the problem is)
    - confidence: 0.0 to 1.0 (how confident you are)
    - evidence: the specific text that indicates this problem
    
    Return as JSON array:
    [
        {{
            "category": "category_key",
            "severity": 0.8,
            "confidence": 0.9,
            "evidence": "relevant quote from review"
        }}
    ]
    
    If no problems are detected, return an empty array [].
    Only include problems that are clearly mentioned or strongly implied.
    """)
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        result = chain.invoke({
            "review_text": review_text,
            "rating": rating,
            "categories": category_info
        })
        
        import json
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0].strip()
        elif "```" in result:
            result = result.split("```")[1].split("```")[0].strip()
        
        problems = json.loads(result)
        
        # Add category names
        category_map = {cat.category_key: cat.name for cat in categories}
        for problem in problems:
            problem["category_name"] = category_map.get(problem["category"], problem["category"])
        
        return problems
    except Exception as e:
        print(f"Problem categorization error: {e}")
        return []


def extract_review_topics(review_text: str) -> list:
    """
    Extract key topics/themes from a review.
    """
    if not llm:
        return []
    
    prompt = ChatPromptTemplate.from_template("""
    Extract the main topics or themes discussed in this review.
    
    Review: {review_text}
    
    Return 3-5 key topics as a JSON array of strings.
    Topics should be short phrases (2-4 words each).
    
    Example: ["food quality", "delivery time", "packaging", "customer service"]
    
    Return only the JSON array, nothing else.
    """)
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        result = chain.invoke({"review_text": review_text})
        
        import json
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0].strip()
        elif "```" in result:
            result = result.split("```")[1].split("```")[0].strip()
        elif "[" in result:
            # Extract just the array
            start = result.find("[")
            end = result.rfind("]") + 1
            result = result[start:end]
        
        topics = json.loads(result)
        return topics if isinstance(topics, list) else []
    except Exception as e:
        print(f"Topic extraction error: {e}")
        return []


def generate_improvement_suggestions(problems: list, db: Session) -> list:
    """
    Generate actionable improvement suggestions based on detected problems.
    """
    from app.models.problem_category import ProblemCategory
    
    if not problems or not llm:
        return []
    
    # Get problem category details
    category_keys = [p["category"] for p in problems]
    categories = db.query(ProblemCategory).filter(
        ProblemCategory.category_key.in_(category_keys)
    ).all()
    
    category_map = {cat.category_key: cat for cat in categories}
    
    # Build context
    problem_context = "\n".join([
        f"- {p['category']}: Severity {p['severity']:.1f}, Evidence: \"{p.get('evidence', 'N/A')}\""
        for p in problems
    ])
    
    prompt = ChatPromptTemplate.from_template("""
    Based on these problems detected in customer reviews, generate specific, actionable improvement suggestions.
    
    Problems Detected:
    {problems}
    
    For each problem, provide:
    - A specific, actionable suggestion
    - Priority level (high/medium/low)
    - Expected impact if implemented
    
    Return as JSON array:
    [
        {{
            "problem": "category_key",
            "suggestion": "Specific action to take",
            "priority": "high",
            "expected_impact": "What will improve"
        }}
    ]
    
    Make suggestions practical and specific to the food/restaurant business.
    """)
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        result = chain.invoke({"problems": problem_context})
        
        import json
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0].strip()
        elif "```" in result:
            result = result.split("```")[1].split("```")[0].strip()
        
        suggestions = json.loads(result)
        return suggestions if isinstance(suggestions, list) else []
    except Exception as e:
        print(f"Suggestion generation error: {e}")
        # Fallback suggestions
        return [
            {
                "problem": p["category"],
                "suggestion": f"Address {p['category'].replace('_', ' ')} issues mentioned in reviews",
                "priority": "high" if p["severity"] > 0.7 else "medium",
                "expected_impact": "Improved customer satisfaction"
            }
            for p in problems
        ]


# def aggregate_store_insights(store_id: int, db: Session, days: Optional[int] = None) -> dict:
#     """
#     Aggregate insights from all reviews for a store.
#     """
#     from app.models.review import Review
#     from app.models.review_analysis import ReviewAnalysis
#     from app.models.store import Store
#     from datetime import datetime, timedelta
    
#     store = db.query(Store).filter(Store.id == store_id).first()
#     if not store:
#         return {}
    
#     # Build query
#     query = db.query(Review).filter(Review.store_id == store_id)
    
#     if days:
#         cutoff_date = datetime.utcnow() - timedelta(days=days)
#         query = query.filter(Review.created_at >= cutoff_date)
    
#     reviews = query.all()
    
#     if not reviews:
#         return {
#             "store_id": store_id,
#             "store_name": store.name,
#             "total_reviews": 0,
#             "message": "No reviews found"
#         }
    
#     # Calculate metrics
#     total_reviews = len(reviews)
#     average_rating = sum(r.rating for r in reviews) / total_reviews
    
#     # Sentiment distribution
#     sentiment_dist = {"positive": 0, "neutral": 0, "negative": 0, "total": total_reviews}
#     for review in reviews:
#         if review.sentiment_label:
#             sentiment_dist[review.sentiment_label] = sentiment_dist.get(review.sentiment_label, 0) + 1
    
#     # Aggregate problems
#     problem_counts = {}
#     for review in reviews:
#         analysis = db.query(ReviewAnalysis).filter(ReviewAnalysis.review_id == review.id).first()
#         if analysis and analysis.detected_problems:
#             for problem_key in analysis.detected_problems:
#                 problem_counts[problem_key] = problem_counts.get(problem_key, 0) + 1
    
#     # Top problems
#     top_problems = [
#         {
#             "category": cat,
#             "occurrences": count,
#             "percentage": (count / total_reviews) * 100
#         }
#         for cat, count in sorted(problem_counts.items(), key=lambda x: x[1], reverse=True)[:5]
#     ]
    
#     return {
#         "store_id": store_id,
#         "store_name": store.name,
#         "total_reviews": total_reviews,
#         "average_rating": round(average_rating, 2),
#         "sentiment_distribution": sentiment_dist,
#         "top_problems": top_problems
#     }
