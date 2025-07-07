from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import Integer, String, text, DateTime, func, delete, select, asc, desc
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import pandas as pd
import os

from data_fetching import first_fetch, fetch_data

load_dotenv()

db_url = getenv('DB_URL')

if not db_url:
    DATABASE_URL = (
        f"postgresql+asyncpg://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}"
        f"@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}"
    )
else:
    DATABASE_URL = db_url[:10] + "+asyncpg" + db_url[11:]

CODES = [
    '37.05.01',
    '38.03.02',
    '38.03.01',
    '05.03.06'
]

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    regnum: Mapped[int] = mapped_column(Integer)
    speciality: Mapped[str] = mapped_column(String(100))
    compensation: Mapped[str] = mapped_column(String(100))
    priority: Mapped[int] = mapped_column(Integer)
    marks: Mapped[str] = mapped_column(String(100))
    total_mark: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def print_tables():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public';"))
        tables = result.fetchall()
        print(tables)

async def create(session: AsyncSession, **kwargs):
    user = User(**kwargs)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def delete_all(session: AsyncSession):
    await session.execute(delete(User))
    await session.commit()

async def get(session: AsyncSession, id: int):
    match id:
        case 1:
            stmt = select(User).where(User.speciality == "37.05.01 Клиническая психология")
        case 2:
            stmt = select(User).where(User.speciality == "38.03.02 Менеджмент")
        case 3:
            stmt = select(User).where(User.speciality == "38.03.01 Экономика")
        case 4:
            stmt = select(User).where(User.speciality == "05.03.06 Экология и природопользование")
        case _:
            stmt = "Программа не найдена"
    
    if stmt != "Программа не найдена":
        stmt = stmt.order_by(asc(User.priority), desc(User.total_mark))
        result = await session.execute(stmt)
        return result.scalars().all()
    else:
        return "Программа не найдена"

async def get_date(session: AsyncSession):
    result = await session.execute(select(User.date).order_by(User.id.asc()).limit(1))
    date = result.scalar_one_or_none()
    return date

async def load_all_data(session: AsyncSession):
    await init_db()

    first_fetch_result = await first_fetch()

    if first_fetch_result != "Error":
        count = first_fetch_result["count"]

        items = first_fetch_result["items"]

        async with SessionLocal() as session:
            await delete_all(session)

            for i in range(100):
                huesos = items[i]

                subjects = huesos["applications"]

                for subject in subjects:
                    if subject["speciality"].split()[0] in CODES:
                        marks = subject["marks"]

                        str_marks = ''

                        for key, mark in marks.items():
                            str_marks += f'{key} {mark["mark"]}'

                        await create(
                            session,
                            regnum=huesos["regnum"],
                            speciality=subject["speciality"],
                            compensation=subject["compensation"],
                            priority=subject["priority"],
                            marks=str_marks,
                            total_mark=subject["total_mark"]
                        )
            
            count -= 100
            page = 1
            while count > 0:
                if count < 100:
                    items = await fetch_data(page, count)
                    count -= count
                else:
                    items = await fetch_data(page, 100)
                    count -= 100
                page += 1

                for huesos in items:
                    if not isinstance(huesos, dict):
                        print(f"⚠ Unexpected entry: {huesos}")
                        continue

                    subjects = huesos.get("applications", [])
                
                    for subject in subjects:
                        if subject["speciality"].split()[0] in CODES:
                            marks = subject["marks"]
                            str_marks = ''
                
                            for key, mark in marks.items():
                                str_marks += f'{key} {mark["mark"]} '
                
                            await create(
                                session,
                                regnum=huesos["regnum"],
                                speciality=subject["speciality"],
                                compensation=subject["compensation"],
                                priority=subject["priority"],
                                marks=str_marks,
                                total_mark=subject["total_mark"]
                            )


    else:
        return "Error"
    

async def need_db_update():
    async with SessionLocal() as session:
        try:
            latest_date = await get_date(session)
            tz = timezone(timedelta(hours=5))
    
            latest_date = latest_date.replace(tzinfo=timezone.utc).astimezone(tz) # type: ignore
    
            current_date = datetime.now()
    
            print(latest_date)
            print(current_date)
    
            if latest_date.day - current_date.day != 0 or latest_date.hour - current_date.hour != 0: # type: ignore
                return True
            else:
                return False
        except Exception as e:
            return True
        
async def save_to_xlsx(id: int):
    async with SessionLocal() as session:
        result = await get(session, id)

        if not os.path.exists('temp'):
            os.mkdir('temp')

        file_path = rf"temp/{CODES[id - 1]}.xlsx"

        data = [{
            "Регистрационный номер": user.regnum,
            "Направление": user.speciality,
            "Основа": user.compensation,
            "Приоритет": user.priority,
            "Оценки": user.marks,
            "Итоговая оценка": user.total_mark
        } for user in result]

        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False, engine='openpyxl')

        return file_path