from peewee import SqliteDatabase

db = SqliteDatabase('db.sqlite')

def start_database_connection():
    from src.models import Receipt
    db.create_tables([Receipt])
    
