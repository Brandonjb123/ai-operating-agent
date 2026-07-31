"""
Schema untuk endpoint autentikasi: register, login, dan token response.
Menggunakan Pydantic v2 dengan field validation.
"""

from pydantic import BaseModel, Field


class UserRegisterRequest(BaseModel):
    """
    Schema untuk request registrasi pengguna baru.
    """
    full_name: str = Field(..., min_length=1, description="Nama lengkap pengguna")
    email: str = Field(..., description="Alamat email valid")
    password: str = Field(..., min_length=8, description="Password minimal 8 karakter")


class UserLoginRequest(BaseModel):
    """
    Schema untuk request login.
    """
    email: str = Field(..., description="Email terdaftar")
    password: str = Field(..., description="Password akun")


class TokenResponse(BaseModel):
    """
    Schema untuk response yang berisi JWT token.
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="Bearer", description="Tipe token (default Bearer)")