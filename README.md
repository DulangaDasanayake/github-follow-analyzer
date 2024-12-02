# GitHub Follower-Following Comparator

This Python program compares your GitHub followers and following lists. It identifies accounts that you're following but aren't following you back and vice versa. The program helps you keep track of your connections on GitHub.

## Features

- **Follower vs Following Comparison:** Easily see who isn't following you back and who you're not following back.
- **Simple and Clean:** No auto-unfollow feature, giving you full control over your connections.

## How It Works

1. **Authentication:** The program uses your GitHub username and personal access token to access the GitHub API.
2. **Comparison:** It fetches the lists of your followers and following, then compares them to identify differences.
3. **Output:** The program prints out two lists:
   - Users you follow but who don't follow you back.
   - Users who follow you but whom you're not following back.

## Requirements

- Python 3.x
- `requests` library

Install the `requests` library if you haven't already:

```bash
pip install requests
```

## Usage

1. Clone this repository.
2. Replace `'your_github_username'` and `'your_github_token'` in the script with your GitHub credentials.
3. Run the script:

```bash
python compare_github_followers.py
```

4. Review the output to see who you might want to unfollow or follow back.

## Disclaimer

This program respects your privacy and does not perform any actions on your behalf (like unfollowing users). It’s designed to help you analyze your GitHub connections manually.

---

# Troubleshooting the issues

## Troubleshooting Guide for GitHub Unfollowing Script


If your script reports that it has unfollowed users but the changes are not reflected, follow these troubleshooting steps:

## 1. Check API Response
Ensure that the API responses are correctly handled and check the actual HTTP status codes returned. For unfollowing, a successful request should return a `204 No Content` status. If not, print the response content to debug:

```python
if response.status_code == 204:
    print(f"Unfollowed {user}")
else:
    print(f"Failed to unfollow {user}. Status code: {response.status_code}, Response: {response.text}")
```

## 2. Verify Permissions
Make sure the access token has the correct permissions. The `user` scope should be sufficient, but double-check the token settings to confirm it has the right scopes.

## 3. Check Rate Limits
GitHub has rate limits on API requests. Ensure you haven't hit the rate limit for the `DELETE /user/following/:username` endpoint. Check the headers of the API response for rate limit status:

```python
print(response.headers.get('X-RateLimit-Remaining'))
```

## 4. Token Validity
Ensure that your token is valid and has not expired. You can regenerate the token and update your script to use the new token.

## 5. API Endpoint Accuracy
Confirm that the API endpoint for unfollowing is correct. The endpoint should be:

```
DELETE https://api.github.com/user/following/{username}
```

## 6. Check User IDs
Sometimes user names may not resolve correctly if they are incorrect or if there are discrepancies in the API response. Ensure that the usernames in the `not_following_back` set are accurate.

## 7. Try Manual Verification
To rule out issues with the API or token, try manually unfollowing a user on GitHub's website to verify that your account can perform the action without issues.

## Example of Improved Debug Output

Here's an updated version of the unfollowing part of the script with additional debugging information:

```python
# Unfollow users not following you back
for user in not_following_back:
    unfollow_url = f'https://api.github.com/user/following/{user}'
    response = requests.delete(unfollow_url, headers=headers)
    
    if response.status_code == 204:
        print(f"Successfully unfollowed {user}")
    else:
        print(f"Failed to unfollow {user}. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"Rate limit remaining: {response.headers.get('X-RateLimit-Remaining')}")
```

### Suggestions for Improvement:

1. **Error Handling for API Rate Limits**:
   - The GitHub API has a rate limit (usually 5,000 requests per hour for authenticated users). If you exceed this, the script may fail.
   - Include a check for rate limits in the headers.

   ```python
   rate_limit_url = 'https://api.github.com/rate_limit'
   rate_limit = requests.get(rate_limit_url, headers=headers).json()
   remaining = rate_limit['rate']['remaining']
   print(f"Remaining API calls: {remaining}")
   if remaining == 0:
       print("Rate limit exceeded. Try again later.")
       exit()
   ```

2. **Validate Response Data**:
   - Ensure the API responses are successful and contain the expected data before processing.

   ```python
   followers_response = requests.get(followers_url, headers=headers)
   if followers_response.status_code != 200:
       print("Failed to fetch followers. Check your token or API limits.")
       exit()
   followers = followers_response.json()
   ```

3. **Pagination Handling**:
   - The GitHub API paginates responses, providing 30 items per page by default. Add pagination support to fetch all data.

   ```python
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

   followers = fetch_all(followers_url)
   following = fetch_all(following_url)
   ```

4. **Log and Monitor Actions**:
   - Instead of directly unfollowing or following users, log actions into a file for review before execution.

   ```python
   with open('action_log.txt', 'w') as log_file:
       for user in not_following_back:
           log_file.write(f"Unfollow: {user}\n")
       for user in not_followed_back:
           log_file.write(f"Follow: {user}\n")
   ```

5. **Rate-Limit-Friendly Delays**:
   - Add delays between API requests to avoid hitting rate limits quickly.

   ```python
   import time

   for user in not_following_back:
       unfollow_url = f'https://api.github.com/user/following/{user}'
       response = requests.delete(unfollow_url, headers=headers)
       if response.status_code == 204:
           print(f"Unfollowed {user}")
       else:
           print(f"Failed to unfollow {user}")
       time.sleep(1)  # Delay between requests
   ```

6. **Personal Access Token Security**:
   - Avoid hardcoding tokens. Use environment variables for better security.

   ```python
   import os
   token = os.getenv('GITHUB_TOKEN')
   ```

---
