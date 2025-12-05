"""
Robust seed script for food data with individual commits.
Run this script to populate the database with sample food items.
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from sqlalchemy import func
from app.core.database import SessionLocal
from app.models.food import Food
from app.services import ai_service

# Sample food data
SAMPLE_FOODS = [
    # Indonesian Main Meals
    {
        "name": "Nasi Goreng",
        "description": "Indonesian fried rice with sweet soy sauce, vegetables, and egg",
        "category": "main_meals",
        "main_ingredients": ["rice", "egg", "vegetables", "sweet soy sauce", "chicken"],
        "taste_profile": ["savory", "sweet", "umami"],
        "texture": ["soft", "slightly crispy"],
        "mood_tags": ["comfort", "energetic", "happy"],
        "calories": 450,
        "protein": 15,
        "carbs": 65,
        "fat": 12,
    },
    {
        "name": "Rendang",
        "description": "Slow-cooked beef in rich coconut and spice curry",
        "category": "main_meals",
        "main_ingredients": ["beef", "coconut milk", "lemongrass", "galangal", "chili"],
        "taste_profile": ["spicy", "savory", "rich", "creamy"],
        "texture": ["tender", "soft"],
        "mood_tags": ["comfort", "indulgent", "celebration"],
        "calories": 550,
        "protein": 35,
        "carbs": 15,
        "fat": 38,
    },
    {
        "name": "Sate Ayam",
        "description": "Grilled chicken skewers with peanut sauce",
        "category": "main_meals",
        "main_ingredients": ["chicken", "peanut sauce", "sweet soy sauce"],
        "taste_profile": ["savory", "sweet", "nutty"],
        "texture": ["tender", "slightly charred"],
        "mood_tags": ["happy", "social", "energetic"],
        "calories": 380,
        "protein": 28,
        "carbs": 20,
        "fat": 18,
    },
    {
        "name": "Gado-gado",
        "description": "Indonesian vegetable salad with peanut sauce",
        "category": "main_meals",
        "main_ingredients": ["vegetables", "tofu", "tempeh", "peanut sauce", "egg"],
        "taste_profile": ["savory", "fresh", "nutty"],
        "texture": ["crunchy", "soft"],
        "mood_tags": ["healthy", "fresh", "light"],
        "calories": 320,
        "protein": 18,
        "carbs": 35,
        "fat": 14,
    },
    {
        "name": "Mie Goreng",
        "description": "Indonesian fried noodles with vegetables and protein",
        "category": "main_meals",
        "main_ingredients": ["noodles", "vegetables", "egg", "chicken", "sweet soy sauce"],
        "taste_profile": ["savory", "sweet", "umami"],
        "texture": ["chewy", "soft"],
        "mood_tags": ["comfort", "quick", "satisfying"],
        "calories": 420,
        "protein": 16,
        "carbs": 58,
        "fat": 14,
    },
    
    # Indonesian Snacks
    {
        "name": "Pisang Goreng",
        "description": "Crispy fried banana fritters",
        "category": "snacks",
        "main_ingredients": ["banana", "flour", "sugar"],
        "taste_profile": ["sweet", "savory"],
        "texture": ["crispy", "soft"],
        "mood_tags": ["comfort", "nostalgic", "happy"],
        "calories": 180,
        "protein": 3,
        "carbs": 32,
        "fat": 6,
    },
    {
        "name": "Martabak Manis",
        "description": "Sweet thick pancake with various toppings",
        "category": "snacks",
        "main_ingredients": ["flour", "chocolate", "cheese", "peanuts", "condensed milk"],
        "taste_profile": ["sweet", "rich"],
        "texture": ["soft", "fluffy"],
        "mood_tags": ["indulgent", "happy", "celebration"],
        "calories": 520,
        "protein": 12,
        "carbs": 68,
        "fat": 22,
    },
    {
        "name": "Keripik Tempe",
        "description": "Crispy fried tempeh chips",
        "category": "snacks",
        "main_ingredients": ["tempeh", "spices"],
        "taste_profile": ["savory", "umami"],
        "texture": ["crispy", "crunchy"],
        "mood_tags": ["energetic", "snacking"],
        "calories": 160,
        "protein": 8,
        "carbs": 15,
        "fat": 8,
    },
    
    # Indonesian Drinks
    {
        "name": "Es Teler",
        "description": "Mixed fruit cocktail with coconut milk and condensed milk",
        "category": "drinks",
        "main_ingredients": ["avocado", "jackfruit", "coconut", "condensed milk", "ice"],
        "taste_profile": ["sweet", "creamy", "fresh"],
        "texture": ["smooth", "chunky"],
        "mood_tags": ["refreshing", "tropical", "happy"],
        "calories": 280,
        "protein": 4,
        "carbs": 45,
        "fat": 12,
    },
    {
        "name": "Es Cendol",
        "description": "Iced sweet dessert with pandan jelly, coconut milk, and palm sugar",
        "category": "drinks",
        "main_ingredients": ["pandan jelly", "coconut milk", "palm sugar", "ice"],
        "taste_profile": ["sweet", "creamy"],
        "texture": ["chewy", "smooth"],
        "mood_tags": ["refreshing", "comfort", "nostalgic"],
        "calories": 220,
        "protein": 2,
        "carbs": 42,
        "fat": 8,
    },
    {
        "name": "Teh Tarik",
        "description": "Pulled milk tea with condensed milk",
        "category": "drinks",
        "main_ingredients": ["black tea", "condensed milk"],
        "taste_profile": ["sweet", "creamy"],
        "texture": ["smooth", "frothy"],
        "mood_tags": ["comfort", "energetic", "social"],
        "calories": 180,
        "protein": 4,
        "carbs": 28,
        "fat": 6,
    },
    
    # Indonesian Desserts
    {
        "name": "Klepon",
        "description": "Sweet rice cake balls filled with palm sugar and coated in coconut",
        "category": "desserts",
        "main_ingredients": ["glutinous rice flour", "palm sugar", "coconut", "pandan"],
        "taste_profile": ["sweet"],
        "texture": ["chewy", "soft"],
        "mood_tags": ["happy", "nostalgic", "comfort"],
        "calories": 150,
        "protein": 2,
        "carbs": 32,
        "fat": 3,
    },
    {
        "name": "Es Krim Kopyor",
        "description": "Coconut ice cream with young coconut meat",
        "category": "desserts",
        "main_ingredients": ["coconut", "milk", "sugar"],
        "taste_profile": ["sweet", "creamy", "fresh"],
        "texture": ["smooth", "chunky"],
        "mood_tags": ["refreshing", "indulgent", "happy"],
        "calories": 240,
        "protein": 3,
        "carbs": 35,
        "fat": 11,
    },
    
    # International Foods
    {
        "name": "Chicken Soup",
        "description": "Warm comforting chicken soup with vegetables",
        "category": "main_meals",
        "main_ingredients": ["chicken", "vegetables", "broth", "noodles"],
        "taste_profile": ["savory", "umami"],
        "texture": ["soft"],
        "mood_tags": ["comfort", "sick", "warm", "healing"],
        "calories": 180,
        "protein": 18,
        "carbs": 15,
        "fat": 6,
    },
    {
        "name": "Chocolate Cake",
        "description": "Rich moist chocolate cake",
        "category": "desserts",
        "main_ingredients": ["chocolate", "flour", "sugar", "eggs", "butter"],
        "taste_profile": ["sweet", "rich"],
        "texture": ["soft", "moist"],
        "mood_tags": ["indulgent", "celebration", "happy", "stressed"],
        "calories": 450,
        "protein": 6,
        "carbs": 58,
        "fat": 24,
    },
    {
        "name": "Caesar Salad",
        "description": "Fresh romaine lettuce with Caesar dressing and croutons",
        "category": "main_meals",
        "main_ingredients": ["romaine lettuce", "parmesan", "croutons", "Caesar dressing"],
        "taste_profile": ["savory", "fresh", "tangy"],
        "texture": ["crunchy", "crispy"],
        "mood_tags": ["healthy", "fresh", "light"],
        "calories": 280,
        "protein": 12,
        "carbs": 18,
        "fat": 18,
    },
    {
        "name": "Iced Coffee",
        "description": "Cold brew coffee with ice",
        "category": "drinks",
        "main_ingredients": ["coffee", "ice", "milk", "sugar"],
        "taste_profile": ["bitter", "sweet"],
        "texture": ["smooth"],
        "mood_tags": ["energetic", "focused", "tired"],
        "calories": 120,
        "protein": 2,
        "carbs": 18,
        "fat": 4,
    },
    {
        "name": "Spicy Ramen",
        "description": "Hot and spicy Japanese noodle soup",
        "category": "main_meals",
        "main_ingredients": ["noodles", "broth", "egg", "vegetables", "chili"],
        "taste_profile": ["spicy", "savory", "umami"],
        "texture": ["chewy", "soft"],
        "mood_tags": ["comfort", "warm", "adventurous", "stressed"],
        "calories": 480,
        "protein": 22,
        "carbs": 62,
        "fat": 16,
    },
    {
        "name": "Smoothie Bowl",
        "description": "Thick fruit smoothie topped with granola and fresh fruits",
        "category": "desserts",
        "main_ingredients": ["banana", "berries", "yogurt", "granola", "honey"],
        "taste_profile": ["sweet", "fresh"],
        "texture": ["smooth", "crunchy"],
        "mood_tags": ["healthy", "energetic", "fresh", "happy"],
        "calories": 320,
        "protein": 8,
        "carbs": 58,
        "fat": 8,
    },
]


def seed_foods():
    """Seed the database with sample food data - commits each food individually"""
    db = SessionLocal()
    
    try:
        # Check if foods already exist
        existing_count = db.query(Food).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} foods.")
            response = input("Delete and reseed? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("Cancelled")
                return
            
            print(f"Deleting {existing_count} existing foods...")
            db.query(Food).delete()
            db.commit()
            print("✅ Deleted")
        
        print("\nSeeding food data...")
        print("=" * 60)
        
        success_count = 0
        fail_count = 0
        
        for i, food_data in enumerate(SAMPLE_FOODS, 1):
            try:
                print(f"[{i}/{len(SAMPLE_FOODS)}] Creating: {food_data['name']}", end="... ")
                
                # Generate embedding
                embedding = ai_service.generate_food_embedding(food_data)
                
                # Create food object
                food = Food(
                    **food_data,
                    embedding=embedding
                )
                
                db.add(food)
                db.commit()  # Commit each food individually
                db.refresh(food)
                
                print(f"✅ (ID: {food.id})")
                success_count += 1
                
            except Exception as e:
                print(f"❌ Failed: {str(e)[:50]}")
                db.rollback()
                fail_count += 1
                continue
        
        print("=" * 60)
        print(f"\n✅ Successfully seeded {success_count}/{len(SAMPLE_FOODS)} foods!")
        if fail_count > 0:
            print(f"⚠️  {fail_count} foods failed to seed")
        
        # Print summary
        categories = db.query(Food.category, func.count(Food.id)).group_by(Food.category).all()
        print("\n📊 Food distribution by category:")
        for category, count in categories:
            print(f"   {category}: {count}")
        
    except Exception as e:
        print(f"\n❌ Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_foods()
