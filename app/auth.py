"""
app/auth.py
Handles:
  - Password hashing
  - Signup
  - Login verification
"""

import bcrypt
from app.db import create_user, get_user_by_email


def hash_password(plain_password: str) -> str:
    """Converts plain password to bcrypt hash."""
    salt   = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if plain password matches the stored hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def signup(name: str, email: str, password: str, role: str = "agent"):
    """
    Creates a new user.
    Returns user object or error message.
    """
    # Check if email already exists
    existing = get_user_by_email(email)
    if existing:
        return None, "Email already registered"

    # Validate role
    if role not in ["admin", "agent"]:
        return None, "Role must be admin or agent"

    # Hash password and create user
    hashed   = hash_password(password)
    user     = create_user(name, email, hashed, role)
    return user, None


def login(email: str, password: str):
    """
    Verifies login credentials.
    Returns user object or error message.
    """
    user = get_user_by_email(email)

    if not user:
        return None, "Email not found"

    if not verify_password(password, user.password):
        return None, "Incorrect password"

    return user, None


# ── Create default admin account ──────────────────────────────────────
def create_default_admin():
    """
    Creates a default admin account if none exists.
    Used on first run.
    """
    existing = get_user_by_email("admin@complaints.com")
    if not existing:
        user, error = signup(
            name     = "Admin",
            email    = "admin@complaints.com",
            password = "admin123",
            role     = "admin"
        )
        if user:
            print("✅ Default admin created")
            print("   Email:    admin@complaints.com")
            print("   Password: admin123")
    else:
        print("✅ Admin account exists")


