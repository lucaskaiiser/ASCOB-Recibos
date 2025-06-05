from peewee import Model,CharField, DateField, FloatField, IntegerField
from src.models import db
from datetime import datetime

class Receipt(Model):

    client_name = CharField()
    address = CharField()
    date = DateField(default=datetime.now().date())
    value = FloatField()
    debtor = CharField()
    por_extenso = CharField()
    bill_number = CharField()
    bill_due_date = DateField()
    installment_number = IntegerField()
    installment_due_date = DateField()
    payment_date = DateField()
    description = CharField(null=True) 
    cobrador = CharField()

    class Meta:
        database = db

    @classmethod
    def edit_receipt(cls, receipt_id, **kwargs):
        return cls.update(**kwargs).where(cls.id == receipt_id).execute()

    @classmethod
    def delete_receipt(cls, receipt_id):
        return cls.delete().where(cls.id == receipt_id).execute()
    

if __name__ == '__main__':
    from datetime import datetime
    db.create_tables([Receipt])
    test = Receipt(
        date=datetime.now().date(),
        value=1000,
        client_name='LJGUERRA',
        debtor='AAAAA',
        address='Rua Exemplo, 123',
        por_extenso='Mil reais',
        bill_number='123456789',
        bill_due_date=datetime(2025, 6, 30).date(),
        installment_number=1,
        installment_due_date=datetime(2025, 7, 30).date(),
        payment_date=datetime.now().date(),  # ou uma data se já foi pago
        description='Pagamento referente ao serviço X',
        cobrador='João Silva'
    )
    test.save()
