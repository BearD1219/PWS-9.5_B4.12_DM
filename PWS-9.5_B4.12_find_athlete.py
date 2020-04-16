import datetime as dt

import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class Athletes(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.INTEGER, primary_key = True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.TEXT)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.TEXT)
    country = sa.Column(sa.TEXT)

class Users(Base):
    __tablename__= "user"
    id = sa.Column(sa.INTEGER, primary_key = True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def query_user_id(session):
    user_data = {}
    id = int(input("Введите ID пользователя: "))
    user = session.query(Users).filter(Users.id == id).first()
    if user is None:
        print("Пользователя с таким ID не существует")
    else:
        user_data["birthdate"] = user.birthdate
        user_data["height"] = user.height
        return user_data

def birthdate_to_dt(birthdate):
    birthdate = birthdate.split("-")
    birthdate = [int(i) for i in birthdate]
    return dt.date(*birthdate)

def nearest_date(user_date, session):
    all_date = session.query(Athletes).all()
    user_date = birthdate_to_dt(user_date)
    near_date = None
    for athlete in all_date:
        athlete_date = birthdate_to_dt(athlete.birthdate)
        diff = abs(user_date - athlete_date)
        if user_date == athlete_date:
            return athlete.name, athlete.birthdate
        elif not near_date or near_date > diff:
            near_date = diff
            athlete_name = athlete.name
            athlete_birthdate = athlete.birthdate
    return athlete_name, athlete_birthdate

def nearest_height(user_height, session):
    all_date = session.query(Athletes).filter(Athletes.height).all()
    near_height = None
    for athlete in all_date:
        athlete_height = athlete.height
        diff = abs(user_height - athlete_height)
        if user_height == athlete.height:
            return athlete.name, athlete.height
        elif not near_height or near_height > diff:
            near_height = diff
            athlete_name = athlete.name
            athlete_height_near = athlete.height
    return athlete_name, athlete_height_near

def main():
    session = connect_db()
    user_data = query_user_id(session)
    if user_data:
        nearest_athlet = {}
        nearest_athlet["near_birthdate"] = nearest_date(user_data["birthdate"], 
            session)
        nearest_athlet["near_height"] = nearest_height(user_data["height"],
            session)
        print(f"Ближайший по возрасту спортсмен: {nearest_athlet['near_birthdate']}"
            f"\nБлижайший по росту спортсмен: {nearest_athlet['near_height']}")

if __name__ == "__main__":
    main()