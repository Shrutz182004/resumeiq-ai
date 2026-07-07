from app.core.security import hash_password, verify_password

password = "MyPassword123"

hashed = hash_password(password)

print("Original Password:", password)
print("Hashed Password:", hashed)

print("Correct Password:", verify_password("MyPassword123", hashed))
print("Wrong Password:", verify_password("WrongPassword", hashed))