"""
Simple API test script
Run with: python test_api.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8081/api"


def print_response(response, title):
    print(f"\n{'=' * 50}")
    print(f"{title}")
    print(f"{'=' * 50}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")


# Test 1: Register a new user
def test_register():
    url = f"{BASE_URL}/auth/register/"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password2": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    response = requests.post(url, json=data)
    print_response(response, "TEST 1: Register User")
    return response.json() if response.status_code == 201 else None


# Test 2: Login
def test_login():
    url = f"{BASE_URL}/auth/login/"
    data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    response = requests.post(url, json=data)
    print_response(response, "TEST 2: Login User")

    if response.status_code == 200:
        return response.json().get('tokens', {}).get('access')
    return None


# Test 3: Get Profile
def test_get_profile(token):
    url = f"{BASE_URL}/auth/profile/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print_response(response, "TEST 3: Get User Profile")


# Test 4: Create a Post
def test_create_post(token):
    url = f"{BASE_URL}/posts/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "caption": "This is my first test post!",
        "is_public": True
    }
    response = requests.post(url, json=data, headers=headers)
    print_response(response, "TEST 4: Create Post")

    # Get the post ID from the feed since create doesn't return full object
    if response.status_code == 201:
        # Fetch posts to get the ID
        feed_response = requests.get(f"{BASE_URL}/posts/", headers=headers)
        if feed_response.status_code == 200:
            posts = feed_response.json().get('results', [])
            if posts:
                return posts[0]['id']
    return None

# Test 5: Get Posts Feed
def test_get_posts(token):
    url = f"{BASE_URL}/posts/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print_response(response, "TEST 5: Get Posts Feed")


# Test 6: Like a Post
def test_like_post(token, post_id):
    if not post_id:
        print("\nSkipping like test - no post ID")
        return

    url = f"{BASE_URL}/posts/{post_id}/like/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers)
    print_response(response, "TEST 6: Like Post")


# Run all tests
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("STARTING API TESTS")
    print("=" * 50)

    # Test registration
    register_result = test_register()

    # Test login
    token = test_login()

    if token:
        # Test authenticated endpoints
        test_get_profile(token)
        post_id = test_create_post(token)
        test_get_posts(token)
        test_like_post(token, post_id)
    else:
        print("\n❌ Login failed - skipping authenticated tests")

    print("\n" + "=" * 50)
    print("TESTS COMPLETED")
    print("=" * 50 + "\n")