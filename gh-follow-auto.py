import requests
import os
import time

# Replace with your GitHub username and load token from environment
username = os.getenv('GITHUB_USERNAME')
token = os.getenv('GITHUB_TOKEN')

# Headers for authentication
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Helper function to handle pagination
def fetch_all(url):
    results = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch: {url}")
            break
        results.extend(response.json())
        url = response.links.get('next', {}).get('url')  # Get next page URL
    return results

# Fetch followers and following
followers_url = f'https://api.github.com/users/{username}/followers'
following_url = f'https://api.github.com/users/{username}/following'

followers = {user['login'] for user in fetch_all(followers_url)}
following = {user['login'] for user in fetch_all(following_url)}

# Identify users
not_following_back = following - followers
not_followed_back = followers - following

# Unfollow users not following back
for user in not_following_back:
    unfollow_url = f'https://api.github.com/user/following/{user}'
    response = requests.delete(unfollow_url, headers=headers)
    if response.status_code == 204:
        print(f"Unfollowed {user}")
    else:
        print(f"Failed to unfollow {user}")
    time.sleep(1)  # Delay between requests

# Follow users not followed back
for user in not_followed_back:
    follow_url = f'https://api.github.com/user/following/{user}'
    response = requests.put(follow_url, headers=headers)
    if response.status_code == 204:
        print(f"Followed {user}")
    else:
        print(f"Failed to follow {user}")
    time.sleep(1)  # Delay between requests

print("\nAccounts you're following but not following you back:")
print(not_following_back)

print("\nAccounts following you but you're not following back:")
print(not_followed_back)
