from tortoise import run_async

from db import init
from models import User


async def new_user(username, age):
    user = User(username=username, age=age)
    await user.save()


async def delete_user(username):
    await User.filter(username=username).delete()


async def update_user(username, new_username):
    await User.filter(username=username).update(username=new_username)


async def search(username):
    # search_list = [(x.username, x.age) for x in await User.filter().all()]
    # return search_list
    user = await User.filter(username=username).first()
    return await user


async def run():

    await init()
    # await new_user("mika", 25)
    # await new_user("zika", 25)
    # await delete_user('zika')
    # await update_user("mika", "mikica")
    x = await search("mikica")
    print(x.age)


if __name__ == '__main__':

    run_async(run())
