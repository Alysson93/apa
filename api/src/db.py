from os import getenv

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.settings import Settings

load_dotenv()

engine = create_async_engine(Settings().DATABASE_URL)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


# user 1264167b-088c-42a8-86c0-c5db94fa18e3
# string 0d0a04f7-ae31-43b5-8db4-613fc8da8cdb
