"""
Comprehensive API Testing Script for Backend
With detailed request/response logging

Run with: uv run python test_api.py
"""

import requests
import json
from typing import Optional

# Configuration
BASE_URL = "http://localhost:8000/api/v1"


# Global token storage
auth_token: Optional[str] = None


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_request(method: str, url: str, data=None, headers=None):
    """Print HTTP request details"""
    print(f"\n📤 REQUEST: {method} {url}")
    if headers:
        safe_headers = {k: (v[:20] + '...' if len(str(v)) > 20 else v) for k, v in headers.items()}
        print(f"   Headers: {json.dumps(safe_headers, indent=11)}")
    if data:
        print(f"   Body: {json.dumps(data, indent=9)}")


def print_response(response):
    """Print HTTP response details"""
    print(f"\n📥 RESPONSE: {response.status_code} {response.reason}")
    try:
        response_json = response.json()
        response_str = json.dumps(response_json, indent=9)
        if len(response_str) > 1500:
            response_str = response_str[:1500] + "\n         ... (truncated)"
        print(f"   Body: {response_str}")
    except:
        text = response.text[:500]
        if len(response.text) > 500:
            text += "... (truncated)"
        print(f"   Body: {text}")


def print_result(test_name: str, success: bool):
    """Print test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"\n{status} - {test_name}")


def get_headers():
    """Get authorization headers"""
    if auth_token:
        return {"Authorization": f"Bearer {auth_token}"}
    return {}


# ========== AUTHENTICATION AND USERS TESTS ==========

def test_auth_and_user():
    global auth_token
    print_section("USER ENDPOINT TESTS")

    # ===============================
    # 1. Register User
    # ===============================
    register_data_1 = {
        "email": "admin@gmail.com",
        "password": "admin1",
        "full_name": "admin123",
        "role": "admin"
    }
    register_data_2 = {
        "email": "client@gmail.com",
        "password": "client1",
        "full_name": "client123"
    }
    register_data_3 = {
        "email": "umkm@gmail.com",
        "password": "umkm1",
        "full_name": "umkm123",
        "role": "umkm"
    }

    url = f"{BASE_URL}/users"
    print_request("POST", url, data=register_data_1)
    response = requests.post(url, json=register_data_1)
    print_response(response)
    print_result("Register User 1", response.status_code in [200, 201, 400])
    
    url = f"{BASE_URL}/users"
    print_request("POST", url, data=register_data_2)
    response = requests.post(url, json=register_data_2)
    print_response(response)
    print_result("Register User 2", response.status_code in [200, 201, 400])
    
    url = f"{BASE_URL}/users"
    print_request("POST", url, data=register_data_3)
    response = requests.post(url, json=register_data_3)
    print_response(response)
    print_result("Register User 3", response.status_code in [200, 201, 400])

    # ===============================
    # 2. Login User
    # ===============================
    login_data = {
        "username": "client@gmail.com",
        "password": "client",
    }

    url = f"{BASE_URL}/auth/login"
    print_request("POST", url, data=login_data)
    response = requests.post(url, data=login_data)
    print_response(response)
    success = response.status_code == 200
    print_result("Login User 1 Wrong Email", success)

    if not success:
        print("❌ Login failed. Stopping tests.")
    else:
        auth_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}
        print(f"  🔑 Token obtained: {auth_token[:30]}...")
    
    login_data = {
        "username": "oo@gmail.com",
        "password": "admin",
    }

    url = f"{BASE_URL}/auth/login"
    print_request("POST", url, data=login_data)
    response = requests.post(url, data=login_data)
    print_response(response)
    success = response.status_code == 200
    print_result("Login User 1 Wrong Password", success)

    if not success:
        print("❌ Login failed. Stopping tests.")
    else:
        auth_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}
        print(f"  🔑 Token obtained: {auth_token[:30]}...")
    
    login_data = {
        "username": "client@gmail.com",
        "password": "client1",
    }

    url = f"{BASE_URL}/auth/login"
    print_request("POST", url, data=login_data)
    response = requests.post(url, data=login_data)
    print_response(response)
    success = response.status_code == 200
    print_result("Login User 1 Correct Email and Password", success)

    if not success:
        print("❌ Login failed. Stopping tests.")
        return
    else:
        auth_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}
        print(f"  🔑 Token obtained: {auth_token[:30]}...")

    # ===============================
    # 3. GET /users/me
    # ===============================
    url = f"{BASE_URL}/users/me"
    print_request("GET", url)
    response = requests.get(url, headers=headers)
    print_response(response)
    print_result("Get Current User", response.status_code == 200)

    # ===============================
    # 4. Update User (PUT /users/me)
    # ===============================
    update_data = {
        "full_name": "client123",
        "password": "client",
        "image_url": "https://dummyimage.com/user.png",
    }

    url = f"{BASE_URL}/users/me"
    print_request("PUT", url, data=update_data)
    response = requests.put(url, json=update_data, headers=headers)
    print_response(response)
    print_result("Update User", response.status_code == 200)

    # ===============================
    # 5. Upload User Image (PUT /users/me/image)
    # ===============================
    url = f"{BASE_URL}/users/me/image"
    mock_file = ("test.png", b"fake image bytes", "image/png")

    print_request("PUT", url, data="(binary image file)")
    response = requests.put(
        url,
        files={"file": mock_file},
        headers=headers,
    )
    print_response(response)
    print_result("Upload User Image", response.status_code == 200)


# ========== STORE API TEST ==========

def test_store_full_flow():
    print_section("FULL STORE API TESTS")

    # -----------------------------------------------------
    # LOGIN CLIENT
    # -----------------------------------------------------
    login_client = {
        "username": "client@gmail.com",
        "password": "client"
    }
    url = f"{BASE_URL}/auth/login"
    response = requests.post(url, data=login_client)
    print_response(response)
    success = response.status_code == 200
    print_result("Login User Client", success)

    if not success:
        print("❌ Login failed. Stopping tests.")
        return
    else:
        auth_token = response.json()["access_token"]
        client_headers = {"Authorization": f"Bearer {auth_token}"}
        print(f"  🔑 Token obtained: {auth_token[:30]}...")

    # -----------------------------------------------------
    # CLIENT CREATE STORE 
    # -----------------------------------------------------
    store_client = {
        "name": "Client Store",
        "description": "Client-made store",
        "province": "DKI Jakarta",
        "city": "Jakarta Selatan",
        "address": "Client Road 22"
    }

    url = f"{BASE_URL}/stores"
    print_request("POST", url, data=store_client)
    response = requests.post(url, json=store_client, headers=client_headers)
    print_response(response)
    success = response.status_code < 300
    print_result("Client Creates Store", success)
    
    if not success:
        print("❌ Add store by client failed. Stopping tests.")
    else:
        store_client_id = response.json().get("id")
        print(f"Store ID: {store_client_id}")

    # -----------------------------------------------------
    # LOGIN UMKM
    # -----------------------------------------------------
    login_umkm = {
        "username": "umkm@gmail.com",
        "password": "umkm1"
    }
    url = f"{BASE_URL}/auth/login"
    response = requests.post(url, data=login_umkm)
    print_response(response)
    success = response.status_code == 200
    print_result("Login User UMKM", success)

    if not success:
        print("❌ Login failed. Stopping tests.")
        return
    else:
        auth_token = response.json()["access_token"]
        umkm_headers = {"Authorization": f"Bearer {auth_token}"}
        print(f"  🔑 Token obtained: {auth_token[:30]}...")

    # -----------------------------------------------------
    # UMKM CREATE STORE 
    # -----------------------------------------------------
    store_umkm = {
        "name": "UMKM Store",
        "description": "UMKM-made store",
        "province": "DKI Jakarta",
        "city": "Jakarta Selatan",
        "address": "Client Road 20"
    }

    url = f"{BASE_URL}/stores"
    print_request("POST", url, data=store_umkm)
    response = requests.post(url, json=store_umkm, headers=umkm_headers)
    print_response(response)
    success = response.status_code < 300
    print_result("UMKM Creates Store", success)
    
    if not success:
        print("❌ Add store by client failed. Stopping tests.")
    else:
        store_umkm_id = response.json().get("id")
        print(f"Store ID: {store_umkm_id}")

    # -----------------------------------------------------
    # 1) GET ALL STORES
    # -----------------------------------------------------
    url = f"{BASE_URL}/stores"
    print_request("GET", url)
    resp = requests.get(url)
    print_response(resp)
    print_result("Get All Stores", resp.status_code == 200)

    # -----------------------------------------------------
    # 2) GET STORE DETAIL
    # -----------------------------------------------------
    url = f"{BASE_URL}/stores/{store_umkm_id}"
    print_request("GET", url)
    resp = requests.get(url)
    print_response(resp)
    print_result("Get Store Detail", resp.status_code == 200)

    # -----------------------------------------------------
    # 3) UPDATE STORE
    # -----------------------------------------------------
    update_payload = {
        "name": "UMKM Store Updated",
        "description": "Updated description",
        "address": "Updated Street 99"
    }

    url = f"{BASE_URL}/stores/{store_umkm_id}"
    print_request("PUT", url, data=update_payload)
    resp = requests.put(url, json=update_payload, headers=umkm_headers)
    print_response(resp)
    print_result("Update Store", resp.status_code == 200)

    # -----------------------------------------------------
    # 4) DELETE STORE
    # -----------------------------------------------------
    url = f"{BASE_URL}/stores/{store_client_id}"
    print_request("DELETE", url)
    resp = requests.delete(url, headers=client_headers)
    print_response(resp)
    print_result("Delete Store", resp.status_code in [200, 204])
    
    # -----------------------------------------------------
    # 5) UPLOAD IMAGE
    # -----------------------------------------------------
    url = f"{BASE_URL}/stores/{store_umkm_id}/image"

    # Pakai binary fake image (tidak butuh file asli)
    fake_image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"

    files = {
        "file": ("test.png", fake_image_content, "image/png")
    }

    print_request("PUT", url, data="binary-image")
    response = requests.put(url, files=files, headers=umkm_headers)
    print_response(response)
    success = response.status_code == 200
    print_result("Upload Store Image", success)

    if not success:
        print("❌ Upload image failed.")
        return

    image_url = response.json().get("image_url")
    print(f"  📷 Uploaded Image URL: {image_url}")
    
    print("\n✔ All store API tests completed.\n")
    
    # ===============================
    # 6. VALIDATE STORE (ADMIN only)
    # ===============================
    url = f"{BASE_URL}/foods/{store_umkm_id}/validate"
    print_request("PUT", url)
    response = requests.put(url, headers=umkm_headers)
    print_response(response)

    success = response.status_code == 200 and response.json().get("is_valid_food") == True
    print_result("Validate Food (Admin Only)", success)

    if not success:
        print("❌ Food validation failed — stopping")
        return


# ========== FOOD API TESTS ==========

def test_food_endpoints():
    print_section("FOOD ENDPOINT TESTS")

    # ===============================
    # 0. LOGIN as Admin (or UMKM)
    # ===============================
    login_data = {
        "username": "admin@gmail.com",
        "password": "admin1"
    }
    url = f"{BASE_URL}/auth/login"
    response = requests.post(url, data=login_data)
    print_response(response)
    success = response.status_code == 200
    print_result("Login Admin", success)

    if not success:
        print("❌ Login failed — cannot continue")
        return

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"🔑 Token: {token[:30]}...")

    # ===============================
    # 1. CREATE FOOD
    # ===============================
    food_payload = {
        "name": "Nasi Goreng",
        "description": "Indonesian fried rice",
        "category": "main_meals",
        "main_ingredients": ["rice", "egg", "soy sauce"],
        "taste_profile": ["savory"],
        "texture": ["soft"],
        "mood_tags": ["comfort"],
        "store_id": None
    }

    url = f"{BASE_URL}/foods"
    print_request("POST", url, food_payload)
    response = requests.post(url, json=food_payload, headers=headers)
    print_response(response)
    success = response.status_code == 201
    print_result("Create Food", success)

    if not success:
        print("❌ Food creation failed — stopping")
        return

    food_id = response.json()["id"]
    print(f"Created Food ID = {food_id}")

    # ===============================
    # 2. LIST FOODS
    # ===============================
    url = f"{BASE_URL}/foods"
    print_request("GET", url)
    response = requests.get(url, headers=headers)
    print_response(response)
    success = response.status_code == 200
    print_result("List Foods", success)

    # ===============================
    # 3. GET FOOD DETAIL
    # ===============================
    url = f"{BASE_URL}/foods/{food_id}"
    print_request("GET", url)
    response = requests.get(url, headers=headers)
    print_response(response)
    success = response.status_code == 200
    print_result("Get Food Detail", success)

    # ===============================
    # 4. UPDATE FOOD
    # ===============================
    update_payload = {
        "description": "Updated fried rice",
        "taste_profile": ["savory", "spicy"]
    }

    url = f"{BASE_URL}/foods/{food_id}"
    print_request("PUT", url, update_payload)
    response = requests.put(url, json=update_payload, headers=headers)
    print_response(response)
    success = response.status_code == 200
    print_result("Update Food", success)


    # ===============================
    # 5. VALIDATE FOOD (ADMIN only)
    # ===============================
    url = f"{BASE_URL}/foods/{food_id}/validate"
    print_request("PUT", url)
    response = requests.put(url, headers=headers)
    print_response(response)

    success = response.status_code == 200 and response.json().get("is_valid_food") == True
    print_result("Validate Food (Admin Only)", success)

    if not success:
        print("❌ Food validation failed — stopping")
        return


    # -----------------------------------------------------
    # 6) UPLOAD IMAGE
    # -----------------------------------------------------
    url = f"{BASE_URL}/foods/{food_id}/image"

    # Pakai binary fake image (tidak butuh file asli)
    fake_image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"

    files = {
        "file": ("test.png", fake_image_content, "image/png")
    }

    print_request("PUT", url, data="binary-image")
    response = requests.put(url, files=files, headers=headers)
    print_response(response)
    success = response.status_code == 200
    print_result("Upload Store Image", success)

    if not success:
        print("❌ Upload image failed.")
        return

    image_url = response.json().get("image_url")
    print(f"  📷 Uploaded Image URL: {image_url}")


    # ===============================
    # 7. DELETE FOOD
    # ===============================
    url = f"{BASE_URL}/foods/{food_id}"
    print_request("DELETE", url)
    response = requests.delete(url, headers=headers)

    print(f"Status Code: {response.status_code}")

    success = response.status_code == 204
    print_result("Delete Food", success)

    # ===============================
    # 8. GET FOOD after DELETE → must 404
    # ===============================
    url = f"{BASE_URL}/foods/{food_id}"
    print_request("GET", url)
    response = requests.get(url, headers=headers)
    print_response(response)
    success = response.status_code == 404
    print_result("Get Deleted Food (should 404)", success)


# ========== USER FOOD HISTORY API TESTS ==========

def test_user_food_history():
    global auth_token
    print_section("USER FOOD HISTORY & PREFERENCES TESTS")

    # ===============================
    # 1. Login as Client
    # ===============================
    login_data = {
        "username": "client@gmail.com",
        "password": "client",
    }

    url = f"{BASE_URL}/auth/login"
    response = requests.post(url, data=login_data)
    print_response(response)

    if response.status_code != 200:
        print("❌ Login failed. Stopping tests.")
        return

    auth_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    # ===============================
    # 2. Create Foods (diverse data)
    # ===============================
    foods_payload = [
        {
            "name": "Nasi Rendang",
            "description": "Rich beef rendang with rice",
            "category": "main_meals",
            "main_ingredients": ["rice", "beef", "spices"],
            "taste_profile": ["savory", "spicy"],
            "texture": ["soft"],
            "mood_tags": ["comfort"],
            "store_id": None
        },
        {
            "name": "Ice Matcha Latte",
            "description": "Sweet and creamy matcha drink",
            "category": "beverages",
            "main_ingredients": ["milk", "matcha"],
            "taste_profile": ["sweet"],
            "texture": ["smooth"],
            "mood_tags": ["relaxed"],
            "store_id": None
        }
    ]

    food_ids = []

    for food in foods_payload:
        url = f"{BASE_URL}/foods"
        print_request("POST", url, food)
        response = requests.post(url, json=food, headers=headers)
        print_response(response)

        if response.status_code != 201:
            print("❌ Food creation failed — stopping test")
            return

        food_id = response.json()["id"]
        food_ids.append(food_id)

    print(f"✅ Created Foods: {food_ids}")

    # ===============================
    # 3. Simulate User Interactions
    # ===============================
    url = f"{BASE_URL}/users/me/food-history"

    interactions = [
        # Food 1 interactions
        {"food_id": food_ids[0], "interaction_type": "viewed", "mood_context": "hungry"},
        {"food_id": food_ids[0], "interaction_type": "selected", "mood_context": "very hungry"},
        {"food_id": food_ids[0], "interaction_type": "rated", "rating": 4.5, "mood_context": "satisfied"},

        # Food 2 interactions
        {"food_id": food_ids[1], "interaction_type": "viewed", "mood_context": "tired"},
        {"food_id": food_ids[1], "interaction_type": "rated", "rating": 4.0, "mood_context": "relaxed"},
    ]

    for i, payload in enumerate(interactions, start=1):
        print_request("POST", url, payload)
        response = requests.post(url, json=payload, headers=headers)
        print_response(response)
        print_result(f"Interaction #{i}", response.status_code == 201)

    # ===============================
    # 4. GET /users/me/food-history
    # ===============================
    url = f"{BASE_URL}/users/me/food-history"
    print_request("GET", url)
    response = requests.get(url, headers=headers)
    print_response(response)
    print_result("Get Food History", response.status_code == 200)

    # ===============================
    # 5. GET /users/me/food-preferences
    # ===============================
    url = f"{BASE_URL}/users/me/food-preferences"
    print_request("GET", url)
    response = requests.get(url, headers=headers)
    print_response(response)

    success = response.status_code == 200
    print_result("Get Food Preferences", success)

    if success:
        prefs = response.json()
        print("✅ Derived Preferences Summary:")
        print(f"  Favorite Categories : {prefs['favorite_categories']}")
        print(f"  Favorite Tastes     : {prefs['favorite_tastes']}")
        print(f"  Favorite Moods      : {prefs['favorite_moods']}")
        print(f"  Average Rating      : {prefs['average_rating']}")
        print(f"  Total Interactions  : {prefs['total_interactions']}")
        print(f"  Most Selected Foods : {prefs['most_selected_foods']}")


# ========== REVIEWS API TESTS ==========

def test_reviews_api():
    global auth_token
    print_section("READ REVIEWS BY STORE TEST")

    # ===============================
    # 1. Login as Client
    # ===============================
    login_data = {
        "username": "client@gmail.com",
        "password": "client",
    }

    url = f"{BASE_URL}/auth/login"
    response = requests.post(url, data=login_data)
    print_response(response)

    if response.status_code != 200:
        print("❌ Login failed")
        return
     
    auth_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    url = f"{BASE_URL}/users/me"
    print_request("GET", url)
    response = requests.get(url, headers=headers)
    print_response(response)
    user_id = response.json()["id"]
    print_result("Get Current User", response.status_code == 200)

    # ===============================
    # 2. Create Store
    # ===============================
    store_payload = {
        "name": "Warung Sederhana",
        "description": "Authentic Minang food",
        "address": "Padang Street No. 1",
        "latitude": -0.9471,
        "longitude": 100.4172
    }

    url = f"{BASE_URL}/stores"
    print_request("POST", url, store_payload)
    response = requests.post(url, json=store_payload, headers=headers)
    print_response(response)

    if response.status_code not in [200, 201]:
        print("❌ Store creation failed")
        return

    store_id = response.json()["id"]
    print(f"✅ Created Store ID = {store_id}")

    # ===============================
    # 3. Create Food (belong to store)
    # ===============================
    food_payload = {
        "name": "Rendang",
        "description": "Slow cooked beef rendang",
        "category": "main_meals",
        "main_ingredients": ["beef", "spices"],
        "taste_profile": ["savory", "spicy"],
        "texture": ["tender"],
        "mood_tags": ["comfort"],
        "store_id": store_id
    }

    url = f"{BASE_URL}/foods"
    print_request("POST", url, food_payload)
    response = requests.post(url, json=food_payload, headers=headers)
    print_response(response)

    if response.status_code != 201:
        print("❌ Food creation failed")
        return

    food_id_1 = response.json()["id"]
    
    food_payload = {
        "name": "Semur",
        "description": "Slow cooked beef semur",
        "category": "main_meals",
        "main_ingredients": ["beef", "spice"],
        "taste_profile": ["savory", "sweet"],
        "texture": ["tender"],
        "mood_tags": ["comfort"],
        "store_id": store_id
    }

    url = f"{BASE_URL}/foods"
    print_request("POST", url, food_payload)
    response = requests.post(url, json=food_payload, headers=headers)
    print_response(response)

    if response.status_code != 201:
        print("❌ Food creation failed")
        return

    food_id_2 = response.json()["id"]

    # ===============================
    # 4. Create Reviews (store-based & food-based)
    # ===============================
    url = f"{BASE_URL}/reviews"

    review_payloads = [
        {
            "food_id": food_id_2,
            "store_id": store_id,
            "rating": 4.5,
            "comment": "Great service and authentic taste"
        },
        {
            "food_id": food_id_1,
            "store_id": store_id,
            "rating": 5.0,
            "comment": "The rendang is the best in town"
        }
    ]

    for i, payload in enumerate(review_payloads, start=1):
        print_request("POST", url, payload)
        response = requests.post(url, json=payload, headers=headers)
        print_response(response)
        print_result(f"Create Review #{i}", response.status_code == 201)

    # ===============================
    # 5. READ Reviews by Store
    # ===============================
    url = f"{BASE_URL}/reviews/store/{store_id}"
    print_request("GET", url)
    response = requests.get(url)
    print_response(response)

    success = response.status_code == 200
    print_result("Read Reviews by Store", success)

    if success:
        reviews = response.json()
        print(f"✅ Total Reviews for Store {store_id}: {len(reviews)}")
        for r in reviews:
            print(f" - ⭐ {r['rating']} | {r['comment']}")
    
    # ===============================
    # 6. Read Reviews by Food
    # ===============================
    url = f"{BASE_URL}/reviews/food/{food_id_1}"
    print_request("GET", url)
    response = requests.get(url)
    print_response(response)
    print_result("Get Reviews by Food", response.status_code == 200)
    
    # ===============================
    # 7. READ Reviews by User
    # ===============================
    url = f"{BASE_URL}/reviews/user/{user_id}"
    print_request("GET", url)
    response = requests.get(url)
    print_response(response)

    success = response.status_code == 200
    print_result("Read Reviews by User", success)

    if success:
        reviews = response.json()
        print(f"✅ Total Reviews by User {user_id}: {len(reviews)}")
        for r in reviews:
            print(f" - ⭐ {r['rating']} | {r['comment']}")


# ========== CLIENT BADGES API TESTS ==========

def test_client_badges_api():
    """Test client badges endpoint"""
    global auth_token
    print_section("CLIENT BADGES API TEST")

    # ===============================
    # 1. Login as Client
    # ===============================
    login_data = {
        "username": "client@gmail.com",
        "password": "client",
    }

    url = f"{BASE_URL}/auth/login"
    response = requests.post(url, data=login_data)
    print_response(response)

    if response.status_code != 200:
        print("❌ Login failed — cannot continue badge tests")
        return

    auth_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    print(f"🔑 Token: {auth_token[:30]}...")

    # ===============================
    # 2. Create stores in different cities
    # ===============================
    stores_payload = [
        {
            "name": "Jakarta Store 111",
            "description": "Store in Jakarta",
            "address": "Jakarta Street 1",
            "province": "DKI Jakarta",
            "city": "Jakarta Selatan",
        },
        {
            "name": "Jakarta Store 222",
            "description": "Another store in Jakarta",
            "address": "Jakarta Street 2",
            "province": "DKI Jakarta",
            "city": "Jakarta Selatan",
        },
        {
            "name": "Bandung Store 111",
            "description": "Store in Bandung",
            "address": "Bandung Street 1",
            "province": "Jawa Barat",
            "city": "Bandung",
        }
    ]

    store_ids = []
    for i, store_data in enumerate(stores_payload, start=1):
        url = f"{BASE_URL}/stores"
        print_request("POST", url, store_data)
        response = requests.post(url, json=store_data, headers=headers)
        print_response(response)

        if response.status_code in [200, 201]:
            store_id = response.json()["id"]
            store_ids.append(store_id)
            print(f"✅ Created Store #{i}: {store_data['name']} (ID={store_id})")
        else:
            print(f"❌ Failed to create store #{i}")

    # ===============================
    # 2.5. Validate stores (set is_valid_store=True)
    # ===============================
    # Login as admin to validate stores
    login_data_admin = {
        "username": "admin@gmail.com",
        "password": "admin1",
    }

    url = f"{BASE_URL}/auth/login"
    response = requests.post(url, data=login_data_admin)
    print_response(response)

    if response.status_code != 200:
        print("❌ Admin login failed — cannot validate stores")
        return

    auth_token_admin = response.json()["access_token"]
    headers_admin = {"Authorization": f"Bearer {auth_token_admin}"}
    print(f"🔑 Admin Token: {auth_token_admin[:30]}...")
    
    for i, store_id in enumerate(store_ids, start=1):
        url = f"{BASE_URL}/stores/{store_id}/validate"
        print_request("PUT", url)
        response = requests.put(url, headers=headers_admin)
        print_response(response)
        
        if response.status_code == 200:
            print(f"✅ Validated Store #{i} (ID={store_id})")
        else:
            print(f"❌ Failed to validate store #{i}")

    # ===============================
    # 3. Create foods for each store
    # ===============================
    food_ids = []
    for i, store_id in enumerate(store_ids, start=1):
        food_payload = {
            "name": f"Food for Store {i}",
            "description": f"Test food {i}",
            "category": "main_meals",
            "main_ingredients": ["rice", "chicken"],
            "taste_profile": ["savory"],
            "texture": ["soft"],
            "mood_tags": ["comfort"],
            "store_id": store_id
        }

        url = f"{BASE_URL}/foods"
        print_request("POST", url, food_payload)
        response = requests.post(url, json=food_payload, headers=headers)
        print_response(response)

        if response.status_code == 201:
            food_id = response.json()["id"]
            food_ids.append(food_id)
            print(f"✅ Created Food for Store #{i} (Food ID={food_id})")

    # ===============================
    # 4. Create reviews (review 2 Jakarta stores, 1 Bandung store)
    # ===============================
    if len(food_ids) >= 3:
        reviews_payload = [
            {
                "food_id": food_ids[0],
                "store_id": store_ids[0],
                "rating": 4.5,
                "comment": "Great food in Jakarta!"
            },
            {
                "food_id": food_ids[1],
                "store_id": store_ids[1],
                "rating": 4.0,
                "comment": "Nice place in Jakarta"
            },
            {
                "food_id": food_ids[2],
                "store_id": store_ids[2],
                "rating": 5.0,
                "comment": "Excellent food in Bandung!"
            }
        ]

        for i, review_data in enumerate(reviews_payload, start=1):
            url = f"{BASE_URL}/reviews"
            print_request("POST", url, review_data)
            response = requests.post(url, json=review_data, headers=headers)
            print_response(response)
            print_result(f"Create Review #{i}", response.status_code == 201)

    # ===============================
    # 5. Test store_in_city_badges endpoint
    # ===============================
    url = f"{BASE_URL}/client-badges/store-in-city-badges"
    print_request("POST", url)
    response = requests.post(url, headers=headers)
    print_response(response)
    success = response.status_code == 200
    print_result("Calculate Store in City Badges", success)

    if success:
        data = response.json()
        print("\n  🏆 Badge Results:")
        print(f"    Total Cities: {data.get('total_cities')}")
        print(f"    Total Reviewed Stores: {data.get('total_reviewed_stores')}")
        
        badges = data.get('badges', [])
        for badge in badges:
            print(f"\n    📍 City: {badge['city']}")
            print(f"       Badge: {badge['badge_percentage']}%")
            print(f"       Reviewed: {badge['reviewed_count']}/{badge['total_stores']} stores")
            print(f"       Stores: {[s['name'] for s in badge['reviewed_stores']]}")

    print("\n✔ Client badges API test completed.\n")


# ========== AI API TESTS ==========


def test_ai_endpoints():
    """Test all AI-powered endpoints"""
    global auth_token
    print_section("AI API ENDPOINT TESTS")

    # ===============================
    # 0. LOGIN as Client
    # ===============================
    login_data = {
        "username": "client@gmail.com",
        "password": "client"
    }
    url = f"{BASE_URL}/auth/login"
    response = requests.post(url, data=login_data)
    print_response(response)
    success = response.status_code == 200
    print_result("Login Client for AI Tests", success)

    if not success:
        print("❌ Login failed — cannot continue AI tests")
        return

    auth_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    print(f"🔑 Token: {auth_token[:30]}...")

    # ===============================
    # 1. Create Test Store for AI Tests
    # ===============================
    store_payload = {
        "name": "AI Test Cafe",
        "description": "Cozy cafe with amazing coffee and pastries",
        "address": "AI Street No. 123",
        "province": "DKI Jakarta",
        "city": "Jakarta Selatan",
        "latitude": -6.2297,
        "longitude": 106.8309
    }

    url = f"{BASE_URL}/stores"
    print_request("POST", url, store_payload)
    response = requests.post(url, json=store_payload, headers=headers)
    print_response(response)

    if response.status_code not in [200, 201]:
        print("❌ Store creation failed for AI tests")
        store_id = None
    else:
        store_id = response.json()["id"]
        print(f"✅ Created Test Store ID = {store_id}")

    # ===============================
    # 2. Create Test Foods for AI Tests
    # ===============================
    foods_payload = [
        {
            "name": "Spicy Ramen",
            "description": "Hot and spicy Japanese noodles",
            "category": "main_meals",
            "main_ingredients": ["noodles", "broth", "chili"],
            "taste_profile": ["spicy", "savory"],
            "texture": ["soft"],
            "mood_tags": ["energized", "comfort"],
            "store_id": store_id
        },
        {
            "name": "Matcha Latte",
            "description": "Smooth and creamy green tea drink",
            "category": "beverages",
            "main_ingredients": ["matcha", "milk"],
            "taste_profile": ["sweet", "earthy"],
            "texture": ["smooth"],
            "mood_tags": ["relaxed", "focused"],
            "store_id": store_id
        },
        {
            "name": "Chocolate Cake",
            "description": "Rich chocolate dessert",
            "category": "desserts",
            "main_ingredients": ["chocolate", "flour", "sugar"],
            "taste_profile": ["sweet"],
            "texture": ["soft", "moist"],
            "mood_tags": ["happy", "comfort"],
            "store_id": store_id
        }
    ]

    food_ids = []
    for i, food in enumerate(foods_payload, start=1):
        url = f"{BASE_URL}/foods"
        print_request("POST", url, food)
        response = requests.post(url, json=food, headers=headers)
        print_response(response)

        if response.status_code == 201:
            food_id = response.json()["id"]
            food_ids.append(food_id)
            print(f"✅ Created Test Food #{i}: {food['name']} (ID={food_id})")
        else:
            print(f"❌ Failed to create test food #{i}")

    # ===============================
    # 3. TEST AI STORE ENDPOINTS
    # ===============================
    
    # Test: Search Stores
    url = f"{BASE_URL}/ai/search-stores?query=cozy cafe with coffee"
    print_request("GET", url)
    response = requests.get(url, headers=headers)
    print_response(response)
    print_result("AI Search Stores", response.status_code == 200)

    # Test: Recommend Stores
    url = f"{BASE_URL}/ai/recommend-stores?preferences=I want a quiet place for studying"
    print_request("GET", url)
    response = requests.get(url, headers=headers)
    print_response(response)
    print_result("AI Recommend Stores", response.status_code == 200)

    # ===============================
    # 4. TEST AI FOOD ENDPOINTS
    # ===============================
    
    # Test: Search Foods (basic)
    url = f"{BASE_URL}/ai/search-foods?query=spicy comfort food&limit=5"
    print_request("GET", url)
    response = requests.get(url, headers=headers)
    print_response(response)
    success = response.status_code == 200
    print_result("AI Search Foods (Basic)", success)

    # Test: Search Foods (with filters)
    url = f"{BASE_URL}/ai/search-foods?query=sweet dessert&limit=5&category=desserts"
    print_request("GET", url)
    response = requests.get(url, headers=headers)
    print_response(response)
    success = response.status_code == 200
    print_result("AI Search Foods (With Category Filter)", success)

    # Test: Recommend Foods by Mood
    url = f"{BASE_URL}/ai/recommend-foods?query=I feel stressed and need comfort food&limit=5"
    print_request("GET", url)
    response = requests.get(url, headers=headers)
    print_response(response)
    success = response.status_code == 200
    print_result("AI Recommend Foods by Mood", success)

    if success:
        data = response.json()
        print(f"  📋 Query: {data.get('query')}")
        print(f"  📊 Total Results: {data.get('total_results')}")

    # Test: Personalized Recommendations
    url = f"{BASE_URL}/ai/personalized-recommendations?limit=5"
    print_request("GET", url)
    response = requests.get(url, headers=headers)
    print_response(response)
    success = response.status_code == 200
    print_result("AI Personalized Recommendations", success)

    if success:
        data = response.json()
        print(f"  📊 Total Recommendations: {data.get('total_results')}")

    # ===============================
    # 5. TEST AI DESCRIPTION GENERATION
    # ===============================
    
    # Test: Generate Food Description
    # Use the first created food ID
    if not food_ids:
        print("⚠️ No food created, skipping description generation tests")
    else:
        test_food_id = food_ids[0]  # Use first created food
        
        # No request body needed - uses existing food data
        url = f"{BASE_URL}/ai/generate-food-description/{test_food_id}"
        print_request("POST", url, data=None)
        response = requests.post(url, headers=headers)
        print_response(response)
        success = response.status_code == 200
        print_result("AI Generate Food Description", success)

        if success:
            data = response.json()
            print("  📝 Generated Description:")
            print(f"    Short: {data.get('short_description', '')[:100]}...")
            print(f"    Long: {data.get('long_description', '')[:100]}...")
            print(f"    Selling Points: {len(data.get('selling_points', []))} points")

        # Test: Enhance Food Description
        # No request body needed - uses existing food description
        url = f"{BASE_URL}/ai/generate-enhanced-food-description/{test_food_id}"
        print_request("POST", url, data=None)
        response = requests.post(url, headers=headers)
        print_response(response)
        success = response.status_code == 200
        print_result("AI Enhance Food Description", success)

        if success:
            data = response.json()
            print(f"  📝 Enhanced Description: {data.get('enhanced_description', '')[:150]}...")

    print("\n✔ All AI API tests completed.\n")


# ========== MAIN TEST RUNNER ==========


def run_all_tests():
    """Run all API tests"""
    print("\n" + "🚀" * 40)
    print("  MOOD TO MAKAN API COMPREHENSIVE TEST SUITE")
    print("  WITH DETAILED REQUEST/RESPONSE LOGGING")
    print("🚀" * 40)
    print(f"\nBase URL: {BASE_URL}")
    
    try:
        # Run tests in order, assumption: the database is empty
        test_auth_and_user()
        test_store_full_flow()
        test_food_endpoints()
        test_user_food_history()
        test_reviews_api()
        test_client_badges_api()
        test_ai_endpoints()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server")
        print(f"Make sure the server is running at {BASE_URL}")
        print("Run: uv run uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
