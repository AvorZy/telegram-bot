import requests

def test_image_url():
    url = "https://pub-133f8593b35749f28fa090bc33925b31.r2.dev/7dc0047c-95c7-4d24-be97-c97705772c9d.jpg"
    
    try:
        # Test HEAD request
        head_response = requests.head(url, timeout=10)
        print(f"HEAD - Status: {head_response.status_code}")
        print(f"HEAD - Content-Type: {head_response.headers.get('content-type')}")
        print(f"HEAD - Content-Length: {head_response.headers.get('content-length')}")
        
        # Test GET request to see actual content
        get_response = requests.get(url, timeout=10)
        print(f"\nGET - Status: {get_response.status_code}")
        print(f"GET - Content-Type: {get_response.headers.get('content-type')}")
        print(f"GET - Content-Length: {len(get_response.content)}")
        print(f"GET - First 100 bytes: {get_response.content[:100]}")
        
        # Check if it's actually an image
        if get_response.content.startswith(b'\xff\xd8\xff'):
            print("✅ Content starts with JPEG magic bytes")
        elif get_response.content.startswith(b'\x89PNG'):
            print("✅ Content starts with PNG magic bytes")
        else:
            print(f"❌ Content doesn't start with image magic bytes: {get_response.content[:10]}")
            print(f"❌ Content as text: {get_response.content[:200].decode('utf-8', errors='ignore')}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_image_url()