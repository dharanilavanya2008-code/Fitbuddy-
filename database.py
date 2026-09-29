from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    username = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    goal = Column(String)
    intensity = Column(String)


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    original_plan = Column(Text)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text)


Base.metadata.create_all(bind=engine)


def save_user(user_data):
    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(User.user_id == user_data.user_id)
            .first()
        )

        if existing_user:
            existing_user.username = user_data.username
            existing_user.age = user_data.age
            existing_user.weight = user_data.weight
            existing_user.goal = user_data.goal
            existing_user.intensity = user_data.intensity
        else:
            user = User(
                user_id=user_data.user_id,
                username=user_data.username,
                age=user_data.age,
                weight=user_data.weight,
                goal=user_data.goal,
                intensity=user_data.intensity
            )

            db.add(user)

        db.commit()

    finally:
        db.close()


def save_plan(user_id, original_plan, nutrition_tip):
    db = SessionLocal()

    try:
        plan = Plan(
            user_id=user_id,
            original_plan=original_plan,
            nutrition_tip=nutrition_tip
        )

        db.add(plan)
        db.commit()

    finally:
        db.close()


def get_user(user_id):
    db = SessionLocal()

    try:
        return (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

    finally:
        db.close()


def get_original_plan(user_id):
    db = SessionLocal()

    try:
        plan = (
            db.query(Plan)
            .filter(Plan.user_id == user_id)
            .order_by(Plan.id.desc())
            .first()
        )

        return plan.original_plan if plan else None

    finally:
        db.close()


def update_plan(user_id, updated_plan):
    db = SessionLocal()

    try:
        plan = (
            db.query(Plan)
            .filter(Plan.user_id == user_id)
            .order_by(Plan.id.desc())
            .first()
        )

        if plan:
            plan.updated_plan = updated_plan
            db.commit()

    finally:
        db.close()


def get_latest_plan(user_id):
    db = SessionLocal()

    try:
        return (
            db.query(Plan)
            .filter(Plan.user_id == user_id)
            .order_by(Plan.id.desc())
            .first()
        )

    finally:
        db.close()


def get_all_users():
    db = SessionLocal()

    try:
        return db.query(User).all()

    finally:
        db.close()


def get_all_plans():
    db = SessionLocal()

    try:
        return db.query(Plan).all()

    finally:
        db.close()


def delete_user(user_id):
    db = SessionLocal()

    try:
        db.query(Plan).filter(Plan.user_id == user_id).delete()
        db.query(User).filter(User.user_id == user_id).delete()

        db.commit()

    finally:
        db.close()