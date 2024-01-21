from app import create_app
from app.extensions import db
from app.models import *


app = create_app()

def update_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True)