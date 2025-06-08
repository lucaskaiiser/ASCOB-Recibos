from peewee import Model,CharField, DateField, FloatField, IntegerField
from src.models import db
from datetime import datetime, timedelta

class Receipt(Model):

    client_name = CharField()
    address = CharField()
    date = DateField(default=datetime.now().date())
    value = FloatField()
    debtor = CharField()
    #por_extenso = CharField()
    #bill_number = CharField()
    #bill_due_date = DateField()
    #installment_number = IntegerField()
    #installment_due_date = DateField()
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
    def populate_receipts():
        example_data = [
            {
                "client_name": "João Silva",
                "address": "Rua das Flores, 123",
                "date": datetime.now().date() - timedelta(days=10),
                "value": 250.75,
                "debtor": "Empresa XYZ",
                "payment_date": datetime.now().date() - timedelta(days=5),
                "description": "Pagamento referente ao serviço A.",
                "cobrador": "Carlos"
            },
            {
                "client_name": "Maria Oliveira",
                "address": "Av. Brasil, 456",
                "date": datetime.now().date() - timedelta(days=20),
                "value": 1000.00,
                "debtor": "Empresa ABC",
                "payment_date": datetime.now().date() - timedelta(days=18),
                "description": "Pagamento parcial da fatura 456.",
                "cobrador": "Ana"
            },
            {
                "client_name": "Pedro Santos",
                "address": "Praça Central, 789",
                "date": datetime.now().date(),
                "value": 500.50,
                "debtor": "Fulano Ltda",
                "payment_date": datetime.now().date(),
                "description": None,
                "cobrador": "Lucas"
            },
        ]

        for receipt in example_data:
            Receipt.create(**receipt)
        print("Dados inseridos com sucesso!")
    populate_receipts()