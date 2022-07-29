import sqlalchemy as sq

# from datetime import date, time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

#создаем базовый класс
Base = declarative_base()

db = 'postgresql://user:1@localhost:5432/diploma'
engine = sq.create_engine(db)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    vk_id = sq.Column(sq.Integer, nullable=False, unique=True)
    age = sq.Column(sq.Integer, nullable=False)
    sex = sq.Column(sq.String, nullable=False)
    city = sq.Column(sq.String, nullable=False)
    martial_status = sq.Column(sq.String, nullable=False)

    couples = relationship('Couple', secondary='user_couple', back_populates='users')

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id


class Couple(Base):
    __tablename__ = 'couple'

    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    vk_id = sq.Column(sq.Integer, nullable=False, unique=True)
    age = sq.Column(sq.Integer, nullable=False)
    sex = sq.Column(sq.String, nullable=False)
    city = sq.Column(sq.String, nullable=False)
    martial_status = sq.Column(sq.String, nullable=False)

    users = relationship(User, secondary='user_couple', backref='user')

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

# Создаем таблицу для осуществления связи многие-ко-многим
user_couple = sq.Table(
    'user_couple',
    Base.metadata,
    sq.Column('user_id', sq.Integer, sq.ForeignKey('user.id'), nullable=False),
    sq.Column('couple_id', sq.Integer, sq.ForeignKey('couple.id'), nullable=False)
)

if __name__ == '__main__':

    with Session() as session:
        # Init scheme
        Base.metadata.create_all(engine)

        # Add data
        user1 = User(
            vk_id='1234569568',
            age=30,
            sex='female',
            city='Moscow',
            martial_status='search',
        )
        couple_1 = Couple(
            vk_id='987654658',
            age=30,
            sex='male',
            city='Moscow',
            martial_status='search',
        )
        session.add(user1)
        session.add(couple_1)
        session.commit()