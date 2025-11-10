from bot.handlers.message import router as message_router
from bot.handlers.callback import router as callback_router
from bot.handlers.fsm import router as fsm_router
from aiogram import Router

routers = []
for key, val in list(globals().items()):
    filter_key = "_router" in key
    second_val = type(val) is Router

    if filter_key and second_val:
        routers.append(val)
if __name__ == '__main__':
    print(routers)
