import inspect

import peewee
import peewee_async
import playhouse.migrate
from loguru import logger

from tg_bot_template.config import BotSettings
from tg_bot_template.db_infra import models

ALL_TABLES = [data for _, data in inspect.getmembers(models) if isinstance(data, peewee.ModelBase)]


def _dev_drop_tables(database: peewee_async.PooledPostgresqlDatabase, tables: list[peewee.ModelBase]) -> None:
    with database:
        database.drop_tables(tables, safe=True)
    logger.info("Tables dropped")


def _create_tables(database: peewee_async.PooledPostgresqlDatabase, tables: list[peewee.ModelBase]) -> None:
    with database:
        database.create_tables(tables, safe=True)
    logger.info("Tables created")


def _make_migrations(database: peewee_async.PooledPostgresqlDatabase) -> None:
    migrator = playhouse.migrate.PostgresqlMigrator(database)  # noqa: F841
    try:
        with database.atomic():
            playhouse.migrate.migrate(
                # migrator.add_column("users", "social_id", peewee.BigIntegerField(null=True)),  # noqa: ERA001
                # migrator.drop_not_null("users", "name"),  # noqa: ERA001
                # migrator.alter_column_type("users", "social_id", peewee.BigIntegerField(null=False)),  # noqa: ERA001
            )
        logger.info("Tables migrated")
    except peewee.ProgrammingError as e:
        logger.exception(f"Tables migrating error: {str(e)}")


def setup_db(settings: BotSettings) -> peewee_async.Manager:
    # psql postgresql://tg_bot_user:tg_bot_user@localhost:5432/tg_bot_user
    # ---------------- DB INIT ----------------
    database = peewee_async.PooledPostgresqlDatabase(
        settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
        host=settings.postgres_host,
    )
    database.bind(ALL_TABLES)

    # ---------------- MIGRATIONS ----------------
    # _dev_drop_tables(database, ALL_TABLES)  # noqa: ERA001
    _create_tables(database, ALL_TABLES)
    _make_migrations(database)

    database.close()
    database.set_allow_sync(False)

    return peewee_async.Manager(database)
