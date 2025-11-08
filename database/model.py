from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import TEXT, ARRAY, String, TypeDecorator
import json
from database.config import DBConfig
from dotenv import load_dotenv
from utils.logger import logger
load_dotenv()

# Объект класса с конфигурацией
db_config = DBConfig()

# Данные для подключения
user = db_config.USER
password = db_config.PASSWORD
host = db_config.HOST
port = db_config.PORT
dbname = db_config.DBNAME

engine = create_async_engine(f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}", pool_pre_ping=True)
session_maker = async_sessionmaker(bind=engine, autoflush=False)


class JSON(TypeDecorator):
    cache_ok = True
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value, ensure_ascii=False)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)


class Base(DeclarativeBase):
    ...


class Users(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(unique=True, nullable=True)
    role: Mapped[str] = mapped_column(comment="Роль участника в системе")

    @classmethod
    async def create_table(cls):
        async with engine.begin() as connect:
            logger.info(f"Создаю базу данных {cls.__tablename__}...")
            await connect.run_sync(
                lambda sync_conn: cls.metadata.drop_all(sync_conn, tables=[cls.__table__])
            )
            await connect.run_sync(
                lambda sync_conn: cls.metadata.create_all(sync_conn, tables=[cls.__table__])
            )
            logger.info("База данных создана!")
