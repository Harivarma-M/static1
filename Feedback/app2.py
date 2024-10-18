from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database configuration
DB_NAME = 'feedback.db'

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            rating INTEGER,
            subject TEXT,
            feedback_type TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    rating = int(request.form['rating'])
    subject = request.form['subject']
    feedback_type = request.form['feedbackType']
    message = request.form['message']

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Insert feedback into the database
    cursor.execute('''
        INSERT INTO feedback (name, email, rating, subject, feedback_type, message)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, rating, subject, feedback_type, message))

    conn.commit()
    conn.close()

    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
