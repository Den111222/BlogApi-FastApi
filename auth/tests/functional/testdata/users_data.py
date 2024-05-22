from datetime import datetime

from passlib.handlers.pbkdf2 import pbkdf2_sha256

from models.db import User

users_data = [
    {
        "id": "f24fd632-b1a5-4273-a835-0119bd12f829",
        "login": "admin",
        "password": "admin_admin",
        "email": "admin@mail.com",
        "is_superuser": True,
        "is_deleted": False,
        "created_at": datetime.utcnow(),
    },
    {
        "id": "31cabbb5-6389-45c6-9b48-f7f173f6c40f",
        "login": "user01",
        "password": "user01_user01",
        "email": "user01@mail.com",
        "is_superuser": False,
        "is_deleted": False,
        "created_at": datetime.utcnow(),
    },
    {
        "id": "2f89e116-4827-4ff4-853c-b6e058f71e31",
        "login": "user02",
        "password": "user02_user02",
        "email": "user02@mail.com",
        "is_superuser": False,
        "is_deleted": False,
        "created_at": datetime.utcnow(),
    },
]
not_exist_users_data = [
    {
        "id": "f24fd632-b1a5-4273-a835-0119bd12f958",
        "login": "test_admin",
        "password": "test_test",
        "email": "test_admin@mail.com",
        "is_superuser": True,
        "is_deleted": False,
        "created_at": datetime.utcnow(),
    },
    {
        "id": "f24fd632-b1a5-4273-a835-0119bd12f958",
        "login": "test_not_admin",
        "password": "test_test",
        "email": "test_not_admin@mail.com",
        "is_superuser": False,
        "is_deleted": False,
        "created_at": datetime.utcnow(),
    },
]
invalid_users_data = [
    {
        "id": "",
        "login": 123,
        "password": "",
        "email": "asd#sdfg.com",
        "is_superuser": 10,
        "is_deleted": "false",
        "created_at": "",
    },
]


def get_user_data():
    for item in users_data:
        item2 = item.copy()
        item2["password"] = pbkdf2_sha256.hash(item["password"])
        yield User(**item2)
