from api.schemas import user_schema as user_m, material_schema as mat
from database.model import Users, session_maker, Materials, UsersProfileComp
from utils.logger import logger
from database.response import SuccessResponse, FailedResponse
import asyncio
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select


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
                await session.rollback()
                return FailedResponse(status_code=500, detail="Запись уже существует")
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return FailedResponse(status_code=500, detail="Произошла ошибка при выполнении")


class UserCompMethods:
    @classmethod
    async def update_comp_profile(cls, body: user_m.UpdateCompProfile):
        async with session_maker() as session:
            try:
                dumped_model = body.model_dump()
                user = UsersProfileComp(**dumped_model)
                session.add(user)
                await session.commit()

                return SuccessResponse(status_code=200, data=dumped_model)
            except IntegrityError as e:
                await session.rollback()
                return FailedResponse(status_code=500, detail="Студент с таким именем уже есть в Вашем списке.")
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return FailedResponse(status_code=500, detail="Произошла ошибка при выполнении")

    @classmethod
    async def get_profile(cls, telegram_id: int, student: str):
        async with session_maker() as session:
            try:
                query = select(UsersProfileComp.profile).where(UsersProfileComp.telegram_id == telegram_id).where(
                    UsersProfileComp.student == student)
                state = await session.execute(query)
                profile = state.scalar_one_or_none()
                if not profile:
                    return FailedResponse(status_code=404, detail="Студента с таким именем не существует.")

                return SuccessResponse(status_code=200, data=profile)
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return FailedResponse(status_code=500, detail="Произошла ошибка при выполнении")

    @classmethod
    async def get_students_names(cls, telegram_id: int):
        async with session_maker() as session:
            try:
                query = select(UsersProfileComp.student).where(UsersProfileComp.telegram_id == telegram_id)
                state = await session.execute(query)
                students = state.scalars().all()
                if not students:
                    return FailedResponse(status_code=404, detail="⚠️ У Вас пока что нет студентов.")

                return SuccessResponse(status_code=200, data=students)
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return FailedResponse(status_code=500, detail="⚠️ Произошла ошибка при выполнении")


class MaterialMethods:
    @classmethod
    async def add_material(cls, body: mat.AddMaterial):
        async with session_maker() as session:
            try:
                dumped_model = body.model_dump()
                user = Materials(**dumped_model)
                session.add(user)
                await session.commit()

                return SuccessResponse(status_code=200, data=dumped_model)
            except IntegrityError as e:
                await session.rollback()
                return FailedResponse(status_code=500,
                                      detail="⚠️ Материал с таким именем уже есть. Придумайте другое название.")
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return FailedResponse(status_code=500, detail="⚠️ Произошла ошибка при выполнении")

    @classmethod
    async def get_material(cls, telegram_id: int, material_name: str):
        async with session_maker() as session:
            try:
                query = select(Materials.material).where(Materials.telegram_id == telegram_id).where(
                    Materials.material_name == material_name)
                state = await session.execute(query)
                profile = state.scalar_one_or_none()
                if not profile:
                    return FailedResponse(status_code=404, detail="⚠️ Материала с таким именем не существует.")

                return SuccessResponse(status_code=200, data=profile)
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return FailedResponse(status_code=500, detail="Произошла ошибка при выполнении")

    @classmethod
    async def get_materials(cls, telegram_id: int):
        async with session_maker() as session:
            try:
                query = select(Materials.material_name).where(Materials.telegram_id == telegram_id)
                state = await session.execute(query)
                students = state.scalars().all()
                if not students:
                    return FailedResponse(status_code=404, detail="⚠️ У Вас не добавлено ни одного материала.")

                return SuccessResponse(status_code=200, data=students)
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return FailedResponse(status_code=500, detail="Произошла ошибка при выполнении")

# a = MaterialMethods()
# b = asyncio.run(a.get_materials(1045678578))
# print(vars(b))
