import requests

# Test Backend (FastAPI)
def test_backend():
    try:
        response = requests.get("http://localhost:8000")
        if response.status_code == 200:
            print("✅ Backend (FastAPI) is running!")
        else:
            print(f"❌ Backend test failed with status code: {response.status_code}")
    except requests.ConnectionError:
        print("❌ Backend (FastAPI) is not reachable!")

# Test Frontend (Nginx)
def test_frontend():
    try:
        response = requests.get("http://localhost")
        if response.status_code == 200:
            print("✅ Frontend (Nginx) is running!")
        else:
            print(f"❌ Frontend test failed with status code: {response.status_code}")
    except requests.ConnectionError:
        print("❌ Frontend (Nginx) is not reachable!")

if __name__ == "__main__":
    print("Running health checks...")
    test_backend()
    test_frontend()
