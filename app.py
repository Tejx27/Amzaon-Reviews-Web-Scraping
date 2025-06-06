from flask import Flask, request, jsonify
from textblob import TextBlob
import mysql.connector
import threading

app = Flask(__name__)

# Connect to MySQL database
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="IPHONE"
    )
    return conn

# Home route
@app.route('/')
def home():
    return "Welcome to the Amazon Reviews API!"

# Sentiment Analysis API
@app.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.json
    review_text = data.get('review_text', '')
    
    if not review_text:
        return jsonify({'error': 'No review text provided'}), 400
    
    # Perform sentiment analysis
    blob = TextBlob(review_text)
    sentiment_score = blob.sentiment.polarity  # Range from -1 (negative) to +1 (positive)

    return jsonify({'sentiment_score': sentiment_score})

# Review Retrieval API
@app.route('/reviews', methods=['GET'])
def get_reviews():
    color = request.args.get('color')
    style_name = request.args.get('style_name')
    verified_purchase = request.args.get('verified_purchase')

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM reviews WHERE color=%s AND style_name=%s AND verified_purchase=%s"
    cursor.execute(query, (color, style_name, verified_purchase))
    
    reviews = cursor.fetchall()
    
    cursor.close()
    conn.close()

    # Convert fetched data to a list of dictionaries for JSON response
    reviews_list = []
    for review in reviews:
        reviews_list.append({
            'review_title': review[0],
            'review_text': review[1],
            'style_name': review[2],
            'color': review[3],
            'verified_purchase': review[4]
        })

        return jsonify(reviews_list)
# Run the app in a separate thread
def run_app():
    app.run(port=5001)

# Start the Flask app in a new thread
threading.Thread(target=run_app).start()