import json
import os
from datetime import datetime

from bson import ObjectId

from db import get_db, init_db


def serialize(doc):
    if isinstance(doc, ObjectId):
        return str(doc)
    return doc


def export_collection(db, name):
    return list(db[name].find())


def main():
    init_db()
    db = get_db()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(os.getcwd(), "backups", timestamp)
    os.makedirs(out_dir, exist_ok=True)

    collections = [
        "users",
        "settings",
        "about",
        "skills",
        "experiences",
        "projects",
        "messages",
    ]

    for name in collections:
        data = export_collection(db, name)
        path = os.path.join(out_dir, f"{name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, default=serialize, indent=2)

    print(f"Backup exportado em: {out_dir}")


if __name__ == "__main__":
    main()
