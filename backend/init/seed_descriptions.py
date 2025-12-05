"""
Seed script for description templates and promotional keywords.
Run this script to populate the database with templates and keywords for description generation.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.description_template import DescriptionTemplate
from app.models.promotional_keyword import PromotionalKeyword

# Sample description templates
DESCRIPTION_TEMPLATES = [
    # Main Meals Templates
    {
        "name": "Main Meals - Promotional",
        "category": "main_meals",
        "use_case": "promotional",
        "language": "en",
        "short_template": "Authentic [region] [name] featuring [ingredients]. [selling_point]. Perfect for [mood].",
        "long_template": "Experience the authentic taste of [region] with our [name]. This [category] features [ingredients], expertly prepared with [cooking_method]. [taste_description]. [texture_description]. [selling_point]. Perfect for [occasion].",
        "example_short": "Authentic Indonesian Nasi Goreng featuring fragrant rice, tender chicken, and fresh vegetables. Homemade with aromatic spices. Perfect for comfort food lovers.",
        "example_long": "Experience the authentic taste of Indonesia with our Nasi Goreng Spesial. This beloved fried rice dish features fragrant jasmine rice, tender marinated chicken, and a colorful array of fresh vegetables, expertly prepared with traditional Indonesian spices. The perfect balance of savory and sweet flavors from our signature kecap manis. Crispy fried shallots add the perfect crunch. Homemade with love and aromatic spices. Perfect for a satisfying lunch or dinner.",
        "is_active": True
    },
    {
        "name": "Main Meals - Informational",
        "category": "main_meals",
        "use_case": "informational",
        "language": "en",
        "short_template": "[name] is a [region] [category] made with [ingredients].",
        "long_template": "[name] is a traditional [region] [category] that consists of [ingredients]. It is typically prepared by [cooking_method] and seasoned with [seasonings]. The dish is known for its [taste_profile] flavor and [texture] texture.",
        "example_short": "Nasi Goreng is an Indonesian fried rice dish made with rice, vegetables, and protein.",
        "example_long": "Nasi Goreng is a traditional Indonesian fried rice dish that consists of cooked rice, vegetables, eggs, and choice of protein. It is typically prepared by stir-frying in a wok and seasoned with sweet soy sauce (kecap manis), garlic, and shallots. The dish is known for its savory-sweet flavor and soft yet slightly crispy texture.",
        "is_active": True
    },
    
    # Snacks Templates
    {
        "name": "Snacks - Promotional",
        "category": "snacks",
        "use_case": "promotional",
        "language": "en",
        "short_template": "Crispy and delicious [name] made with [ingredients]. [selling_point]. Perfect for [occasion].",
        "long_template": "Indulge in our [name], a delightful [category] that's [texture_description]. Made with [ingredients] and [cooking_method], each bite delivers [taste_description]. [selling_point]. Perfect for [occasion] or whenever you need a tasty treat.",
        "example_short": "Crispy and delicious Pisang Goreng made with fresh bananas and light batter. Perfectly fried to golden perfection. Perfect for afternoon snacking.",
        "example_long": "Indulge in our Pisang Goreng, a delightful Indonesian snack that's crispy on the outside and soft on the inside. Made with ripe bananas and a light, crispy batter, and fried to golden perfection, each bite delivers a perfect balance of sweet banana flavor and satisfying crunch. Made fresh daily with quality ingredients. Perfect for afternoon tea or whenever you need a tasty treat.",
        "is_active": True
    },
    
    # Drinks Templates
    {
        "name": "Drinks - Promotional",
        "category": "drinks",
        "use_case": "promotional",
        "language": "en",
        "short_template": "Refreshing [name] with [ingredients]. [selling_point]. Perfect for [occasion].",
        "long_template": "Cool down with our [name], a refreshing [category] that combines [ingredients]. [preparation_description]. [taste_description]. [selling_point]. Perfect for [weather_condition] or [occasion].",
        "example_short": "Refreshing Es Teler with avocado, jackfruit, and coconut in sweet coconut milk. A tropical paradise in a glass. Perfect for hot days.",
        "example_long": "Cool down with our Es Teler, a refreshing Indonesian beverage that combines creamy avocado, sweet jackfruit, and tender young coconut in rich coconut milk. Served over crushed ice with a drizzle of condensed milk. Sweet, creamy, and incredibly refreshing. A tropical paradise in every sip. Perfect for hot days or as a sweet ending to your meal.",
        "is_active": True
    },
    
    # Desserts Templates
    {
        "name": "Desserts - Promotional",
        "category": "desserts",
        "use_case": "promotional",
        "language": "en",
        "short_template": "Indulgent [name] crafted with [ingredients]. [selling_point]. Perfect for [occasion].",
        "long_template": "Treat yourself to our [name], a decadent [category] that's [texture_description]. Crafted with [ingredients] and [preparation_method], this dessert delivers [taste_description]. [selling_point]. Perfect for [occasion] or whenever you deserve something special.",
        "example_short": "Indulgent Klepon crafted with glutinous rice and palm sugar. Bursting with sweet surprise. Perfect for dessert lovers.",
        "example_long": "Treat yourself to our Klepon, a traditional Indonesian dessert that's soft, chewy, and delightfully sweet. Crafted with glutinous rice flour and filled with liquid palm sugar, then rolled in fresh grated coconut, this dessert delivers a burst of sweetness with every bite. Made fresh using traditional methods. Perfect for dessert after meals or as a sweet snack with tea.",
        "is_active": True
    },
]

# Promotional keywords by category and type
PROMOTIONAL_KEYWORDS = [
    # Main Meals - Selling Points
    {
        "category": "main_meals",
        "keyword_type": "selling_point",
        "language": "en",
        "keywords": [
            "authentic", "homemade", "traditional", "handcrafted", "made to order",
            "fresh ingredients", "aromatic spices", "family recipe", "chef's special",
            "locally sourced", "premium quality", "signature dish", "award-winning",
            "time-honored recipe", "expertly prepared", "cooked to perfection"
        ],
        "usage_notes": "Use to highlight authenticity and quality"
    },
    {
        "category": "main_meals",
        "keyword_type": "flavor",
        "language": "en",
        "keywords": [
            "savory", "rich", "flavorful", "aromatic", "umami", "well-seasoned",
            "perfectly balanced", "complex flavors", "bold", "delicate", "subtle",
            "harmonious", "layered flavors", "mouth-watering"
        ],
        "usage_notes": "Use to describe taste characteristics"
    },
    {
        "category": "main_meals",
        "keyword_type": "texture",
        "language": "en",
        "keywords": [
            "tender", "juicy", "crispy", "succulent", "melt-in-your-mouth",
            "perfectly cooked", "al dente", "fluffy", "creamy", "velvety"
        ],
        "usage_notes": "Use to describe texture and mouthfeel"
    },
    
    # Snacks - Selling Points
    {
        "category": "snacks",
        "keyword_type": "selling_point",
        "language": "en",
        "keywords": [
            "crispy", "crunchy", "freshly made", "bite-sized", "perfect for sharing",
            "addictively good", "irresistible", "golden fried", "light and crispy",
            "made fresh daily", "street food favorite", "crowd-pleaser"
        ],
        "usage_notes": "Use to highlight snack appeal"
    },
    {
        "category": "snacks",
        "keyword_type": "flavor",
        "language": "en",
        "keywords": [
            "savory", "sweet", "tangy", "spicy", "zesty", "flavorful",
            "perfectly seasoned", "addictive", "satisfying"
        ],
        "usage_notes": "Use to describe snack flavors"
    },
    
    # Drinks - Selling Points
    {
        "category": "drinks",
        "keyword_type": "selling_point",
        "language": "en",
        "keywords": [
            "refreshing", "cooling", "energizing", "revitalizing", "thirst-quenching",
            "made to order", "freshly prepared", "Instagram-worthy", "tropical",
            "authentic", "traditional", "signature blend"
        ],
        "usage_notes": "Use to highlight drink appeal"
    },
    {
        "category": "drinks",
        "keyword_type": "flavor",
        "language": "en",
        "keywords": [
            "sweet", "creamy", "smooth", "rich", "refreshing", "fruity",
            "aromatic", "balanced", "not too sweet", "perfectly sweetened"
        ],
        "usage_notes": "Use to describe drink flavors"
    },
    
    # Desserts - Selling Points
    {
        "category": "desserts",
        "keyword_type": "selling_point",
        "language": "en",
        "keywords": [
            "indulgent", "decadent", "heavenly", "irresistible", "divine",
            "handcrafted", "artisanal", "made with love", "traditional recipe",
            "sweet perfection", "guilt-free pleasure", "not too sweet"
        ],
        "usage_notes": "Use to highlight dessert appeal"
    },
    {
        "category": "desserts",
        "keyword_type": "flavor",
        "language": "en",
        "keywords": [
            "sweet", "rich", "creamy", "smooth", "velvety", "luscious",
            "perfectly balanced", "not overly sweet", "delicate sweetness"
        ],
        "usage_notes": "Use to describe dessert flavors"
    },
    
    # General keywords for all categories
    {
        "category": "all",
        "keyword_type": "general",
        "language": "en",
        "keywords": [
            "delicious", "tasty", "flavorful", "appetizing", "mouthwatering",
            "delectable", "scrumptious", "yummy", "amazing", "wonderful",
            "fantastic", "excellent", "outstanding", "exceptional"
        ],
        "usage_notes": "General positive descriptors for any food"
    },
]


def seed_descriptions():
    """Seed the database with description templates and promotional keywords"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_templates = db.query(DescriptionTemplate).count()
        existing_keywords = db.query(PromotionalKeyword).count()
        
        if existing_templates > 0 or existing_keywords > 0:
            print(f"Database already has {existing_templates} templates and {existing_keywords} keyword sets.")
            print("Skipping seed. Delete existing data first if you want to re-seed.")
            return
        
        print("Seeding description templates...")
        for template_data in DESCRIPTION_TEMPLATES:
            print(f"  Creating template: {template_data['name']}")
            template = DescriptionTemplate(**template_data)
            db.add(template)
        
        print("\nSeeding promotional keywords...")
        for keyword_data in PROMOTIONAL_KEYWORDS:
            print(f"  Creating keywords: {keyword_data['category']} - {keyword_data['keyword_type']}")
            keyword = PromotionalKeyword(**keyword_data)
            db.add(keyword)
        
        db.commit()
        
        print(f"\n✅ Successfully seeded:")
        print(f"   - {len(DESCRIPTION_TEMPLATES)} description templates")
        print(f"   - {len(PROMOTIONAL_KEYWORDS)} promotional keyword sets")
        
        # Print summary
        print("\nTemplates by category:")
        from sqlalchemy import func
        categories = db.query(
            DescriptionTemplate.category, 
            func.count(DescriptionTemplate.id)
        ).group_by(DescriptionTemplate.category).all()
        for category, count in categories:
            print(f"  - {category}: {count}")
        
        print("\nKeywords by category:")
        categories = db.query(
            PromotionalKeyword.category,
            func.count(PromotionalKeyword.id)
        ).group_by(PromotionalKeyword.category).all()
        for category, count in categories:
            print(f"  - {category}: {count}")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_descriptions()
