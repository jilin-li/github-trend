import requests
import base64

def fetch_trending_repos(token):
    url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"token {token}"}
    params = {
        "q": "created:>2024-01-01",
        "sort": "stars",
        "order": "desc"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data['items']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def fetch_readme(repo_full_name, token):
    url = f"https://api.github.com/repos/{repo_full_name}/readme"
    headers = {"Authorization": f"token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        content = base64.b64decode(data['content']).decode('utf-8')
        return content
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching README for {repo_full_name}: {e}")
        return None

def save_to_markdown(repos, token, include_readme=False, filename="trending_repos.md"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# GitHub Trending Repositories\n\n")
        for repo in repos:
            f.write(f"## {repo['name']}\n")
            f.write(f"- **URL**: [{repo['name']}]({repo['html_url']})\n")
            f.write(f"- **Stars**: {repo['stargazers_count']}\n")
            f.write(f"- **Description**: {repo['description'] or 'N/A'}\n")
            f.write(f"- **Language**: {repo['language'] or 'N/A'}\n")
            f.write(f"- **Open Issues**: {repo['open_issues_count']}\n")
            f.write(f"- **Forks**: {repo['forks_count']}\n")
            f.write(f"- **Watchers**: {repo['watchers_count']}\n")
            f.write(f"- **Created At**: {repo['created_at'][:10]}\n")
            f.write(f"- **Updated At**: {repo['updated_at'][:10]}\n\n")
            
            if include_readme:
                readme_content = fetch_readme(repo['full_name'], token)
                if readme_content:
                    f.write("### README\n")
                    f.write(readme_content)
                    f.write("\n\n")
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    user_token = input("Please enter your GitHub API token: ")
    include_readme = input("Do you want to include README files? (yes/no): ").strip().lower() == 'yes'
    trending_repos = fetch_trending_repos(user_token)
    save_to_markdown(trending_repos, user_token, include_readme) 