"""
AIEmployee Service — logika bisnis untuk manajemen AI employee.
Menggunakan OrganizationRepository & AIEmployeeRepository melalui dependency injection.
Tidak mengakses Session secara langsung.
"""

from uuid import UUID

from app.models.ai_employee import AIEmployee
from app.repositories.ai_employee_repository import AIEmployeeRepository
from app.repositories.organization_repository import OrganizationRepository
from app.schemas.ai_employee import (
    AIEmployeeCreateRequest,
    AIEmployeeUpdateRequest,
    AIEmployeeResponse,
    ALLOWED_PROVIDERS,
)


class AIEmployeeService:
    """Service untuk manajemen AI employee dalam organisasi."""

    def __init__(
        self,
        ai_employee_repo: AIEmployeeRepository,
        org_repo: OrganizationRepository,
    ) -> None:
        """
        Inisialisasi service dengan repository yang di-inject.

        Args:
            ai_employee_repo: Repository untuk AIEmployee.
            org_repo: Repository untuk Organization.
        """
        self.ai_employee_repo = ai_employee_repo
        self.org_repo = org_repo

    def list_ai_employees(self, organization_id: UUID) -> list[AIEmployeeResponse]:
        """
        Mendaftar semua AI employee dalam satu organisasi.
        """
        employees = self.ai_employee_repo.list_by_organization(organization_id)
        return [AIEmployeeResponse.model_validate(e) for e in employees]

    def get_ai_employee(self, employee_id: UUID) -> AIEmployeeResponse:
        """
        Mendapatkan AI employee berdasarkan ID.
        Raise ValueError jika tidak ditemukan.
        """
        emp = self.ai_employee_repo.get_by_id(employee_id)
        if emp is None:
            raise ValueError("AI Employee not found")
        return AIEmployeeResponse.model_validate(emp)

    def create_ai_employee(self, request: AIEmployeeCreateRequest) -> AIEmployeeResponse:
        """
        Membuat AI employee baru dengan aturan bisnis.
        """
        # 1. Pastikan organisasi ada
        org = self.org_repo.get_by_id(request.organization_id)
        if org is None:
            raise ValueError("Organization not found")

        # 2. Nama tidak boleh kosong (sudah divalidasi schema)
        name = request.name.strip()
        if not name:
            raise ValueError("AI employee name is required")

        # 3. Cek duplikat nama dalam organisasi yang sama
        existing = self.ai_employee_repo.get_by_name(request.organization_id, name)
        if existing:
            raise ValueError("AI employee with this name already exists in organization")

        # 4. Validasi provider (sudah divalidasi schema)
        provider = request.provider.lower()
        if provider not in ALLOWED_PROVIDERS:
            raise ValueError(f"Unsupported provider '{provider}'")

        # 5. System prompt tidak boleh kosong
        system_prompt = request.system_prompt.strip()
        if not system_prompt:
            raise ValueError("System prompt cannot be empty")

        # Buat objek AIEmployee
        employee = AIEmployee(
            organization_id=request.organization_id,
            name=name,
            description=request.description,
            avatar_url=request.avatar_url,
            provider=provider,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            system_prompt=system_prompt,
            status=request.status or "active",
        )
        saved = self.ai_employee_repo.create(employee)
        return AIEmployeeResponse.model_validate(saved)

    def update_ai_employee(
        self, employee_id: UUID, request: AIEmployeeUpdateRequest
    ) -> AIEmployeeResponse:
        """
        Memperbarui AI employee. Hanya field yang tidak None yang diupdate.
        """
        emp = self.ai_employee_repo.get_by_id(employee_id)
        if emp is None:
            raise ValueError("AI Employee not found")

        # Nama
        if request.name is not None:
            new_name = request.name.strip()
            if not new_name:
                raise ValueError("AI employee name is required")
            existing = self.ai_employee_repo.get_by_name(emp.organization_id, new_name)
            if existing and existing.id != employee_id:
                raise ValueError("AI employee with this name already exists in organization")
            emp.name = new_name

        # Provider
        if request.provider is not None:
            provider = request.provider.lower()
            if provider not in ALLOWED_PROVIDERS:
                raise ValueError(f"Unsupported provider '{provider}'")
            emp.provider = provider

        # System prompt
        if request.system_prompt is not None:
            sp = request.system_prompt.strip()
            if not sp:
                raise ValueError("System prompt cannot be empty")
            emp.system_prompt = sp

        # Temperature
        if request.temperature is not None:
            if not (0.0 <= request.temperature <= 2.0):
                raise ValueError("Temperature must be between 0 and 2")
            emp.temperature = request.temperature

        # Max tokens
        if request.max_tokens is not None:
            if request.max_tokens <= 0:
                raise ValueError("max_tokens must be positive")
            emp.max_tokens = request.max_tokens

        # Field lainnya
        if request.description is not None:
            emp.description = request.description
        if request.avatar_url is not None:
            emp.avatar_url = request.avatar_url
        if request.model is not None:
            emp.model = request.model
        if request.status is not None:
            emp.status = request.status

        updated = self.ai_employee_repo.update(emp)
        return AIEmployeeResponse.model_validate(updated)

    def delete_ai_employee(self, employee_id: UUID) -> None:
        """
        Menghapus AI employee.
        """
        emp = self.ai_employee_repo.get_by_id(employee_id)
        if emp is None:
            raise ValueError("AI Employee not found")
        self.ai_employee_repo.delete(emp)