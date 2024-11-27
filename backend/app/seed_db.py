from app.auth.services.utils import get_password_hash
from core.db.models import Answer, Question, Quiz, User
from core.db import SessionLocal


def seed_db():
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
