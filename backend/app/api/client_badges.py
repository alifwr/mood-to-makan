from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api import deps
from app.models.user import User
from app.models.client_badge import ClientBadge
from app.models.review import Review
from app.models.store import Store

router = APIRouter()


@router.post("/store-in-city-badges")
def store_in_city_badges(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Calculate and save badges based on VALID stores reviewed per city.
    Only stores with is_valid_store=True are counted.
    Badge percentage = (reviewed valid stores in city / total valid stores in city) * 100
    
    Only authenticated users can use this endpoint.
    Automatically saves results to client_badges table.
    """
    
    # Get all reviews by the current user
    user_reviews = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.store_id.isnot(None)
    ).all()
    
    if not user_reviews:
        # No reviews, create empty badge record
        client_badge = db.query(ClientBadge).filter(
            ClientBadge.client_id == current_user.id
        ).first()
        
        if not client_badge:
            client_badge = ClientBadge(
                client_id=current_user.id,
                badges=[],
                reviewed_stores_id=[]
            )
            db.add(client_badge)
        else:
            client_badge.badges = []
            client_badge.reviewed_stores_id = []
        
        db.commit()
        db.refresh(client_badge)
        
        return {
            "badges": [],
            "total_cities": 0,
            "message": "No reviews found"
        }
    
    # Get unique store IDs from reviews
    reviewed_store_ids = list(set([r.store_id for r in user_reviews if r.store_id]))
    
    # Get all reviewed stores with their cities - ONLY VALID STORES
    reviewed_stores = db.query(Store).filter(
        Store.id.in_(reviewed_store_ids),
        Store.is_valid_store == True  # Only count valid stores
    ).all()
    
    # If no valid stores were reviewed, return empty
    if not reviewed_stores:
        client_badge = db.query(ClientBadge).filter(
            ClientBadge.client_id == current_user.id
        ).first()
        
        if not client_badge:
            client_badge = ClientBadge(
                client_id=current_user.id,
                badges=[],
                reviewed_stores_id=[]
            )
            db.add(client_badge)
        else:
            client_badge.badges = []
            client_badge.reviewed_stores_id = []
        
        db.commit()
        db.refresh(client_badge)
        
        return {
            "badges": [],
            "total_cities": 0,
            "message": "No valid stores reviewed"
        }
    
    # Group stores by city
    stores_by_city = {}
    for store in reviewed_stores:
        city = store.city or "Unknown"
        if city not in stores_by_city:
            stores_by_city[city] = []
        stores_by_city[city].append({
            "id": store.id,
            "name": store.name,
            "address": store.address
        })
    
    # Calculate badges for each city
    badges = []
    for city, reviewed_stores_in_city in stores_by_city.items():
        # Get total VALID stores in this city
        total_valid_stores_in_city = db.query(func.count(Store.id)).filter(
            Store.city == city,
            Store.is_valid_store == True  # Only count valid stores
        ).scalar()
        
        reviewed_count = len(reviewed_stores_in_city)
        badge_percentage = (reviewed_count / total_valid_stores_in_city * 100) if total_valid_stores_in_city > 0 else 0
        
        badges.append({
            "city": city,
            "badge_percentage": round(badge_percentage, 2),
            "reviewed_count": reviewed_count,
            "total_stores": total_valid_stores_in_city,
            "reviewed_stores": reviewed_stores_in_city
        })
    
    # Sort badges by percentage (highest first)
    badges.sort(key=lambda x: x["badge_percentage"], reverse=True)
    
    # Save to client_badges table (only valid store IDs)
    valid_store_ids = [s.id for s in reviewed_stores]
    
    client_badge = db.query(ClientBadge).filter(
        ClientBadge.client_id == current_user.id
    ).first()
    
    if not client_badge:
        client_badge = ClientBadge(
            client_id=current_user.id,
            badges=badges,
            reviewed_stores_id=valid_store_ids
        )
        db.add(client_badge)
    else:
        client_badge.badges = badges
        client_badge.reviewed_stores_id = valid_store_ids
    
    db.commit()
    db.refresh(client_badge)
    
    return {
        "badges": badges,
        "total_cities": len(badges),
        "total_reviewed_stores": len(valid_store_ids),
        "message": "Badges calculated and saved successfully"
    }
