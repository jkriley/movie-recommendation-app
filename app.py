from flask import Flask, request, jsonify, render_template
from recommendation_model import get_recommendations

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    genre = data.get('genre')
    decade = data.get('decade')
    recommendations = get_recommendations(genre, decade)
    return jsonify(recommendations)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

