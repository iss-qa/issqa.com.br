import argparse
import os
import sys

from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from db import get_db, init_db


def main():
    parser = argparse.ArgumentParser(description="Cria usuário admin no MongoDB.")
    parser.add_argument("--username", required=True, help="Usuário ou e-mail")
    parser.add_argument("--password", required=True, help="Senha do usuário")
    args = parser.parse_args()

    init_db()
    db = get_db()
    db.users.update_one(
        {"username": args.username},
        {"$set": {"username": args.username, "password_hash": generate_password_hash(args.password)}},
        upsert=True,
    )
    print(f"Usuário criado/atualizado: {args.username}")


if __name__ == "__main__":
    main()
