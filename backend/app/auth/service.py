"""
Authentication Service Layer.
Berisi business logic untuk registrasi dan login.
Saat ini berupa skeleton dengan TODO untuk implementasi selanjutnya.
"""

from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse


class AuthService:
    """
    Service class untuk menangani logika autentikasi.
    Belum mengakses database atau repository.
    """

    def register_user(self, request: UserRegisterRequest) -> TokenResponse:
        """
        Mendaftarkan pengguna baru.

        Args:
            request (UserRegisterRequest): Data pendaftaran (full_name, email, password).

        Returns:
            TokenResponse: Token akses setelah registrasi berhasil.
        """
        # TODO:
        # 1. Validasi email uniqueness (panggil repository)
        # 2. Hash password menggunakan hash_password() dari security.py
        # 3. Simpan user ke database (via repository)
        # 4. Buat JWT access token menggunakan create_access_token() dari jwt.py
        # 5. Kembalikan TokenResponse
        raise NotImplementedError("register_user belum diimplementasikan")

    def login_user(self, request: UserLoginRequest) -> TokenResponse:
        """
        Melakukan autentikasi pengguna.

        Args:
            request (UserLoginRequest): Data login (email, password).

        Returns:
            TokenResponse: Token akses setelah login berhasil.
        """
        # TODO:
        # 1. Cari user berdasarkan email (via repository)
        # 2. Jika tidak ditemukan, raise AuthenticationException
        # 3. Verifikasi password menggunakan verify_password() dari security.py
        # 4. Jika password salah, raise AuthenticationException
        # 5. Buat JWT access token menggunakan create_access_token() dengan payload {"sub": user.email}
        # 6. Kembalikan TokenResponse
        raise NotImplementedError("login_user belum diimplementasikan")