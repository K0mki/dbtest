"""
This example shows how relations between models especially unique field work.

Key points in this example are use of ForeignKeyField and OneToOneField has to_field.
For other basic parts, it is the same as relation exmaple.
"""
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from tortoise.query_utils import Prefetch

class School(Model):
    class Meta:
        table='schools'

    id = fields.UUIDField(pk=True)
    name = fields.TextField()

    students: fields.ReverseRelation["Student"]

class Student(Model):
    class Meta:
        table='students'

    id = fields.UUIDField(pk=True)
    name = fields.TextField()
    school: fields.ForeignKeyRelation[School] = fields.ForeignKeyField("models.School", related_name="students", on_delete=fields.CASCADE)


async def run():
    await Tortoise.init(db_url="sqlite://skole.db", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    os_branko_radicevic = School(name="Branko Radicevic")
    await os_branko_radicevic.save()
    os_vuk_karadzic = School(name="Vuk Karadzic")
    await os_vuk_karadzic.save()
    
    igor = Student(name="Igor Jeremic", school=os_branko_radicevic)
    aca = Student(name="Aleksadnar Stankovic", school=os_branko_radicevic)
    stefan = Student(name="Stefan Kotarac", school=os_vuk_karadzic)
    await igor.save()
    await aca.save()
    await stefan.save()

async def run2():
    await Tortoise.init(db_url="sqlite://skole.db", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    os_branko_radicevic = await School.filter(name='Branko Radicevic').prefetch_related('students').get_or_none()

    if os_branko_radicevic:
        print("POSTOJI SKOLA",os_branko_radicevic.name)
    
        print('ucenici iz te skole su')

        # await os_branko_radicevic.fetch_related('students')

        for s in os_branko_radicevic.students:
            print(s,s.id,s.name)
        
    
    

if __name__ == "__main__":
    run_async(run())