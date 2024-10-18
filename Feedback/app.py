from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database setup
conn = sqlite3.connect('feedback.db')
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

@app.route('/')
def index():
    # Fetch feedback from the database
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM feedback')
    feedback = cursor.fetchall()
    conn.close()
    return render_template('index.html', feedback=feedback)

@app.route('/submit', methods=['POST'])
def submit():
    # Handle form submission and insert feedback into the database
    name = request.form['name']
    email = request.form['email']
    rating = int(request.form['rating'])
    subject = request.form['subject']
    feedback_type = request.form['feedbackType']
    message = request.form['message']


    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (name, email, rating, subject, feedback_type, message)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, rating, subject, feedback_type, message))

    conn.commit()
    conn.close()


    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

