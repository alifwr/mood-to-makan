"""
Reseed all data with embeddings - Complete Reset Script

This script will:
1. Clear existing data from foods, descriptions, and review analysis tables
2. Reseed with fresh data including embeddings

Run with: uv run python reseed_all.py
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.food import Food
from app.models.description_template import DescriptionTemplate
from app.models.promotional_keyword import PromotionalKeyword
from app.models.problem_category import ProblemCategory
from sqlalchemy import func

def clear_and_reseed():
    """Clear existing data and reseed everything"""
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("  CLEARING EXISTING DATA")
        print("=" * 80)
        
        # Clear foods
        food_count = db.query(Food).count()
        if food_count > 0:
            print(f"\n🗑️  Deleting {food_count} existing foods...")
            db.query(Food).delete()
            db.commit()
            print("✅ Foods cleared")
        
        # Clear description templates
        template_count = db.query(DescriptionTemplate).count()
        if template_count > 0:
            print(f"🗑️  Deleting {template_count} existing templates...")
            db.query(DescriptionTemplate).delete()
            db.commit()
            print("✅ Templates cleared")
        
        # Clear promotional keywords
        keyword_count = db.query(PromotionalKeyword).count()
        if keyword_count > 0:
            print(f"🗑️  Deleting {keyword_count} existing keyword sets...")
            db.query(PromotionalKeyword).delete()
            db.commit()
            print("✅ Keywords cleared")
        
        # Clear problem categories
        category_count = db.query(ProblemCategory).count()
        if category_count > 0:
            print(f"🗑️  Deleting {category_count} existing problem categories...")
            db.query(ProblemCategory).delete()
            db.commit()
            print("✅ Problem categories cleared")
        
        print("\n" + "=" * 80)
        print("  RESEEDING DATA")
        print("=" * 80)
        
        # Now run the seed scripts
        print("\n📦 Running seed_foods.py...")
        import subprocess
        result = subprocess.run(
            ["uv", "run", "python", "seed_foods.py"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Foods seeded successfully")
        else:
            print(f"❌ Error seeding foods: {result.stderr}")
        
        print("\n📦 Running seed_descriptions.py...")
        result = subprocess.run(
            ["uv", "run", "python", "seed_descriptions.py"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Descriptions seeded successfully")
        else:
            print(f"❌ Error seeding descriptions: {result.stderr}")
        
        print("\n📦 Running seed_review_analysis.py...")
        result = subprocess.run(
            ["uv", "run", "python", "seed_review_analysis.py"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Problem categories seeded successfully")
        else:
            print(f"❌ Error seeding problem categories: {result.stderr}")
        
        print("\n" + "=" * 80)
        print("  ✅ RESEEDING COMPLETE")
        print("=" * 80)
        
        # Show final counts
        db.refresh(db)
        print(f"\n📊 Final counts:")
        print(f"   Foods: {db.query(Food).count()}")
        print(f"   Templates: {db.query(DescriptionTemplate).count()}")
        print(f"   Keywords: {db.query(PromotionalKeyword).count()}")
        print(f"   Problem Categories: {db.query(ProblemCategory).count()}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("\n🚀 MOOD2MAKAN - COMPLETE DATA RESEED")
    print("This will clear and reseed all data with embeddings\n")
    
    response = input("Are you sure you want to continue? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        clear_and_reseed()
    else:
        print("❌ Cancelled")
