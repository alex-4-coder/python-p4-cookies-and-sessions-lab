from app import app, db
from models import Article
from datetime import datetime

with app.app_context():
    print("Seeding data...")

    Article.query.delete()

    articles = [
        Article(
            title="Flask Cookies and Sessions",
            content="This article explains how cookies and sessions work in Flask applications...",
            author="Alex",
            date=datetime.utcnow()
        ),
        Article(
            title="Understanding SQLAlchemy",
            content="SQLAlchemy is a powerful ORM for Python that allows developers to interact with databases...",
            author="Stacey",
            date=datetime.utcnow()
        ),
        Article(
            title="React and Flask Integration",
            content="You can connect a Flask backend with a React frontend to build full-stack applications...",
            author="Jane",
            date=datetime.utcnow()
        ),
    ]

    db.session.add_all(articles)
    db.session.commit()

    print("Seeding complete!")
