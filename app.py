from flask import Flask, render_template, request
import mysql.connector
from textblob import TextBlob

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@123",  # <-- IVIDE NINTE MYSQL PASSWORD IDU CHETTA
    database="intern"
)
cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        text = request.form['text']
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0:
            sentiment = "Positive 😊"
        elif polarity < 0:
            sentiment = "Negative 😡"
        else:
            sentiment = "Neutral 😐"
        
        score = round(polarity, 2)
        
        sql = "INSERT INTO reviews (text, sentiment, score) VALUES (%s, %s, %s)"
        cursor.execute(sql, (text, sentiment, score))
        db.commit()
        
        # --- IVIDE MAATTAM ---
        result = {
            'text': text, 
            'sentiment': sentiment, 
            'score': score
        }  # <-- STRING ALLA, DICTIONARY KODUKKANAM
        # --- MAATTAM THEERNNU ---
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)