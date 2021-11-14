from peewee import Model, BigIntegerField, DoubleField, BlobField, BooleanField, SqliteDatabase

from config.variables import database_file

db = SqliteDatabase(database_file)


class World(Model):
    seed = BigIntegerField(primary_key=True)
    user_rating = DoubleField(null=True)
    biome_data = BlobField(null=True)
    image = BlobField(null=True)
    saved = BooleanField(default=False)
    
    class Meta:
        database = db


def initialize_db():
    db.connect()
    db.create_tables([World], safe=True)
    db.close()


initialize_db()
print('database initialization Done')
