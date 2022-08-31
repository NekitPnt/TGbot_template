import asyncio
import os

import peewee
import peewee_async
import playhouse.migrate
from loguru import logger

# -------------------------------------------- DB INIT --------------------------------------------
database = peewee_async.PooledPostgresqlDatabase(
    os.getenv("POSTGRES_DB", "tg_bot_template"),
    user=os.getenv("POSTGRES_USER", "tg_bot_template"),
    password=os.getenv("POSTGRES_PASSWORD", "tg_bot_template"),
    host=os.getenv("POSTGRES_HOST", "localhost")
)


# -------------------------------------------- MODELS --------------------------------------------
class Users(peewee.Model):
    id = peewee.PrimaryKeyField(null=False)
    social_id = peewee.BigIntegerField(null=False)
    username = peewee.CharField(max_length=50)
    registration_date = peewee.DateTimeField(null=True)

    class Meta:
        database = database


ALL_TABLES = [Users]
# -------------------------------------------- MIGRATIONS --------------------------------------------


def dev_drop_tables(db: peewee_async.PooledPostgresqlDatabase, tables: list):
    with db:
        db.drop_tables(tables, safe=True)
    logger.info("Tables dropped")


def create_tables(db: peewee_async.PooledPostgresqlDatabase, tables: list):
    with db:
        db.create_tables(tables, safe=True)
    logger.info("Tables created")


def make_migrations():
    migrator = playhouse.migrate.PostgresqlMigrator(database)
    try:
        with database.atomic():
            playhouse.migrate.migrate(
                # migrator.alter_column_type("users", "social_id", peewee.BigIntegerField(null=False)),
                # migrator.add_column("users", "channel_id", peewee.CharField(null=False, max_length=50))
            )
        logger.info("Tables migrated")
    except peewee.ProgrammingError:
        pass


# psql postgresql://tg_bot_template:tg_bot_template@localhost:5432/tg_bot_template
# dev_drop_tables(database, ALL_TABLES)
create_tables(database, ALL_TABLES)
make_migrations()
database.close()

# -------------------------------------------- ASYNC MANAGER --------------------------------------------
# Create async models manager:
conn = peewee_async.Manager(database)
database.set_allow_sync(False)

# run db connect
loop = asyncio.get_event_loop()
loop.run_until_complete(database.connect_async(loop=loop))
