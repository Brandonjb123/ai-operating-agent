# AOA Development Roadmap

Project: AI Operating Agent (AOA)
Version: 1.0
Status: Active
Document Type: Canonical Development Roadmap

> This document is the single source of truth for AOA development sequencing.
>
> Sprint scope, architecture decisions, dependencies, and completion status
> must be reconciled against this document before starting new development.

---

## Mandatory Pre-Sprint Review

Before starting any new sprint, verify:

- Current sprint status
- Previous sprint completion
- Product objective
- PRD scope
- System architecture
- Relevant database design
- Existing implementation
- Known limitations
- Architectural decisions
- Dependencies

No sprint may be started solely from conversational context.

# 1. Product Definition

AI Operating Agent (AOA) is an Enterprise AI Operating System designed to
help organizations build, manage, orchestrate, and supervise Digital Employees
powered by Large Language Models (LLMs).

AOA is NOT a traditional chatbot.

The platform is designed to operate a Digital Workforce where AI Employees
perform real business tasks while operating within organizational governance,
security, permissions, knowledge, memory, workflows, tools, and human
oversight.

The long-term objective is to allow organizations to manage Digital Employees
similarly to how they manage human employees.

---

# 2. Core Product Model

AOA operates around the following hierarchy:

Organization
│
├── Users
├── Roles
├── Memberships
│
└── Digital Employees
    │
    ├── Identity / Role
    ├── Goals
    ├── Instructions
    ├── Permissions
    ├── Memory
    ├── Knowledge
    ├── Workflows
    └── Tools
            │
            ▼
      Execution Engine
            │
      ┌─────┼─────────────┐
      ▼     ▼             ▼
   Planning Reasoning    Tools
      │     │             │
      └─────┼─────────────┘
            ▼
       Business Action

---

# 3. Product Principles

AOA development must preserve:

- Modular architecture
- Multi-tenancy
- Security
- Observability
- Extensibility
- Testability
- Human oversight
- Separation of business logic and AI execution
- Provider-agnostic AI architecture
- Clear separation between definition and execution

AOA should evolve as an AI-first enterprise platform rather than as a
traditional CRUD application or standalone chatbot.

---

# 4. Architectural Layers

AOA follows a layered architecture:

Presentation Layer
        ↓
API Layer
        ↓
AI Execution Layer
        ↓
Business Services Layer
        ↓
Data Layer
        ↓
External Services Layer

Core components:

- Frontend
- Backend API
- Execution Engine
- Business Services
- Data Layer
- External Integrations

The frontend communicates with the backend through REST APIs and must not
contain business logic or AI reasoning.

---

# 5. Product Milestones

The official product release strategy defines the following milestones.

## V0.1 — Foundation

Scope:

- Authentication
- Organization
- Basic Dashboard

Status:

COMPLETE / implemented through early development sprints.

---

## V0.2 — Digital Employee

Scope:

- Employee Management
- Prompt Configuration
- Goal Configuration

Status:

COMPLETE / implemented through Sprint 7.

---

## V0.3 — Knowledge

Scope:

- Document Upload
- Embedding
- RAG
- Vector Search

Status:

PARTIAL / foundation implemented.

Current implementation includes the Knowledge entity,
repository, service, schema, API, and PostgreSQL persistence.

Full document processing, embeddings, vector search, and RAG remain future
implementation work.

---

## V0.4 — Workflow

Scope:

- Workflow Builder
- Tool Calling
- Human Approval

Status:

PARTIAL / Workflow Definition and initial execution foundation implemented.

---

## V0.5 — Execution Engine

Scope:

- Planning
- Memory
- Reasoning
- Logging

Status:

IN PROGRESS / execution foundation implemented.

Sprint 11 implemented the initial Workflow Runtime and LLM execution
foundation.

---

## V1.0 — Production Release

Target capabilities:

- Enterprise Dashboard
- Monitoring
- Analytics
- Stable APIs
- Production Deployment

Additional V1 requirements defined in the PRD include:

- Authentication & Authorization
- Organization Management
- Digital Employee Management
- Knowledge Management
- Memory Management
- Workflow Management
- Tool Integrations
- Execution Engine
- Monitoring
- Dashboard

V1 explicitly excludes:

- AI Marketplace
- Multi-region deployment
- Voice Agent
- Video Agent
- Mobile application
- Billing system
- Plugin Marketplace
- Self-learning agents
- Autonomous organization management

---

# 6. Sprint Roadmap

## Sprint 1 — Foundation

Status: COMPLETE

Objective:

Establish the initial project foundation.

Delivered:

- Project structure
- Development environment
- Initial application foundation

---

## Sprint 2 — FastAPI

Status: COMPLETE

Objective:

Establish the FastAPI backend foundation.

Delivered:

- FastAPI application
- API foundation
- Basic backend structure

---

## Sprint 3 — Configuration

Status: COMPLETE

Objective:

Establish centralized application configuration and environment handling.

Delivered:

- Configuration foundation
- Environment variable handling
- Application settings

---

## Sprint 4 — Database

Status: COMPLETE

Objective:

Establish the PostgreSQL database layer and migration system.

Delivered:

- PostgreSQL
- SQLAlchemy
- Alembic
- Database models
- Initial migrations

Core initial entities:

- Organization
- User
- Role
- Membership

---

## Sprint 5 — Authentication

Status: COMPLETE

Objective:

Implement user authentication and protected access.

Delivered:

- Authentication foundation
- JWT-based authentication
- Login / logout flow
- Authentication-related API layer

---

## Sprint 6 — Multi-Tenant

Status: COMPLETE

Objective:

Establish organization-level tenant isolation and organization relationships.

Delivered:

- Organization management
- User relationships
- Role management
- Membership management
- Multi-tenant data boundaries

---

## Sprint 7 — Digital Employee

Status: COMPLETE

Objective:

Create the Digital Employee foundation.

Delivered:

- AI Employee model
- AI Employee repository
- AI Employee service
- AI Employee schemas
- AI Employee API
- PostgreSQL migration
- Integration testing

Core concept:

Organization
    ↓
AI Employee

The Digital Employee becomes the central AI worker entity to which
Memory, Knowledge, Workflow, and future Tools are attached.

---

## Sprint 8 — Memory System

Status: COMPLETE

Objective:

Build persistent AI memory.

Delivered:

- Memory model
- Memory repository
- Memory service
- Memory schemas
- Memory API
- PostgreSQL migration
- Integration testing

Memory supports:

- Agent-specific memories
- Memory types
- Importance ranking
- Metadata
- Last-access tracking

Memory is intended to support future context building, RAG integration,
and execution-time memory retrieval.

---

## Sprint 9 — Knowledge Base

Status: COMPLETE

Objective:

Build structured Knowledge Base infrastructure.

Delivered:

- Knowledge model
- Knowledge repository
- Knowledge service
- Knowledge schemas
- Knowledge API
- PostgreSQL migration
- Integration testing

Knowledge supports:

- Agent-specific knowledge
- Knowledge types
- Status lifecycle
- Metadata
- Source tracking

Important distinction:

Memory
= information the AI remembers.

Knowledge
= structured reference information the AI knows.

Future Knowledge capabilities include:

- Document processing
- Embeddings
- Vector search
- RAG

---

## Sprint 10 — Workflow Definition

Status: COMPLETE

Objective:

Build the Workflow Definition layer.

Delivered:

- Workflow model
- Workflow repository
- Workflow service
- Workflow schemas
- Workflow API
- PostgreSQL migration
- Integration testing

Workflow supports:

- Workflow definition
- Trigger type
- Status
- JSON definition
- Agent-specific workflows

Trigger types currently defined:

- manual
- api
- schedule
- event

Architectural boundary:

Workflow Definition
        ≠
Workflow Execution

Sprint 10 defines WHAT the AI should do.

It does not execute the workflow.

---

## Sprint 11 — Workflow Runtime / AI Execution Foundation

Status: COMPLETE

Objective:

Build the initial execution layer responsible for running persisted
workflow definitions.

Delivered:

- WorkflowExecution model
- WorkflowExecution repository
- WorkflowExecution service
- WorkflowExecution schemas
- Workflow execution API
- ExecutionContext
- StepResult
- StepExecutor abstraction
- ExecutorRegistry
- LLMExecutor
- WorkflowRuntime
- LLMProvider abstraction
- GroqProvider
- MockLLMProvider
- Execution integration tests

Execution flow:

API
 ↓
WorkflowRuntime
 ↓
ExecutorRegistry
 ↓
LLMExecutor
 ↓
LLMProvider
 ↓
Groq / Mock Provider

Verified:

- pending → running
- running → completed
- running → failed
- sequential multi-step execution
- execution persistence
- safe error handling
- unsupported step handling
- execution not found handling
- Swagger integration
- regression tests

Important limitation:

Sprint 11 provides the initial execution foundation.

The complete AOA Execution Engine described in the architecture still includes
additional capabilities such as:

- Planning
- Reasoning
- Memory Retrieval
- Knowledge Retrieval
- Tool Invocation
- Validation
- Memory Update
- Logging
- Human Approval
- Advanced workflow execution

These capabilities must NOT be assumed to be complete merely because Sprint 11
is marked complete.

---

# 7. Sprint 12 — Frontend

Status: COMPLETE

Objective:

Build the AOA frontend / presentation layer on top of the existing backend
and AI infrastructure.

Technology:

- Next.js

The frontend communicates with the backend through REST APIs.

The frontend must NOT contain:

- Business logic
- Database logic
- AI reasoning
- Workflow execution logic
- LLM provider logic

Primary frontend areas defined by the System Architecture:

- Authentication
- Dashboard
- Chat Interface
- Digital Employee Management
- Workflow Management
- Knowledge Management
- Approval Center
- Analytics Dashboard
- System Settings

Additional V1 dashboard requirements include:

- Organization Dashboard
- Employee Dashboard
- Task Dashboard
- Analytics Overview

Sprint 12 checkpoints:

- Phase 12.1 — Frontend Foundation: COMPLETED
- Phase 12.2 — Authentication: COMPLETED
- Phase 12.3 — Layout & Navigation: COMPLETED
- Phase 12.4 — Digital Employees UI: COMPLETED
- Phase 12.5 — Workflow UI: COMPLETED
- Phase 12.6 — Knowledge UI: COMPLETED

Checkpoint: Phase 12.6 — Knowledge UI completed; Sprint 12 frontend scope is
complete.

---

# 8. Future Capability Areas

The following capabilities are part of the AOA product architecture but are
NOT automatically assigned to Sprint 12.

They must be scheduled explicitly in a future roadmap update.

## Advanced Workflow

Potential capabilities:

- Conditional branching
- Parallel execution
- Human-in-the-loop
- Retry logic
- Error recovery
- Alternative paths
- Advanced workflow orchestration

---

## Tool Engine

Potential integrations:

- Gmail
- Google Calendar
- Google Drive
- Slack
- WhatsApp
- REST APIs
- PostgreSQL
- Other enterprise systems

Tool Engine responsibilities include:

- Tool registration
- Credential management
- Permission assignment
- Tool configuration
- Tool invocation

---

## Planning Engine

Responsibilities:

- Understand user intent
- Identify business objectives
- Select workflows
- Determine required tools
- Evaluate approval requirements

---

## Reasoning Engine

Inputs may include:

- Goal
- Instructions
- Memory
- Knowledge
- User request
- Business policies

Outputs may include:

- Recommended action
- Decision rationale
- Confidence estimation

---

## Memory Engine

Future capabilities:

- Short-term memory
- Long-term memory
- Conversation history
- Shared memory
- Business context
- Execution-time retrieval

---

## Knowledge Engine

Future capabilities:

- Semantic retrieval
- Embeddings
- Vector search
- RAG
- Knowledge ingestion
- Knowledge indexing

---

## Human Collaboration

Future capabilities:

- Approval requests
- Manual override
- Feedback
- Escalation
- Task assignment

Critical actions may require human approval.

---

## Monitoring & Observability

Future capabilities:

- Live execution status
- Execution logs
- Error tracking
- Token usage
- Cost tracking
- Performance metrics
- Execution traces
- Structured logs
- Audit events

---

## Analytics

Future capabilities:

- Productivity metrics
- Cost analysis
- Agent performance
- Workflow analytics
- Business metrics

---

# 9. Dependency Map

The major dependency chain is:

Organization
    ↓
Users / Roles / Memberships
    ↓
Digital Employee
    ↓
┌───────────────┬────────────────┬────────────────┐
│               │                │
Memory       Knowledge       Workflow
│               │                │
└───────────────┴────────────────┘
                ↓
        Workflow Execution
                ↓
        Execution Engine
                ↓
      ┌─────────┼─────────┐
      │         │         │
   Planning  Reasoning  Tools
      │         │         │
      └─────────┼─────────┘
                ↓
         Business Action
                ↓
      Validation / Memory
                ↓
          Audit / Metrics

Frontend
    ↓
Backend API
    ↓
Existing platform services

The frontend is a presentation layer and does not replace the execution
architecture.

---

# 10. Current Project State

Current completed sprint:

Sprint 12 — Frontend

Current next sprint:

TBD — must be explicitly planned and approved.

Current backend foundations:

- Organization
- User
- Role
- Membership
- AI Employee
- Memory
- Knowledge
- Workflow
- Workflow Execution
- Workflow Runtime
- LLM Provider abstraction

Current AI execution capability:

- Sequential workflow execution
- LLM step execution
- Provider abstraction
- Groq provider
- Mock provider
- Execution persistence
- Failure handling

Current known gaps:

- Full Tool Engine
- Full Planning Engine
- Full Reasoning Engine
- Full Knowledge/RAG execution integration
- Full Memory Engine integration
- Human Approval runtime
- Advanced workflow branching
- Retry / recovery
- Monitoring
- Analytics

---

# 11. Roadmap Rules

1. Do not silently change sprint scope.

2. Do not move a capability from one sprint to another without updating this
   document.

3. Product requirements must be checked against the PRD.

4. Architecture decisions must be checked against System Architecture.

5. Actual implementation status must be checked against the Sprint Journal.

6. A sprint may be marked COMPLETE only when its defined acceptance criteria
   are verified.

7. "Foundation implemented" must not be interpreted as "entire product
   capability completed."

8. Future capabilities must remain explicitly marked as future until assigned
   to an approved sprint.

9. Frontend must remain separated from backend business logic and AI
   execution.

10. Workflow Definition and Workflow Execution remain separate architectural
    concepts.

---

# 12. Source of Truth

The following documents are authoritative for AOA development:

1. PRD
2. System Architecture
3. Database Design
4. Development Standards
5. Sprint Journal
6. This Roadmap

When documents conflict:

- Do not silently resolve the conflict.
- Identify the conflict.
- Review the relevant architectural/product decision.
- Update the canonical document explicitly.

Chat conversation memory is NOT considered a source of truth.

---

# 13. Current Decision

As of the current project state:

Sprint 11 = COMPLETE

Sprint 12 = COMPLETE

Advanced workflow capabilities such as Tool Execution, Scheduling,
Retry, Recovery, Human Approval, and related execution enhancements
are NOT assigned to Sprint 12 by this document unless explicitly added
through a future roadmap revision.

---

# 14. Roadmap Status

┌─────────┬──────────────────────────────────────┬──────────────┐
│ Sprint  │ Scope                                │ Status       │
├─────────┼──────────────────────────────────────┼──────────────┤
│ 1       │ Foundation                           │ COMPLETE     │
│ 2       │ FastAPI                              │ COMPLETE     │
│ 3       │ Configuration                        │ COMPLETE     │
│ 4       │ Database                             │ COMPLETE     │
│ 5       │ Authentication                       │ COMPLETE     │
│ 6       │ Multi-Tenant                         │ COMPLETE     │
│ 7       │ Digital Employee                     │ COMPLETE     │
│ 8       │ Memory System                        │ COMPLETE     │
│ 9       │ Knowledge Base                       │ COMPLETE     │
│ 10      │ Workflow Definition                  │ COMPLETE     │
│ 11      │ Workflow Runtime / AI Engine         │ COMPLETE     │
│ 12      │ Frontend                             │ COMPLETE     │
└─────────┴──────────────────────────────────────┴──────────────┘

Future sprints after Sprint 12:

TBD — must be explicitly planned and approved.
