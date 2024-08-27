import requests

# Replace 'your_github_username' with your actual GitHub username
username = 'your_github_username'

# Fetch followers
followers_url = f'https://api.github.com/users/{username}/followers'
followers = requests.get(followers_url).json()

# Fetch following
following_url = f'https://api.github.com/users/{username}/following'
following = requests.get(following_url).json()

# Extract usernames
followers_usernames = {user['login'] for user in followers}
following_usernames = {user['login'] for user in following}

# Compare followers with following
not_following_back = following_usernames - followers_usernames
not_followed_by = followers_usernames - following_usernames

# Output accounts that not following back
print("Accounts you're following but not following you back:")
print(not_following_back)

# Output account that you don't follow back
print("\nAccounts following you but you're not following back:")
print(not_followed_by)
