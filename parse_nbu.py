import datetime

import aiohttp
import asyncio

from sqlalchemy import select

from database import async_db_session
from models import User, Dashboard

start_date = datetime.date(2001, 3, 2)
end_date = datetime.date(2001, 3, 2)
_delta = datetime.timedelta(days=1)


async def init_app():
    await async_db_session.init()
    await async_db_session.create_all()
    default_user = User(full_name='default')
    async_db_session.add(default_user)
    await async_db_session.flush()


async def main():
    print('Start init')
    await init_app()
    print('End init')
    users_query = await async_db_session.execute(select(User).where(User.id == 1))
    (default_user,) = users_query.one()
    await parsing_date(start_date, end_date, default_user)


async def parsing_date(start_date, end_date, default_user):
    async with aiohttp.ClientSession() as session:
        while start_date <= end_date:
            print(str(start_date) + '-------------')
            nbu_url = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={str(start_date).replace("-", "")}&json'
            start_date += _delta
            async with session.get(nbu_url) as resp:
                data = await resp.json()
                for el in data:
                    new_dashboard = async_db_session.add(Dashboard(user_id=default_user.id,
                                              r030=el['r030'],
                                              name=el['txt'],
                                              rate=el['rate'],
                                              shortname=el['cc'],
                                              exchangedate=el['exchangedate']))

                    await async_db_session.commit()


asyncio.run(main())
