# GitHub Follower Manager - Beginner's Guide

This guide will walk you through what you need to know to use the **GitHub Follower Manager** web app, a simple tool to manage your GitHub followers and those you are following. The app will help you identify who is not following you back and who you are not following back.

## What is the GitHub Follower Manager?

The **GitHub Follower Manager** is a web app that interacts with GitHub's API to fetch your followers and the accounts you are following. It then compares both lists and identifies:
- **Users who don't follow you back**
- **Users you are not following back**

You can use this information to clean up your follower list or manage your GitHub connections.

## What You Need to Know

### 1. **GitHub Username and Personal Access Token**

To use this app, you need:
- **Your GitHub username**: This is the username you use to log into GitHub (e.g., `your_username`).
- **Personal Access Token (PAT)**: This is an authentication token that lets the app access your GitHub account data. You can create a PAT on GitHub.

### How to Create a Personal Access Token (PAT)
1. Go to [GitHub Settings](https://github.com/settings/tokens).
2. Click **Generate new token**.
3. Give the token a description and select the following scopes:
   - **repo** (Full control of private repositories)
   - **read:user** (Read all user profile data)
   - **user:follow** (Access to follow/unfollow users)
4. Click **Generate token** and save the token securely.

### 2. **Using the Web Interface**
Once the app is deployed, follow these steps:
1. **Open the app URL**: After deploying the app to Render (or any hosting platform), you will get a URL like `https://your-app.onrender.com`.
2. **Input Your GitHub Information**:
   - **GitHub Username**: Enter your GitHub username in the text box.
   - **Personal Access Token**: Enter your generated PAT in the password field.
3. **Click the "Analyze" Button**: Once you submit the form, the app will process your followers and following data.

### 3. **Understanding the Results**
After clicking "Analyze," the app will show you:
- **Not Following Back**: Users you are following but who are not following you back.
- **Not Followed Back**: Users who follow you but you haven't followed back.

You can use this data to decide whom to unfollow or follow back.

## How Does It Work?

### The Technical Part:
- The app fetches your **followers** and **following** lists from GitHub using their API.
- It compares the lists and identifies differences:
  - **Following but not followed back**: You follow them, but they don’t follow you.
  - **Followed but not following back**: They follow you, but you’re not following them.
- The app then displays these lists for you to manage.

## Limitations and Notes
- **API Rate Limits**: GitHub imposes a rate limit on API requests. If you have a lot of followers, you might need to wait before making another request.
- **Security**: Do not share your Personal Access Token with others. Keep it secure!

## Troubleshooting
- **Invalid Token**: If you get an error saying "Invalid token," double-check your personal access token to ensure it's correctly entered.
- **Rate Limiting**: GitHub’s API may limit how often you can make requests. If you encounter a rate limit error, wait for some time and try again.

## Conclusion
This app is a simple yet powerful tool for managing your GitHub followers and keeping your account organized. Whether you're a casual user or a GitHub power user, the **GitHub Follower Manager** can help streamline your connections and improve your GitHub experience.

---

Here's a directory structure and the file names you'll need for your Flask-based GitHub Follower Manager app:

### Project Structure:

```
/your-project-folder
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile               # Specifies how to run the app on Render
└── /templates
    └── index.html         # HTML template for the web interface
```

### File Details:

1. **app.py** (Flask Application):
   - This is your main Flask application file where the logic for interacting with GitHub's API and managing followers is defined.

   ```python
   from flask import Flask, request, jsonify, render_template
   import requests

   app = Flask(__name__)

   @app.route('/')
   def home():
       return render_template('index.html')  # Create an HTML form for user input

   @app.route('/manage_followers', methods=['POST'])
   def manage_followers():
       username = request.form['username']
       token = request.form['token']

       headers = {
           'Authorization': f'token {token}',
           'Accept': 'application/vnd.github.v3+json'
       }

       def fetch_all(url):
           results = []
           while url:
               response = requests.get(url, headers=headers)
               if response.status_code != 200:
                   return f"Failed to fetch: {url}"
               results.extend(response.json())
               url = response.links.get('next', {}).get('url')  # Get next page URL
           return results

       followers_url = f'https://api.github.com/users/{username}/followers'
       following_url = f'https://api.github.com/users/{username}/following'

       followers = {user['login'] for user in fetch_all(followers_url)}
       following = {user['login'] for user in fetch_all(following_url)}

       not_following_back = list(following - followers)
       not_followed_back = list(followers - following)

       return jsonify({
           "not_following_back": not_following_back,
           "not_followed_back": not_followed_back
       })

   if __name__ == "__main__":
       app.run(debug=True)
   ```

2. **requirements.txt** (Python dependencies):
   - List the required Python libraries that will be installed when the app is deployed.

   ```
   Flask
   requests
   gunicorn
   ```

3. **Procfile** (Render deployment):
   - Specifies the start command for your web app on Render.

   ```
   web: gunicorn app:app
   ```

   This tells Render to use **gunicorn** to serve your Flask app (`app:app` points to the `app` object in `app.py`).

4. **templates/index.html** (HTML form for user input):
   - This is the frontend interface that allows users to enter their GitHub username and token.

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>GitHub Follower Manager</title>
   </head>
   <body>
       <h1>GitHub Follower Manager</h1>
       <form action="/manage_followers" method="POST">
           <label for="username">GitHub Username:</label>
           <input type="text" id="username" name="username" required>
           <br>
           <label for="token">Personal Access Token:</label>
           <input type="password" id="token" name="token" required>
           <br>
           <button type="submit">Analyze</button>
       </form>
   </body>
   </html>
   ```

---

### Deploying to Render:

1. **GitHub Repository**:
   - Create a new repository on GitHub and push all these files into it.

2. **Render Deployment**:
   - Sign in to [Render](https://render.com/).
   - Create a new **Web Service** and connect your GitHub repository.
   - Follow the setup steps (you can leave the default **build command** and **start command** as `pip install -r requirements.txt` and `gunicorn app:app`).
   
3. **Environment Variables**:
   - In Render, add the **GitHub Personal Access Token** as an environment variable (optional if you prefer not to hardcode it).

4. **Access the Web App**:
   - Once Render finishes deploying, you’ll be given a URL (e.g., `https://your-app.onrender.com`). This is where your Flask app will be running.

---
