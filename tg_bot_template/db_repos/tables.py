import sqlalchemy
from sqlalchemy import MetaData

metadata = MetaData()

users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("social_id", sqlalchemy.BigInteger, nullable=False),
    sqlalchemy.Column("username", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("registration_date", sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column("taps", sqlalchemy.BigInteger, default=0),
    sqlalchemy.Column("name", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("info", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("photo", sqlalchemy.Text, nullable=True),
)
