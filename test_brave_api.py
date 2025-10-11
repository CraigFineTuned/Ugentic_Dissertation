import requests
import urllib.parse
import json
import traceback

BRAVE_API_KEY = "BSAGLf6JqzrpVxKl3ZSRyRyRlGi9RUIx-"
QUERY = "test"

def test_brave_search():
    headers = {"Accept": "application/json", "X-Subscription-Token": BRAVE_API_KEY}
    url = f"https://api.search.brave.com/res/v1/web/search?q={urllib.parse.quote(QUERY)}"
    print(f"Testing Brave Search with URL: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"Brave API response: {json.dumps(data, indent=2)}")
        if data.get("web") and data["web"].get("results"):
            print(f"Found {len(data['web']['results'])} results.")
        else:
            print("No web results found.")
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_brave_search()