from fastapi import FastAPI
from database import model as dbs
import asyncio
app = FastAPI(title="Образоательная платформа")

async def create_tables():
    await dbs.Users.create_table()
    await dbs.UsersProfileComp.create_table()
    await dbs.Materials.create_table()
if __name__ == '__main__':
   asyncio.run(create_tables())