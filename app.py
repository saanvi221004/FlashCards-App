from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'flashcards.db'

@app.route('/')
def welcome():
    return render_template('welcome.html')
    
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT NOT NULL,
            is_learned INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/home')
def home():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flashcards')
    cards = cursor.fetchall()
    conn.close()
    return render_template('home.html', cards=cards)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        category = request.form['category']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO flashcards (question, answer, category) VALUES (?, ?, ?)',
                       (question, answer, category))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/mark/<int:card_id>')
def mark_as_learned(card_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE flashcards SET is_learned = 1 WHERE id = ?', (card_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
