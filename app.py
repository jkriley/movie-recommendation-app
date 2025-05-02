from flask import Flask, request, jsonify, render_template
from recommendation_model import get_recommendations, load_data
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    if request.is_json:
        data = request.get_json()
        genre = data.get('genre', '').lower().strip()
        decade = data.get('decade', '').lower().strip()
    else:
        genre = request.form.get('genre', '').lower().strip()
        decade = request.form.get('decade', '').lower().strip()

    print("User selected genre:", genre)
    print("User selected decade:", decade)

    try:
        recommendations = get_recommendations(genre, decade)
    except Exception as e:
        print("❌ Error during recommendation:", e)
        recommendations = ["Something went wrong. Please try again."]

    if request.is_json:
        return jsonify(recommendations)
    else:
        return render_template('index.html', recommendations=recommendations)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("📦 Preloading model data...")
    load_data()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
