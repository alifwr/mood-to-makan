"""
Seed script for problem categories.
Run this script to populate the database with problem categories for review analysis.
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.problem_category import ProblemCategory

# Problem categories with descriptions and keywords
PROBLEM_CATEGORIES = [
    {
        "category_key": "inconsistent_taste",
        "name": "Inconsistent Taste",
        "description": "Food quality varies, seasoning issues, taste not as expected",
        "keywords": [
            "taste", "flavor", "bland", "too salty", "too sweet", "too spicy",
            "not fresh", "quality", "inconsistent", "different", "changed",
            "not like before", "seasoning", "undercooked", "overcooked"
        ],
        "severity_weight": 0.8,
        "action_template": "Review and standardize recipes. Implement quality control checks. Train kitchen staff on consistent preparation methods.",
        "is_active": True,
        "language": "en"
    },
    {
        "category_key": "untidy_packaging",
        "name": "Untidy Packaging",
        "description": "Poor presentation, leaking containers, messy packaging",
        "keywords": [
            "packaging", "container", "leak", "spill", "messy", "dirty",
            "presentation", "wrapped", "box", "bag", "untidy", "sloppy",
            "not sealed", "broken", "damaged"
        ],
        "severity_weight": 0.6,
        "action_template": "Invest in better quality packaging materials. Train staff on proper packaging techniques. Implement packaging quality checks before delivery.",
        "is_active": True,
        "language": "en"
    },
    {
        "category_key": "slow_delivery",
        "name": "Slow Delivery",
        "description": "Late arrivals, long wait times, delayed orders",
        "keywords": [
            "late", "slow", "delay", "wait", "long time", "took forever",
            "delivery", "arrived", "waiting", "hours", "cold food",
            "not on time", "schedule", "promised time"
        ],
        "severity_weight": 0.7,
        "action_template": "Optimize delivery routes. Consider hiring additional delivery staff during peak hours. Implement better order tracking and time management systems.",
        "is_active": True,
        "language": "en"
    },
    {
        "category_key": "unfriendly_service",
        "name": "Unfriendly Service",
        "description": "Rude staff, poor communication, unhelpful attitude",
        "keywords": [
            "rude", "unfriendly", "attitude", "service", "staff", "impolite",
            "disrespectful", "unhelpful", "ignored", "communication",
            "customer service", "behavior", "manner", "treated badly"
        ],
        "severity_weight": 0.9,
        "action_template": "Provide customer service training to all staff. Implement customer feedback system. Address specific staff behavior issues promptly.",
        "is_active": True,
        "language": "en"
    },
    {
        "category_key": "inappropriate_portion",
        "name": "Inappropriate Portion Size",
        "description": "Portions too small or too large, value for money concerns",
        "keywords": [
            "portion", "size", "small", "tiny", "not enough", "quantity",
            "amount", "value", "price", "expensive", "too much", "too little",
            "serving", "not worth", "overpriced"
        ],
        "severity_weight": 0.6,
        "action_template": "Review portion sizes and pricing. Ensure consistency in serving sizes. Consider offering different portion options (small/regular/large).",
        "is_active": True,
        "language": "en"
    },
]


def seed_problem_categories():
    """Seed the database with problem categories"""
    db = SessionLocal()
    
    try:
        # Check if categories already exist
        existing_count = db.query(ProblemCategory).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} problem categories.")
            print("Skipping seed. Delete existing categories first if you want to re-seed.")
            return
        
        print("Seeding problem categories...")
        
        for category_data in PROBLEM_CATEGORIES:
            print(f"  Creating: {category_data['name']}")
            category = ProblemCategory(**category_data)
            db.add(category)
        
        db.commit()
        
        print(f"\n✅ Successfully seeded {len(PROBLEM_CATEGORIES)} problem categories!")
        
        # Print summary
        print("\nProblem Categories:")
        categories = db.query(ProblemCategory).all()
        for cat in categories:
            print(f"  - {cat.name} ({cat.category_key})")
            print(f"    Severity: {cat.severity_weight}, Keywords: {len(cat.keywords)}")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_problem_categories()
