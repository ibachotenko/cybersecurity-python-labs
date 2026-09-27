import os
import random
import string
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER


def check_password_strength(
    password: str, all_passwords: list[str], criteria: dict, forbidden: set
) -> str:
    min_length = criteria["min_length"]

    if password in forbidden or len(password) < min_length:
        return "Заборонений"

    has_digit = any(c.isdigit() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_special = any(c in string.punctuation for c in password)

    criteria_count = sum([has_digit, has_upper, has_lower, has_special])

    if has_digit and has_upper and has_lower and has_special:
        if len(password) >= min_length + 4 and all_passwords.count(password) == 1:
            return "Дуже сильний"
        return "Сильний"

    if criteria_count > 1:
        return "Середній"

    return "Слабкий"


def main() -> None:
    print(f"Студент: {STUDENT_NAME}, Група: {GROUP_NAME}, Варіант: {VARIANT_NUMBER}\n")

    passwords = [
        "DataS3cur3!",
        "123",
        "Crypto@Analysis",
        "access",
        "Security@Pro",
        "password1",
        "Adv@nced123",
        "test123",
        "Quantum#2023",
        "guest123",
    ]
    criteria = {
        "min_length": 12,
        "require_digits": True,
        "require_upper": True,
        "require_special": True,
    }
    forbidden_passwords = {"123", "test123", "access", "password1", "guest123", "admin"}

    duplicates = [passwords[i] for i in random.sample(range(len(passwords)), 3)]
    passwords.extend(duplicates)

    for pwd in passwords:
        status = check_password_strength(pwd, passwords, criteria, forbidden_passwords)
        print(f"{pwd:<20}  {status}")


if __name__ == "__main__":
    main()
