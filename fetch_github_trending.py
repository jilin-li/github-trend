import requests
import base64
import re
from urllib.parse import urljoin, urlparse
from datetime import datetime, timedelta

def fetch_trending_repos(token, days=7):
    url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"token {token}"}
    
    # Get the date N days ago in YYYY-MM-DD format
    past_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    params = {
        "q": f"created:>{past_date}",
        "sort": "stars",
        "order": "desc",
        "per_page": 10  # Limit to top 10 repositories
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Debug: Print the number of items returned
        print(f"Number of repositories found: {len(data.get('items', []))}")
        print(f"Fetching trending repositories created in the last {days} days")
        
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

def extract_images_from_readme(readme_content, repo_url):
    # Use regex to find image URLs in the README content
    image_urls = re.findall(r'!\[.*?\]\((.*?)\)', readme_content)
    # Convert relative URLs to absolute URLs
    absolute_urls = [urljoin(repo_url, url) if not urlparse(url).netloc else url for url in image_urls]
    return absolute_urls

def save_to_markdown(repos, token, days, include_readme=False, filename="trending_repos.md"):
    with open(filename, 'w', encoding='utf-8') as f:
        # Write the timestamp and period at the beginning of the file
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"# GitHub Trending Repositories (Last {days} Days)\n\n")
        f.write(f"**Query Date and Time**: {timestamp}\n\n")
        
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
                    image_urls = extract_images_from_readme(readme_content, repo['html_url'])
                    if image_urls:
                        f.write("### Images\n")
                        for url in image_urls:
                            f.write(f"![Image]({url})\n")
                        f.write("\n")
                        
                        f.write("### README\n")
                        f.write(readme_content)
                        f.write("\n\n")
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    user_token = input("Please enter your GitHub API token: ")
    days = int(input("Enter the number of days to look back (e.g., 7 for one week): "))
    include_readme = input("Do you want to include README files? (yes/no): ").strip().lower() == 'yes'
    
    trending_repos = fetch_trending_repos(user_token, days)
    save_to_markdown(trending_repos, user_token, days, include_readme)