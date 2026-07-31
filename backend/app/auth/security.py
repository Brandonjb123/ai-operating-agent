"""
Utilitas keamanan untuk penanganan password.
Menggunakan bcrypt lewat passlib untuk hashing dan verifikasi yang aman.
"""

from passlib.context import CryptContext

# Buat CryptContext dengan bcrypt sebagai satu-satunya skema.
# "deprecated": "auto" akan otomatis menangani algoritma usang
# jika di masa depan perlu dilakukan upgrade.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Meng-hash password teks biasa menggunakan bcrypt.

    Args:
        password (str): Password teks biasa yang akan di-hash.

    Returns:
        str: Hash bcrypt yang dihasilkan.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Memverifikasi password teks biasa terhadap hash bcrypt.

    Args:
        plain_password (str): Password teks biasa yang akan dicek.
        hashed_password (str): Hash bcrypt yang akan diverifikasi.

    Returns:
        bool: True jika password cocok, False jika tidak.
    """
    return pwd_context.verify(plain_password, hashed_password)

if __name__ == "__main__":
    # Contoh penggunaan (jangan hardcode di produksi)
    test_password = "admin123"

    hashed = hash_password(test_password)
    print(f"Password ter-hash: {hashed}")

    is_valid = verify_password(test_password, hashed)
    print(f"Hasil verifikasi: {is_valid}")