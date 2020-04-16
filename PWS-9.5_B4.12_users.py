import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

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
    
def request_data():
    print("Регистрация пользователя:\n")
    fn = input("Введите имя: ")
    ln = input("Введите фамилию: ")
    gender = valid_gender()
    while not gender:
        print("Ошибка ввода, попробуйте ещё раз!")
        gender = valid_gender()
    email = input("Введите E-mail: ")
    while not valid_email(email):
        email = input("Введенный E-mail не корректен, повторите попытку: ")
    birthdate = valid_birthdate()
    while not birthdate:
        print("Ошибка ввода, попробуйте ещё раз!")
        birthdate = valid_birthdate()
    height = valid_height()
    while not height:
        print("Ошибка ввода, попробуйте ещё раз!")
        height = valid_height()
    user = Users(first_name = fn, last_name = ln, gender = gender,
        email = email, birthdate = birthdate, height = height)
    return user
    
def valid_gender():
    gender = input("Ваш пол: 1 - Male    2 - Female: ")
    if gender == "1":
        return "Male"
    elif gender == "2":
        return "Female"

def valid_email(email):
    email_list = list(email)
    if email_list.count("@") == 1:
        return "." in email_list[email_list.index("@") :]

def valid_birthdate():
    birthdate = input("Дата рождения в формате YYYY-MM-DD: ")
    birthdate_list = birthdate.split("-")
    if len(birthdate_list) == 3:
        if (len(birthdate_list[0]) == 4) and (len(birthdate_list[1]) == 2) and (
                len(birthdate_list[2]) == 2):
            return birthdate

def valid_height():
    height = float(input("Ваш рост: "))
    if height > 3:
        height /= 100
    return height

def main():
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print("Пользователь добавлен")

if __name__ == "__main__":
    main()