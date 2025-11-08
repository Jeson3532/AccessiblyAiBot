from api.schemas import user_schema as user_m
from database.model import Users, session_maker
from utils.logger import logger
from database.response import SuccessResponse, FailedResponse
import asyncio
from sqlalchemy.exc import IntegrityError

class UserMethods:
    @classmethod
    async def add_user(cls, body: user_m.AddUserModel):
        async with session_maker() as session:
            try:
                dumped_model = body.model_dump()
                user = Users(**dumped_model)
                session.add(user)
                await session.commit()

                return SuccessResponse(status_code=200, data=dumped_model)
            except IntegrityError as e:
                logger.error(e)
                await session.rollback()
                return FailedResponse(status_code=500, detail="Запись уже существует")
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return FailedResponse(status_code=500, detail="Произошла ошибка при выполнении")

a = user_m.AddUserModel(telegram_id=2)
b = UserMethods()
result = asyncio.run(b.add_user(a))
print(vars(result))
