import requests

def test_github_api():
    url = "https://api.github.com"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("GitHub API is accessible.")
        else:
            print(f"Failed to access GitHub API. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def test_github_api_with_token(token):
    url = "https://api.github.com"
    headers = {"Authorization": f"token {token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("GitHub API is accessible with token.")
        else:
            print(f"Failed to access GitHub API with token. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Test without token
    test_github_api()
    
    # Test with token
    # Prompt user to input their GitHub API token
    user_token = input("Please enter your GitHub API token: ")
    test_github_api_with_token(user_token) 