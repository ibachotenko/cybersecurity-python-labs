import csv
import datetime
import hashlib
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER


class ValidationError(Exception):
    pass


def generate_hash(password: str, salt: str = "00000") -> str:
    if not password or not salt:
        raise ValueError()
    if len(password) < 16:
        raise ValidationError()

    data = (password + salt).encode("utf-8")
    return hashlib.sha3_256(data).hexdigest()


def create_user(username, password):
    salt = str(VARIANT_NUMBER).zfill(5)
    hash_value = generate_hash(password, salt)
    return (username, hash_value)


def create_users(users_list):
    os.makedirs("labs/lab01/data", exist_ok=True)
    filepath = "labs/lab01/data/users.csv"

    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for username, password in users_list:
            try:
                user_data = create_user(username, password)
                writer.writerow(user_data)
            except (ValueError, ValidationError):
                pass


def log_event(func):
    def wrapper(username: str, password: str, *args, **kwargs):
        result = False
        try:
            result = func(username, password, *args, **kwargs)
        except Exception:
            result = False
            raise
        finally:
            os.makedirs("labs/lab01/data", exist_ok=True)
            log_file = "labs/lab01/data/log.json"

            log_entry = {
                "event": "login",
                "user": username,
                "result": "success" if result else "failure",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "args": args,
                "kwargs": kwargs,
            }

            try:
                logs = []
                if os.path.exists(log_file):
                    with open(log_file, "r", encoding="utf-8") as f:
                        try:
                            logs = json.load(f)
                        except json.JSONDecodeError:
                            logs = []

                logs.append(log_entry)

                with open(log_file, "w", encoding="utf-8") as f:
                    json.dump(logs, f, indent=4)
            except (OSError, FileNotFoundError, PermissionError):
                pass

        return result

    return wrapper


@log_event
def login(username: str, password: str) -> bool:
    if not username or not password:
        raise ValueError()

    filepath = "labs/lab01/data/users.csv"
    users_db = []

    with open(filepath, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                users_db.append(tuple(row))

    salt = str(VARIANT_NUMBER).zfill(5)
    try:
        input_hash = generate_hash(password, salt)
    except (ValueError, ValidationError):
        return False

    for user, pwd_hash in users_db:
        if user == username and pwd_hash == input_hash:
            return True
    return False


def main() -> None:
    try:
        print(
            f"Студент: {STUDENT_NAME}, Група: {GROUP_NAME}, Варіант: {VARIANT_NUMBER}\n"
        )

        users_to_register = (
            ("admin", "SuperSecurePassword123!"),
            ("user1", "Short1!"),
            ("user2", "AnotherLongPassword456!"),
            ("guest", "GuestPass7890!@#$"),
            ("test", "TestAccountPassword123"),
            ("dev", "DeveloperPassword!2023"),
            ("qa", "QualityAssurancePass!"),
            ("manager", "ManagerSecurePass!@#"),
            ("ceo", "ChiefExecOfficerPass1!"),
            ("intern", "InternPassword12345!"),
        )

        create_users(users_to_register)

        filepath = "labs/lab01/data/users.csv"
        users_db = []
        with open(filepath, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    users_db.append(tuple(row))

        for u, h in users_db:
            print(f"{u:<15}  {h}")

        print("\nСпроба входу (admin):", login("admin", "SuperSecurePassword123!"))
        print("Спроба входу (wrong):", login("admin", "WrongPassword123!"))

    except (OSError, FileNotFoundError, PermissionError, ValidationError, ValueError):
        pass


if __name__ == "__main__":
    main()
