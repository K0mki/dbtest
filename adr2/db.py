from tortoise import Tortoise, run_async


async def init():

    await Tortoise.init(
        db_url='postgres://aca:123@localhost/test',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()

# run_async is a helper function to run simple async Tortoise scripts.
if __name__ == '__main__':
    run_async(init())
