import hashlib
import uuid
from datetime import datetime


# ─────────────────────────────────────────────
#  In-memory user store
# ─────────────────────────────────────────────

def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


_users: dict[str, dict] = {}


def _seed():
    """Создать дефолтного admin при первом импорте."""
    admin_id = "usr_admin"
    _users[admin_id] = {
        "user_id": admin_id,
        "username": "admin",
        "email": "admin@omnify.store",
        "password_hash": _hash("admin123"),
        "is_admin": True,
        "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }


_seed()


# ─── Public API ──────────────────────────────

def register_user(username: str, email: str, password: str) -> tuple[dict | None, str]:
    """Регистрация. Возвращает (user, '') или (None, error_message)."""
    username = username.strip()
    email = email.strip().lower()

    if len(username) < 3:
        return None, "Имя пользователя должно быть не менее 3 символов"
    if len(password) < 6:
        return None, "Пароль должен быть не менее 6 символов"

    for u in _users.values():
        if u["username"].lower() == username.lower():
            return None, "Пользователь с таким именем уже существует"
        if u["email"] == email:
            return None, "Email уже используется"

    user_id = "usr_" + str(uuid.uuid4())[:8]
    user = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "password_hash": _hash(password),
        "is_admin": False,
        "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }
    _users[user_id] = user
    return user, ""


def login_user(username: str, password: str) -> tuple[dict | None, str]:
    """Логин по имени или email. Возвращает (user, '') или (None, error)."""
    username = username.strip()
    pw_hash = _hash(password)
    for u in _users.values():
        if (u["username"].lower() == username.lower() or u["email"] == username.lower()):
            if u["password_hash"] == pw_hash:
                return u, ""
    return None, "Неверное имя пользователя или пароль"


def get_user(user_id: str) -> dict | None:
    return _users.get(user_id)


def get_all_users() -> list[dict]:
    return [
        {k: v for k, v in u.items() if k != "password_hash"}
        for u in _users.values()
    ]


def set_admin(user_id: str, is_admin: bool) -> bool:
    if user_id in _users:
        _users[user_id]["is_admin"] = is_admin
        return True
    return False


def delete_user(user_id: str) -> bool:
    if user_id in _users and _users[user_id]["username"] != "admin":
        del _users[user_id]
        return True
    return False
