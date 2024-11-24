from app.auth.services.utils import get_password_hash
from core.db.models import User
from core.db import SessionLocal


def seed_db():
    with SessionLocal() as session:
        if session.query(User).all():
            return
        
        admin = User(
            username="Admin",
            password=get_password_hash("Admin"),
            is_admin=True
        )
        
        session.add(admin)
        session.commit()
