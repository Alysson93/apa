from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from os import getenv
from dotenv import load_dotenv
from src.settings import Settings
from src.models.entities import table_registry
from sqlalchemy.pool import StaticPool

load_dotenv()

# engine = None
# if getenv('ENV') == 'test':
#     engine = create_async_engine(
#         "sqlite+aiosqlite:///:memory:",
#         connect_args={"check_same_thread": False},
#         poolclass=StaticPool,
#     )
# else:
engine = create_async_engine(Settings().DATABASE_URL)


async def get_session():
    # if getenv('ENV') == 'test':
    #     async with engine.begin() as conn:
    #         await conn.run_sync(table_registry.metadata.create_all)
    #     async with AsyncSession(engine, expire_on_commit=False) as session:
    #         yield session
    #     async with engine.begin() as conn:
    #         await conn.run_sync(table_registry.metadata.drop_all)
    # else:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
