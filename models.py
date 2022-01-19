from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from database import Base, async_db_session


class ModelManager:
    @classmethod
    async def create(cls, **kwargs):
        async_db_session.add(cls(**kwargs))
        await async_db_session.commit()

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
                .where(cls.id == id)
                .values(**kwargs)
                .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, id: int):
        query = select(cls).where(cls.id == id)
        results = await async_db_session.execute(query)
        (result,) = results.one()
        return result



class User(Base, ModelManager):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)
    dashboards = relationship("Dashboard")

    def __repr__(self):
        return f'{self.__class__.name}(id={self.id}, full_name={self.full_name})'


class Dashboard(Base, ModelManager):
    __tablename__ = "dashboards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"))
    r030 = Column(Integer, unique=True)
    name = Column(String)
    rate = Column(Float)
    shortname = Column(String)
    exchangedate = Column(String)

    def __repr__(self):
        return f'{self.__class__.name}(id={self.id}, shortname={self.shortname}, rate={self.rate}'


PydanticUser = sqlalchemy_to_pydantic(User)
PydanticDashboard = sqlalchemy_to_pydantic(Dashboard)
