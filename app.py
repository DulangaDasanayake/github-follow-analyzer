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
