from peewee import Model,CharField, DateField, FloatField
from src.models import db

class Receipt(Model):
    date = DateField()
    value = FloatField()
    client = CharField()
    debtor = CharField()

    class Meta:
        database = db

    @classmethod
    def edit_receipt(cls, receipt_id, **kwargs):
        return cls.update(**kwargs).where(cls.id == receipt_id).execute()

    @classmethod
    def delete_receipt(cls, receipt_id):
        return cls.delete().where(cls.id == receipt_id).execute()
        


