import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER


def check_access(
    username: str,
    resource_name: str,
    resource_level: int,
    users: dict,
    blocked_users: set,
) -> str:
    if username not in users:
        return "DENY (User not found)"

    if username in blocked_users:
        return "DENY (User is blocked)"

    user_info = users[username]
    if not user_info.get("active", False):
        return "DENY (Account inactive)"

    if user_info.get("clearance", 0) >= resource_level:
        return "ALLOW"

    return "DENY (Insufficient clearance)"


def main() -> None:
    print(f"Студент: {STUDENT_NAME}, Група: {GROUP_NAME}, Варіант: {VARIANT_NUMBER}\n")

    users = {
        "forensic_lead": {
            "role": "forensic_analyst",
            "clearance": 4,
            "department": "Forensics",
            "active": True,
        },
        "compliance_off": {
            "role": "compliance_officer",
            "clearance": 3,
            "department": "Compliance",
            "active": True,
        },
        "trainee_sec": {
            "role": "trainee",
            "clearance": 1,
            "department": "Training",
            "active": True,
        },
        "vendor_tech": {
            "role": "vendor_support",
            "clearance": 2,
            "department": "Vendor",
            "active": True,
        },
        "archived_usr": {
            "role": "archived",
            "clearance": 1,
            "department": "Archive",
            "active": False,
        },
    }

    resources = [
        ("forensic_images", 4),
        ("compliance_reports", 3),
        ("training_videos", 1),
        ("vendor_tools", 2),
        ("evidence_locker", 4),
        ("certification_docs", 1),
        ("audit_findings", 3),
        ("chain_of_custody", 4),
        ("support_tickets", 2),
        ("learning_modules", 1),
    ]

    security_levels = ("Basic", "Standard", "Protected", "Maximum")
    blocked_users = {"archived_usr", "terminated_vendor", "security_breach"}

    print("Список ресурсів системи:")
    for res_name, res_level in resources:
        level_name = security_levels[res_level - 1]
        print(f"- {res_name}: {level_name}")

    print("\nРезультати перевірки доступу:")

    test_users = list(users.keys()) + ["unknown_user"]

    for username in test_users:
        for res_name, res_level in resources:
            result = check_access(username, res_name, res_level, users, blocked_users)
            print(f"user={username} resource={res_name} -> {result}")


if __name__ == "__main__":
    main()
