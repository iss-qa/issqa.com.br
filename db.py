import os
from datetime import datetime
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING
import certifi
ca = certifi.where()

load_dotenv()

from urllib.parse import quote_plus, unquote

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "portfolio_cv")

# Robusto para Vercel: Garante que caracteres especiais (@, :, etc) na senha sejam codificados apenas uma vez
if "://" in MONGO_URI and "@" in MONGO_URI:
    try:
        protocol, rest = MONGO_URI.split("://", 1)
        creds, cluster = rest.rsplit("@", 1)
        if ":" in creds:
            user, password = creds.split(":", 1)
            # Unquote seguido de quote_plus resolve tanto senhas cruas quanto já codificadas (evita double-encoding)
            safe_user = quote_plus(unquote(user))
            safe_password = quote_plus(unquote(password))
            MONGO_URI = f"{protocol}://{safe_user}:{safe_password}@{cluster}"
    except Exception as e:
        print(f"Erro ao tratar MONGO_URI: {e}")

_client = MongoClient(MONGO_URI, tlsCAFile=ca, serverSelectionTimeoutMS=5000)
_db = _client[MONGO_DB]


def get_db():
    return _db


def init_db():
    _db.settings.create_index([("key", ASCENDING)], unique=True)
    _db.users.create_index([("username", ASCENDING)], unique=True)


def seed_settings(defaults):
    for key, value in defaults.items():
        _db.settings.update_one(
            {"key": key},
            {"$setOnInsert": {"key": key, "value": value}},
            upsert=True,
        )


def seed_about(default_text):
    if _db.about.count_documents({}) == 0:
        _db.about.insert_one({"content": default_text, "created_at": datetime.utcnow()})


def seed_admin(username, password_hash):
    if _db.users.count_documents({"username": username}) == 0:
        _db.users.insert_one(
            {
                "username": username,
                "password_hash": password_hash,
                "created_at": datetime.utcnow(),
            }
        )


def get_setting(key, default=""):
    doc = _db.settings.find_one({"key": key})
    return doc["value"] if doc else default


def set_setting(key, value):
    _db.settings.update_one(
        {"key": key},
        {"$set": {"key": key, "value": value}},
        upsert=True,
    )
