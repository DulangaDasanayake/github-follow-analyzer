# GitHub Follower-Following Manager

This Python script helps you manage your GitHub followers and following lists. It identifies users you're following who don't follow you back and users who follow you but whom you're not following back. You can also automate following or unfollowing based on these lists.


## Features

- **Follower vs Following Comparison**:  
  Easily see who isn't following you back and who you're not following back.  
- **Automated Management**:  
  - Unfollow users who don't follow you back.  
  - Follow users who follow you but whom you're not following.  
- **Detailed Output**:  
  Prints lists of discrepancies for easy review.  


## Requirements

- **Python 3.x**  
- **Requests library** (Install using `pip install requests`)  


## How It Works

1. **Authentication**:  
   The script uses your GitHub username and personal access token to access the GitHub API.  
2. **Comparison**:  
   It fetches the lists of your followers and following, then compares them to identify differences.  
3. **Automated Actions**:  
   - Unfollows users who don't follow you back.  
   - Follows users who follow you but whom you're not following.  
4. **Output**:  
   Displays two lists:  
   - Users you're following but who don't follow you back.  
   - Users following you but whom you're not following.  


## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/your_username/github-follow-analyzer.git
   cd github-follow-analyzer
   ```
2. Replace the placeholders in the script:  
   - `'your_github_username'`: Your GitHub username.  
   - `'GITHUB_TOKEN'`: Your personal access token.  
3. Run the script:
   ```bash
   python github_follow_analyzer.py
   ```
4. Review the output and check the automated actions.


## Troubleshooting

### Common Issues and Fixes:

#### 1. **Unfollowing Doesn't Work**:
   - Ensure the access token has the correct permissions (the `user` scope).  
   - Check the API response for errors or rate limits:
     ```python
     print(response.status_code, response.text)
     ```
   - Verify that the API endpoint is correct:
     ```
     DELETE https://api.github.com/user/following/{username}
     ```

#### 2. **API Rate Limits**:
   - GitHub's API allows 5,000 requests per hour for authenticated users.  
   - Check your remaining requests using:
     ```python
     rate_limit_url = 'https://api.github.com/rate_limit'
     response = requests.get(rate_limit_url, headers=headers)
     print(response.json())
     ```
   - Add delays between requests to avoid hitting limits:
     ```python
     time.sleep(1)  # Add a 1-second delay
     ```

#### 3. **Token Issues**:
   - Ensure the token is valid and has not expired.  
   - Regenerate the token if needed and update it in the script.  

#### 4. **Environment Variables for Security**:
   - Avoid hardcoding your token in the script. Use environment variables instead:
     ```python
     import os
     token = os.getenv('GITHUB_TOKEN')
     ```


## Example Output

```plaintext
Accounts you're following but not following you back:
{'user1', 'user2', 'user3'}

Accounts following you but you're not following back:
{'user4', 'user5'}
```


## Notes

- This script is for personal use and respects GitHub's API terms.  
- Be mindful of your connections before automating follow/unfollow actions.  
- Always review the lists before making changes.  
