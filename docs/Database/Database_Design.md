# Database Design

Project: AI Operating Agent (AOA)

Version: 1.0

---

# Table of Contents

1. Introduction

Sprint 12 Database Baseline

2. Database Principles

3. Database Architecture

4. Core Entities

5. Relationships

6. Naming Conventions

7. Indexing Strategy

8. Future Modules

---

# 1. Introduction

This document defines the database architecture for the AI Operating Agent (AOA).

The database is designed to support a scalable, secure, and multi-tenant AI platform capable of managing organizations, users, Digital Employees, workflows, knowledge, memory, execution history, and integrations.

The objective is to provide a well-structured relational database that is maintainable, extensible, and optimized for enterprise-scale AI operations.

---

# Sprint 12 Database Baseline

This section records the database baseline at the completion of Sprint 12
Phase 12.1–12.6. It distinguishes implemented backend models from the AOA
target data architecture without removing future design.

- **Implemented foundation:** a backend model and relational persistence exist.
- **Partial / foundation:** supporting schema exists, but production capability
  or enforcement is incomplete.
- **Planned target:** a future AOA data capability; it is not an implemented
  backend entity or deployed storage component.

| Domain | Sprint 12 status | Backend authority / boundary |
| --- | --- | --- |
| Organization, User, Role, Membership | Implemented foundation | Models and PostgreSQL tables exist. RBAC and tenant-isolation enforcement are partial / foundation. |
| AIEmployee (UI: Digital Employee) | Implemented foundation | `ai_employee` is the backend table and central configuration owner. |
| Memory | Implemented foundation | `memory` CRUD and persistence exist; retrieval and runtime context integration are planned targets. |
| Knowledge | Implemented foundation | `knowledge` stores text-based records per AIEmployee; document ingestion, embedding, vector search, and RAG are planned targets. |
| Workflow | Implemented foundation | `workflow` stores definitions for sequential LLM steps; advanced controls are planned targets. |
| Workflow Execution | Implemented foundation | `workflow_execution` persists initial execution state and basic failure data; complete audit and operational execution history are partial / foundation. |
| Tooling, approval, analytics, and advanced monitoring | Planned target | No corresponding backend entities are implemented. |
| Vector, object, Redis, and logging/metrics storage | Planned target | These are future infrastructure/storage architecture, not deployed database components. |

Tenant relationship baseline:

```text
Organization → AIEmployee → Memory / Knowledge / Workflow → WorkflowExecution
```

`WorkflowExecution` also directly references `Organization` and `AIEmployee`
to preserve its execution ownership. The current default-organization
mechanism is temporary and must not be interpreted as production tenant
selection.

---

# 2. Database Principles

The AOA database follows several engineering principles.

## Multi-Tenant

Each organization owns its own data while sharing the same platform infrastructure.

---

## Normalized

The schema minimizes data duplication through proper normalization while maintaining performance.

---

## Scalable

The database supports future expansion without requiring major structural changes.

---

## Secure

Sensitive information such as passwords, credentials, and API keys are encrypted or securely stored.

---

## Auditable

Critical business operations are recorded for monitoring, compliance, and debugging.

---

## Extensible

New modules and entities can be added without modifying existing core structures.

---

## Consistency

The database enforces consistent relationships through foreign keys, constraints, and standardized naming conventions.

---

# 3. Database Architecture

The AOA platform uses PostgreSQL as its primary relational database.

The database is organized into modular business domains.

Core modules include:

- Organization
- User Management
- Digital Employees
- Workflow
- Knowledge Base
- Memory
- Execution

These are implemented foundation modules. Audit, analytics, approval, tools,
RAG/vector storage, document ingestion, external integrations, and advanced
monitoring remain planned target modules unless specifically described as
partial / foundation below.

Each implemented module is connected through well-defined relationships and
foreign keys.

The database architecture supports modular application development and can evolve toward a microservices architecture if future business requirements demand greater scalability.

---

# 4. Core Entities

The core database entities form the foundation of the AOA platform.

These entities are responsible for organization management, user access, and authorization.

The initial core entities include:

- Organization
- User
- Role
- Membership

Implemented backend entities also include AIEmployee (the backend technical
term for the UI’s Digital Employee), Memory, Knowledge, Workflow, and
WorkflowExecution.

---

## Organization

Represents a company or tenant using the AOA platform.

Responsibilities:

- Stores organization information
- Defines tenant boundaries
- Owns platform resources
- Serves as the root entity of the database

Fields:

- id (UUID)
- name
- slug
- description
- logo_url
- website
- status
- created_at
- updated_at

---

## User

Represents an individual platform user.

Responsibilities:

- Represents platform users
- Authenticates users
- Includes a direct `organization_id` foreign key in the current model
- Participates in organization membership through Membership records
- Tracks login activities

Fields:

- id (UUID)
- organization_id
- full_name
- email
- password_hash
- avatar_url
- status
- last_login
- created_at
- updated_at

---

## Role

Defines user permissions inside an organization.

Responsibilities:

- Defines access roles
- Supports Role-Based Access Control (RBAC)
- Organizes user permissions

Examples:

- Owner
- Admin
- Manager
- Employee
- Viewer

Fields:

- id (UUID)
- organization_id
- name
- description
- created_at
- updated_at

---

## Membership

Maps a user and role inside an organization.

The current model includes `organization_id`, `user_id`, and `role_id`. A user
can be represented in multiple organizations through Membership records;
therefore this document must not describe a User as belonging to exactly one
Organization. The direct `User.organization_id` remains part of the current
backend model and must not be removed or reinterpreted without a backend
schema change.

Responsibilities:

- Connects users and roles
- Supports multiple roles per user
- Records organization membership

Fields:

- id (UUID)
- organization_id
- user_id
- role_id
- joined_at
- created_at

---

## AIEmployee (UI: Digital Employee)

Status: **Implemented foundation**. The backend model and table are named
`AIEmployee` and `ai_employee`; product UI uses the term Digital Employee.

Responsibilities:

- Acts as the central configuration owner for a Digital Employee
- Belongs to an Organization
- Owns Memory, Knowledge, Workflow, and WorkflowExecution records

Fields:

- id (UUID)
- organization_id
- name
- description
- avatar_url
- provider
- model
- temperature
- max_tokens
- system_prompt
- status
- created_at
- updated_at

---

## Memory

Status: **Implemented foundation** for CRUD and persistence. Retrieval and
runtime context integration are planned targets.

Fields:

- id (UUID)
- organization_id
- ai_employee_id
- memory_key
- memory_value
- memory_type
- importance
- metadata
- last_accessed_at
- created_at
- updated_at

---

## Knowledge

Status: **Implemented foundation** for text-based CRUD per AIEmployee.
Document ingestion, parsing, embeddings, vector search, and RAG are planned
targets and do not have implemented database entities in this baseline.

Fields:

- id (UUID)
- organization_id
- ai_employee_id
- title
- content
- source
- knowledge_type
- status
- metadata
- created_at
- updated_at

---

## Workflow

Status: **Implemented foundation**. Workflow definitions are stored as JSON
and support sequential LLM steps in the current runtime. Branching,
retry/recovery, scheduling, parallelism, and approval are planned targets.

Fields:

- id (UUID)
- organization_id
- ai_employee_id
- name
- description
- definition
- status
- trigger_type
- created_at
- updated_at

---

## WorkflowExecution

Status: **Implemented foundation** for initial execution persistence and basic
failure data; complete audit and operational execution-history capability is
**partial / foundation**.

Fields:

- id (UUID)
- organization_id
- workflow_id
- ai_employee_id
- status
- trigger_type
- input_data
- output_data
- error_message
- started_at
- completed_at
- created_at
- updated_at

---

# 5. Relationships

The AOA database is designed using relational database principles.

Relationships between entities are established through foreign keys to ensure data integrity and consistency.

The current implemented relationships include:

- Organization → User (direct foreign key in the current User model)
- Organization → Role
- Organization → Membership
- User ↔ Role (through Membership)
- Organization → AIEmployee → Memory / Knowledge / Workflow
- Workflow → WorkflowExecution
- Organization / AIEmployee → WorkflowExecution

Future modules may introduce additional relationships only after their backend
entities are implemented.

---

## Organization → User

Relationship:

One Organization can have many Users through the current direct foreign key.

The current User model contains `organization_id`. Membership additionally
records organization membership, so this direct relationship must not be read
as a statement that a user can belong to only one organization.

Cardinality:

Organization (1) ---- (*) User

Foreign Key:

User.organization_id → Organization.id

---

## Organization → Role

Relationship:

One Organization can define multiple Roles.

Each Role belongs to one Organization.

Cardinality:

Organization (1) ---- (*) Role

Foreign Key:

Role.organization_id → Organization.id

---

## User ↔ Role

Relationship:

Users and Roles have a many-to-many relationship.

A User may have multiple Roles.

A Role may be assigned to multiple Users.

This relationship is implemented using the Membership table.

Cardinality:

User (*) ---- (*) Role

Bridge Table:

Membership

Foreign Keys:

Membership.organization_id → Organization.id

Membership.user_id → User.id

Membership.role_id → Role.id

---

## Relationship Diagram

```text
                    Organization
                    ┌──────────────┐
                    │ id           │
                    │ name         │
                    │ slug         │
                    └──────┬───────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
          User                          Role
┌────────────────────┐          ┌────────────────────┐
│ id                 │          │ id                 │
│ organization_id    │          │ organization_id    │
│ full_name          │          │ name               │
│ email              │          │ description        │
└─────────┬──────────┘          └─────────┬──────────┘
          │                               │
          └──────────────┬────────────────┘
                         ▼
                  Membership
            ┌────────────────────┐
            │ id                 │
            │ organization_id    │
            │ user_id            │
            │ role_id            │
            │ joined_at          │
            │ created_at         │
            └────────────────────┘
```

---

## Organization → AIEmployee → Domain Records

`AIEmployee` is the technical backend entity for the UI’s Digital Employee.
Each AIEmployee directly references its owning Organization. Memory, Knowledge,
and Workflow each directly reference both Organization and AIEmployee.

`WorkflowExecution` directly references Organization, AIEmployee, and
Workflow. These direct foreign keys preserve ownership at each stage of the
Sprint 12 execution foundation.

```text
Organization
  └── AIEmployee (Digital Employee in UI)
        ├── Memory
        ├── Knowledge
        └── Workflow
              └── WorkflowExecution

WorkflowExecution ── also references ── Organization and AIEmployee
```

Tenant isolation is **partial / foundation**: organization-scoped foreign keys
provide a data-model basis, but production tenant context and server-side
authorization/RBAC enforcement remain planned hardening.

---

# 6. Naming Conventions

The AOA database follows consistent naming conventions to improve readability and maintainability.

## Tables

Table names use singular nouns.

Examples:

- organization
- user
- role
- membership

---

## Columns

Column names use snake_case.

Examples:

- organization_id
- created_at
- updated_at

---

## Primary Keys

Primary keys use:

- id

---

## Foreign Keys

Foreign keys follow:

`<entity>_id`

Examples:

- organization_id
- user_id
- role_id

---

## Timestamp Columns

Standard timestamp fields:

- created_at
- updated_at

---

# 7. Indexing Strategy

Implemented primary keys, foreign keys, and model-defined uniqueness provide
the current foundation. Additional indexes must be introduced only through a
reviewed backend schema change and migration.

The indexing strategy will prioritize:

- Primary Keys
- Foreign Keys
- Frequently Queried Columns
- Unique Constraints
- Composite Indexes where appropriate

Future indexing will follow actual access patterns for implemented query paths;
it must not imply future entities or infrastructure are already deployed.

---

# 8. Planned Database Modules and Storage

The following are **planned targets**. They are retained as future AOA
architecture and must not be read as implemented backend tables or deployed
storage components:

- RAG/vector storage, embeddings, and document-ingestion records
- Tool Registry and external-integration credential/configuration records
- Approval System records
- Audit logs and complete execution-history records
- Analytics and monitoring records
- Advanced/distributed execution support records
- Object storage for documents and attachments
- Redis-backed cache, session, queue, or temporary execution state
- Dedicated logging and metrics storage

The current implemented entity set is limited to Organization, User, Role,
Membership, AIEmployee, Memory, Knowledge, Workflow, and WorkflowExecution.
