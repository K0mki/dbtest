from tortoise import Tortoise, run_async, fields 
from tortoise.models import Model 

class PhoneType(Model):
    class Meta:
        table='lookup_phone_types'
    
    id = fields.UUIDField(pk=True)
    name = fields.CharField(8,unique= True)

    # phones: fields.ReverseRelation["PhoneNumber"]                   # mislim da nije bitno, jer ti ne treba funkcionalnost daj mi sve mobilne telefone 

    # phones1 : fields.ReverseRelation["SearchList"]                  # ?!?


class Contact(Model):
    class Meta:
        table='contacts'

    id = fields.UUIDField(pk=True)
    first_name = fields.TextField()
    last_name = fields.TextField()

    # phone_numbers: fields.ReverseRelation["PhoneNumber"]

    # async def mk_search(self):

    #     sl = await SearchList.filter(contact=self).get_or_none()
    #     if not sl:
    #         sl = SearchList(contact=self)

    #     pn = await self.fetch_related('phone_numbers')
    #     def normalize_pn(n):
    #         for x in ('-',' ','/','(',')','+'):
    #             n=n.replace(x, '')
    #         return n

    #     search = [x for x in [first_name, last_name] if x] + [normalize_pn(x.phone_number)+(' '+x.note) if x.note else '' for x in self.phone_numbers]
    #     search = ' '.join(search).lower()

    #     if sl.search != search:
    #         sl.search = search
    #         await sl.save()


class PhoneNumber(Model):
    class Meta:
        table='phone_numbers'

    id = fields.UUIDField(pk = True)
    phone_number = fields.TextField()
    is_primary = fields.BooleanField(null = True, unique = True)                              # TODO: Obezbedi da jedan kontakt moze da ima samo jedan primarni telefon
    note = fields.TextField(null=True)

    contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact")

    phone_type : fields.ForeignKeyRelation[PhoneType] = fields.ForeignKeyField("models.PhoneType")

    #number : fields.ReverseRelation["SearchList"]                   # ?
    #primary : fields.ReverseRelation["SearchList"]                  # ?
    #type : fields.ReverseRelation["SearchList"]                     # ?
    #note1 : fields.ReverseRelation["SearchList"]                    # ?

class SearchList(Model):
    class Meta:
        table='search_list'

    id = fields.IntField(pk=True)
    contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact", unique=True)

    search: fields.TextField(null=True) 
    
    #id : fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact", related_name="id1", pk = True)
    #first_name : fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact", related_name="first", )
    #last_name : fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact", related_name="last")
    #phone_number : fields.ForeignKeyRelation[PhoneNumber] = fields.ForeignKeyField("models.PhoneNumber",related_name="number")
    #is_primary : fields.ForeignKeyRelation[PhoneNumber] = fields.ForeignKeyField("models.PhoneNumber",related_name="primary")
    #note : fields.ForeignKeyRelation[PhoneNumber] = fields.ForeignKeyField("models.PhoneNumber",related_name="note1")
    #phone_type_id : fields.ForeignKeyRelation[PhoneType] = fields.ForeignKeyField("models.PhoneType",related_name="type")