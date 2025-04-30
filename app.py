from flask import Flask, request, jsonify, render_template
from recommendation_model import get_recommendations
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Check if request is JSON (e.g. API call) or from a web form
    if request.is_json:
        data = request.get_json()
        genre = data.get('genre', '').lower()
        decade = data.get('decade', '').lower()
    else:
        genre = request.form.get('genre', '').lower()
        decade = request.form.get('decade', '').lower()

    # Debug print to terminal
    print("User selected genre (normalized):", genre)
    print("User selected decade (normalized):", decade)

    # Get recommendations
    recommendations = get_recommendations(genre, decade)

    # Return to frontend or API
    if request.is_json:
        return jsonify(recommendations)
    else:
        return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
