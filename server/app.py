from flask import Flask, jsonify, request, session
from flask_migrate import Migrate
from models import db, Article

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super-secret"  # Needed for sessions

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return "<h1>Cookies & Sessions Lab</h1>"


@app.route('/articles')
def get_articles():
    articles = Article.query.all()
    return jsonify([
        {
            "id": a.id,
            "title": a.title,
            "author": a.author,
            "preview": a.content[:50],
            "date": a.date.isoformat()
        }
        for a in articles
    ])


@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize session counter if missing
    if 'page_views' not in session:
        session['page_views'] = 0

    # Increment first
    session['page_views'] += 1

    # Enforce max 3 allowed, block on 4th+
    if session['page_views'] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401

    # Fetch article from DB
    article = Article.query.get(id)
    if not article:
        return jsonify({"error": "Article not found"}), 404

    # Calculate minutes_to_read
    words = len(article.content.split())
    minutes = max(1, words // 200)

    return jsonify({
        "id": article.id,
        "author": article.author,
        "title": article.title,
        "content": article.content,
        "preview": article.content[:50],
        "minutes_to_read": minutes,
        "date": article.date.isoformat()
    })


if __name__ == '__main__':
    app.run(port=5555, debug=True)
