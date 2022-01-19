import datetime

import aiohttp
import asyncio

from sqlalchemy import select

from database import async_db_session
from models import User, Dashboard

start_date = datetime.date(2005, 3, 2)
end_date = datetime.date(2005, 3, 3)
_delta = datetime.timedelta(days=1)


async def init_app():
    await async_db_session.init()
    await async_db_session.create_all()


async def main():
    print('Start init')
    await init_app()
    print('End init')
    await User.create(full_name='default')
    default_user = await User.get(1)
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
                    query = select(Dashboard).where(Dashboard.r030 == el['r030']).where(Dashboard.exchangedate == el['exchangedate'])
                    res = await async_db_session.execute(query)
                    res_set = res.fetchall()
                    if len(res_set) >= 1:
                        print('In DB now')
                    else:
                        await Dashboard.create(user_id=default_user.id,
                                               r030=el['r030'],
                                               name=el['txt'],
                                               rate=el['rate'],
                                               shortname=el['cc'],
                                               exchangedate=el['exchangedate'])


asyncio.run(main())
