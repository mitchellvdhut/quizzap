import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth.services.utils import get_password_hash
from core.db.models import Answer, Question, Quiz, User
from core.db import SessionLocal, Base

def seed_db():
    if os.getenv("env") == "test":
        seed_test_db()
    else:  # pragma: no cover
        seed_normal_db()

def seed_normal_db():  # pragma: no cover
    with SessionLocal() as session:
        admin = session.query(User).where(User.username == "Admin").first()
        if not admin:
            admin = User(
                username="Admin",
                password=get_password_hash("Admin"),
                is_admin=True
            )
        
            session.add(admin)
        
        quiz = session.query(Quiz).where(Quiz.name == "The Greg quiz!").first()
        if not quiz:
            quiz = Quiz(
                name="The Greg quiz!",
                description="The one and only!",
                creator=admin
            )

            question_1 = Question(
                    name="Important Greg question",
                    description="Is greg disappointed?"
                )

            question_1_answer_1 = Answer(
                        description="Yes",
                        is_correct=True
                    )
            question_1_answer_2 = Answer(
                        description="No"
                    )
            
            question_1.answers.append(question_1_answer_1)
            question_1.answers.append(question_1_answer_2)
            
            quiz.questions.append(question_1)

            session.add(quiz)

        session.commit()

def seed_test_db():
    # we can now construct a Session() without needing to pass the
    # engine each time

    if os.path.isfile("test.db"):
        os.remove("test.db")    

    engine = create_engine("sqlite:///./test.db")
        
    Base.metadata.create_all(engine)


    logging.info("IM BEING CALLED")

    # a sessionmaker(), also in the same scope as the engine
    Session = sessionmaker(engine)

    with Session() as session:
        # Add your things here
        admin_pass = get_password_hash("admin")

        admin_user = User(
            username="admin",
            password=admin_pass,
            is_admin=True,
        )

        normal_user = User(
            username="normal_user",
            password=get_password_hash("normal_user")
        )

        session.add_all([admin_user, normal_user])
        session.commit()

    # needed to call this because test.db couldnt be deleted anymore
    engine.dispose()
