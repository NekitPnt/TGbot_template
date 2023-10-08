import peewee
import peewee_async
import playhouse.migrate
from loguru import logger

from tg_bot_template.config import settings

# -------------------------------------------- DB INIT --------------------------------------------
database = peewee_async.PooledPostgresqlDatabase(
    settings.postgres_db,
    user=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.postgres_host,
)
conn = peewee_async.Manager(database)


# -------------------------------------------- MODELS --------------------------------------------
class BaseModel(peewee.Model):
    class Meta:
        database = database


class Users(BaseModel):
    id = peewee.PrimaryKeyField(null=False)
    social_id = peewee.BigIntegerField(null=False)
    username = peewee.CharField(max_length=50)
    registration_date = peewee.DateTimeField(null=True)
    taps = peewee.BigIntegerField(default=0)
    name = peewee.TextField(null=True)
    info = peewee.TextField(null=True)
    photo = peewee.TextField(null=True)


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


def setup_db():
    # psql postgresql://tg_bot_user:tg_bot_user@localhost:5432/tg_bot_user
    # dev_drop_tables(database, ALL_TABLES)
    create_tables(database, ALL_TABLES)
    make_migrations()
    database.close()
    database.set_allow_sync(False)
