import random
import sys
import os
from pathlib import Path
import datetime

# Add the parent directory to sys.path to allow importing app
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.models.store import Store
from app.models.food import Food
from app.models.review import Review
from app.models.client_badge import ClientBadge
from app.models.user_food_history import UserFoodHistory
from app.core.security import get_password_hash
from app.services.ai_service import generate_embedding

def seed_users(db: Session):
    print("Seeding Users...")
    users = []
    
    # Admin
    if not db.query(User).filter(User.email == "admin@example.com").first():
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="Admin User",
            role=UserRole.admin,
            image_url="https://ui-avatars.com/api/?name=Admin+User"
        )
        db.add(admin)
        users.append(admin)

    # UMKM Users
    umkm_emails = ["umkm1@example.com", "umkm2@example.com"]
    for i, email in enumerate(umkm_emails):
        if not db.query(User).filter(User.email == email).first():
            user = User(
                email=email,
                hashed_password=get_password_hash("password123"),
                full_name=f"UMKM Owner {i+1}",
                role=UserRole.umkm,
                image_url=f"https://ui-avatars.com/api/?name=UMKM+{i+1}"
            )
            db.add(user)
            users.append(user)

    # Client Users
    client_emails = ["client1@example.com", "client2@example.com", "client3@example.com"]
    for i, email in enumerate(client_emails):
        if not db.query(User).filter(User.email == email).first():
            user = User(
                email=email,
                hashed_password=get_password_hash("password123"),
                full_name=f"Client User {i+1}",
                role=UserRole.client,
                image_url=f"https://ui-avatars.com/api/?name=Client+{i+1}"
            )
            db.add(user)
            users.append(user)
    
    db.commit()
    print("Users seeded.")
    return users

def seed_stores(db: Session):
    print("Seeding Stores...")
    umkm_users = db.query(User).filter(User.role == UserRole.umkm).all()
    if not umkm_users:
        print("No UMKM users found. Skipping store seeding.")
        return

    stores_data = [
        {
            "name": "Warung Nasi Goreng Spesial",
            "description": "Nasi goreng enak dengan bumbu rahasia.",
            "province": "DKI Jakarta",
            "city": "Jakarta Selatan",
            "address": "Jl. Fatmawati No. 10",
            "latitude": -6.261493,
            "longitude": 106.810600,
        },
        {
            "name": "Bakso Solo Mantap",
            "description": "Bakso asli Solo dengan kuah segar.",
            "province": "DKI Jakarta",
            "city": "Jakarta Pusat",
            "address": "Jl. Sudirman No. 5",
            "latitude": -6.208763,
            "longitude": 106.845599,
        },
        {
            "name": "Sate Ayam Madura",
            "description": "Sate ayam empuk dengan bumbu kacang kental.",
            "province": "Jawa Timur",
            "city": "Surabaya",
            "address": "Jl. Tunjungan No. 20",
            "latitude": -7.257472,
            "longitude": 112.752088,
        }
    ]

    for i, data in enumerate(stores_data):
        # Assign to random UMKM user
        umkm = random.choice(umkm_users)
        
        # Check if store exists (by name for simplicity)
        if not db.query(Store).filter(Store.name == data["name"]).first():
            store = Store(
                umkm_id=umkm.id,
                name=data["name"],
                description=data["description"],
                enhanced_description=f"Enhanced: {data['description']}",
                province=data["province"],
                city=data["city"],
                address=data["address"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                image_url=f"https://placehold.co/600x400?text={data['name'].replace(' ', '+')}",
                embedding=generate_embedding(f"{data['name']} {data['description']} {data['province']} {data['city']}"),
                is_valid_store=True
            )
            db.add(store)
    
    db.commit()
    print("Stores seeded.")

def seed_foods(db: Session):
    print("Seeding Foods...")
    stores = db.query(Store).all()
    if not stores:
        print("No stores found. Skipping food seeding.")
        return

    foods_data = [
        {
            "name": "Nasi Goreng Ayam",
            "description": "Nasi goreng dengan potongan ayam.",
            "category": "main_meals",
            "taste_profile": ["savory", "spicy"],
            "texture": ["soft"],
            "mood_tags": ["happy", "comfort"],
            "price": 25000
        },
        {
            "name": "Es Teh Manis",
            "description": "Teh manis dingin segar.",
            "category": "drinks",
            "taste_profile": ["sweet", "fresh"],
            "texture": [],
            "mood_tags": ["refreshing"],
            "price": 5000
        },
        {
            "name": "Pisang Goreng",
            "description": "Pisang goreng renyah.",
            "category": "snacks",
            "taste_profile": ["sweet"],
            "texture": ["crispy"],
            "mood_tags": ["happy"],
            "price": 10000
        },
        {
            "name": "Bakso Urat",
            "description": "Bakso dengan urat sapi asli.",
            "category": "main_meals",
            "taste_profile": ["savory"],
            "texture": ["chewy"],
            "mood_tags": ["comfort"],
            "price": 20000
        }
    ]

    for store in stores:
        if store.umkm_id is None:
            continue

        # Add 2-3 random foods to each store
        store_foods = random.sample(foods_data, k=random.randint(2, 3))
        for food_data in store_foods:
            # Check if food exists in this store
            if not db.query(Food).filter(Food.store_id == store.id, Food.name == food_data["name"]).first():
                food = Food(
                    store_id=store.id,
                    user_id=store.umkm_id, # Assuming food belongs to store owner
                    name=food_data["name"],
                    description=food_data["description"],
                    enhanced_description=f"Delicious {food_data['name']}",
                    category=food_data["category"],
                    main_ingredients=["ingredient1", "ingredient2"],
                    taste_profile=food_data["taste_profile"],
                    texture=food_data["texture"],
                    mood_tags=food_data["mood_tags"],
                    image_url=f"https://placehold.co/400x300?text={food_data['name'].replace(' ', '+')}",
                    embedding=generate_embedding(f"{food_data['name']} {food_data['description']} {food_data['category']} {' '.join(food_data['taste_profile'])}"),
                    is_valid_food=True
                )
                db.add(food)
    
    db.commit()
    print("Foods seeded.")

def seed_reviews(db: Session):
    print("Seeding Reviews...")
    clients = db.query(User).filter(User.role == UserRole.client).all()
    foods = db.query(Food).all()
    
    if not clients or not foods:
        print("Missing clients or foods. Skipping reviews.")
        return

    comments = [
        "Enak banget!",
        "Lumayan lah.",
        "Kurang asin dikit.",
        "Mantap jiwa!",
        "Biasa aja.",
        "Recommended!"
    ]

    for _ in range(20): # Create 20 random reviews
        client = random.choice(clients)
        food = random.choice(foods)
        
        # Check if review already exists (optional, but good for idempotency)
        # For simplicity, we just add if not strictly checking unique constraint on (user, food) unless defined
        
        review = Review(
            user_id=client.id,
            store_id=food.store_id,
            food_id=food.id,
            rating=random.randint(3, 5), # Mostly positive reviews
            comment=random.choice(comments),
            embedding=generate_embedding(random.choice(comments))
        )
        db.add(review)
    
    db.commit()
    print("Reviews seeded.")

def seed_client_badges(db: Session):
    print("Seeding Client Badges...")
    clients = db.query(User).filter(User.role == UserRole.client).all()
    
    for client in clients:
        if not db.query(ClientBadge).filter(ClientBadge.client_id == client.id).first():
            badge = ClientBadge(
                client_id=client.id,
                badges=[{"name": "Foodie", "date": str(datetime.datetime.now().date())}],
                reviewed_stores_id=[]
            )
            db.add(badge)
    
    db.commit()
    print("Client Badges seeded.")

def seed_user_food_history(db: Session):
    print("Seeding User Food History...")
    clients = db.query(User).filter(User.role == UserRole.client).all()
    foods = db.query(Food).all()
    
    if not clients or not foods:
        return

    interaction_types = ["viewed", "liked", "reviewed"]
    moods = ["happy", "sad", "hungry", "bored"]

    for _ in range(30):
        client = random.choice(clients)
        food = random.choice(foods)
        
        history = UserFoodHistory(
            user_id=client.id,
            food_id=food.id,
            interaction_type=random.choice(interaction_types),
            rating=random.randint(1, 5) if random.random() > 0.5 else None,
            mood_context=random.choice(moods),
            created_at=datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=random.randint(0, 30))
        )
        db.add(history)
    
    db.commit()
    print("User Food History seeded.")

def main():
    db = SessionLocal()
    try:
        seed_users(db)
        seed_stores(db)
        seed_foods(db)
        seed_reviews(db)
        seed_client_badges(db)
        seed_user_food_history(db)
        print("All tables seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
