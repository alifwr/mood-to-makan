from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def seed_db():
    db = SessionLocal()
    try:
        # Check if users exist
        if not db.query(User).filter(User.email == "umkm@example.com").first():
            umkm_user = User(
                email="umkm@example.com",
                hashed_password=get_password_hash("password123"),
                full_name="UMKM Owner",
                role="umkm"
            )
            db.add(umkm_user)
            print("Created UMKM user: umkm@example.com / password123")

        if not db.query(User).filter(User.email == "client@example.com").first():
            client_user = User(
                email="client@example.com",
                hashed_password=get_password_hash("password123"),
                full_name="Client User",
                role="client"
            )
            db.add(client_user)
            print("Created Client user: client@example.com / password123")
        
        db.commit()
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
