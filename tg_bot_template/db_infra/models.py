import peewee


class Users(peewee.Model):  # type: ignore[misc]
    id = peewee.PrimaryKeyField(null=False)
    social_id = peewee.BigIntegerField(null=False)
    username = peewee.CharField(max_length=50)
    registration_date = peewee.DateTimeField(null=True)
    taps = peewee.BigIntegerField(default=0)
    name = peewee.TextField(null=True)
    info = peewee.TextField(null=True)
    photo = peewee.TextField(null=True)
