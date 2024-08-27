import requests

# Replace with your GitHub username and personal access token
username = 'your_github_username'
token = 'your_github_token'

# Headers for authentication
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Fetch followers
followers_url = f'https://api.github.com/users/{username}/followers'
followers = requests.get(followers_url, headers=headers).json()

# Fetch following
following_url = f'https://api.github.com/users/{username}/following'
following = requests.get(following_url, headers=headers).json()

# Extract usernames
followers_usernames = {user['login'] for user in followers}
following_usernames = {user['login'] for user in following}

# Identify users not following back
not_following_back = following_usernames - followers_usernames
# Identify users you are not following back
not_followed_back = followers_usernames - following_usernames

# Unfollow users not following you back
for user in not_following_back:
    unfollow_url = f'https://api.github.com/user/following/{user}'
    response = requests.delete(unfollow_url, headers=headers)
    if response.status_code == 204:
        print(f"Unfollowed {user}")
    else:
        print(f"Failed to unfollow {user}")

# Automatically follow users you're not following back
for user in not_followed_back:
    follow_url = f'https://api.github.com/user/following/{user}'
    response = requests.put(follow_url, headers=headers)
    if response.status_code == 204:
        print(f"Followed {user}")
    else:
        print(f"Failed to follow {user}")

print("\nAccounts you're following but not following you back:")
print(not_following_back)

print("\nAccounts following you but you're not following back:")
print(not_followed_back)
