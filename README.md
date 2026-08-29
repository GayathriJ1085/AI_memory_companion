# AI Memory Companion — Phase 1

## Basic Conversational AI

Phase 1 establishes the foundation of the **AI Memory Companion** project.

The goal of this phase is to build a reliable text-based conversational system that will later become the software brain of a personalized AI companion.

At this stage, the project focuses only on the **basic AI and conversation infrastructure**.

---

## Phase 1 Goal

Build a reliable text conversation system capable of:

* Text-based interaction
* Backend API communication
* LLM integration
* Session-based conversation history
* Error handling
* Basic companion personality

---

## Current Phase Scope

### Included

* Next.js frontend foundation
* FastAPI backend foundation
* AI provider abstraction
* Gemini API integration
* Environment-based configuration
* Basic AI error handling
* Python virtual environment
* Project-level Git repository

### Not Included Yet

The following features are intentionally excluded from Phase 1:

* Long-term personal memory
* Personal knowledge system
* Continuous learning
* Caregiver system
* Emergency automation
* Voice interaction
* Pet/avatar interface
* Hardware integration
* Vector database
* Persistent user profiles

These will be introduced in later development phases.

---

# Project Architecture

The Phase 1 architecture is designed to keep the AI provider separate from the conversation system.

```text
                         USER
                           │
                           ▼
                    Next.js Frontend
                           │
                           ▼
                     FastAPI Backend
                           │
                           ▼
                  Conversation Service
                           │
                           ▼
                  Conversation Engine
                           │
                           ▼
                      LLM Service
                           │
                           ▼
                     AI Provider
                           │
                           ▼
                   Gemini API
                           │
                           ▼
                  Gemini 3.6 Flash
```

The architecture uses an abstraction layer so that the AI provider can be replaced in the future without rewriting the rest of the application.

---

# Project Structure

```text
phase-01-basic-ai/
│
├── apps/
│   │
│   ├── api/
│   │   ├── main.py
│   │   │
│   │   ├── routes/
│   │   │   └── chat.py
│   │   │
│   │   ├── schemas/
│   │   │   └── chat.py
│   │   │
│   │   └── services/
│   │       ├── conversation_service.py
│   │       └── llm_service.py
│   │
│   └── web/
│       ├── app/
│       │   ├── page.tsx
│       │   ├── layout.tsx
│       │   └── chat/
│       │       └── page.tsx
│       │
│       ├── components/
│       │   ├── ChatWindow.tsx
│       │   ├── MessageList.tsx
│       │   ├── MessageInput.tsx
│       │   └── LoadingIndicator.tsx
│       │
│       └── lib/
│           └── api.ts
│
├── core/
│   │
│   ├── ai/
│   │   ├── provider.py
│   │   ├── models.py
│   │   └── errors.py
│   │
│   └── conversation/
│       ├── orchestrator.py
│       ├── context.py
│       ├── session.py
│       └── prompts.py
│
├── tests/
│   └── unit/
│       └── test_conversation.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

# Technology Stack

## Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

## AI

* Google Gemini API
* `google-genai` Python SDK
* Gemini 3.6 Flash

## Configuration

* `python-dotenv`
* Environment variables

## Development

* Python virtual environment
* npm
* Git

---

# AI Provider Architecture

The project does not directly couple the conversation system to Gemini.

Instead, an abstract provider interface is used:

```text
AIProvider
     │
     ▼
GeminiProvider
     │
     ▼
Gemini API
```

The abstraction is defined in:

```text
core/ai/provider.py
```

AI-related data structures are defined in:

```text
core/ai/models.py
```

AI-specific exceptions are defined in:

```text
core/ai/errors.py
```

The application-level LLM service is located at:

```text
apps/api/services/llm_service.py
```

This design allows additional providers to be added later.

For example:

```text
AIProvider
├── GeminiProvider
├── OpenAIProvider
└── LocalProvider
```

The rest of the application can continue using the same `AIProvider` interface.

---

# Environment Configuration

The project uses environment variables for API configuration.

Example:

```env
AI_PROVIDER=gemini

GEMINI_API_KEY=

GEMINI_MODEL=gemini-3.6-flash
```

The actual API key must be stored in:

```text
.env
```

The `.env` file must never be committed to GitHub.

Only the template file is committed:

```text
.env.example
```

---

# Completed Setup

The following components have been successfully established:

### 1. Project Structure

The complete Phase 1 directory structure has been created.

### 2. Python Environment

A project-specific Python virtual environment has been created:

```text
.venv/
```

### 3. Backend

FastAPI has been configured and verified.

The backend currently exposes:

```text
GET /
GET /health
```

The API documentation is available through FastAPI's development documentation.

### 4. Frontend

Next.js has been initialized successfully.

The development server runs on:

```text
http://localhost:3000
```

### 5. AI Provider Abstraction

The provider-independent AI interface has been implemented.

### 6. Gemini Integration

Gemini API connectivity has been successfully tested using:

```text
gemini-3.6-flash
```

A successful test response has been received from the Gemini API.

### 7. Error Handling Foundation

AI-specific exception classes have been established for:

* General AI errors
* Provider errors
* Configuration errors

---

# Current Development Status

```text
Phase 1 — Basic Conversational AI

Project Structure          ✅ Complete
Python Environment         ✅ Complete
Next.js Setup              ✅ Complete
FastAPI Setup              ✅ Complete
AI Abstraction             ✅ Complete
Gemini Integration         ✅ Tested

Conversation Engine        ⏳ In Progress
Session History            ⏳ Pending
Context Management         ⏳ Pending
Companion Personality      ⏳ Pending
Chat API                   ⏳ Pending
Frontend Chat              ⏳ Pending
Error Handling Integration ⏳ Pending
Unit Tests                 ⏳ Pending
```

---

# Development Principle

The first version intentionally focuses on the **conversation foundation**.

The AI should first become reliable at holding a coherent conversation within a single session.

Long-term personal memory will not be implemented in this phase.

The distinction is:

```text
Phase 1

Current Session
      │
      ├── User message
      ├── AI response
      ├── User message
      └── AI response

              ↓

       Session ends
              ↓

       History discarded
```

Long-term memory will be introduced in Phase 2.

---

# Phase 1 Success Condition

Phase 1 will be considered complete when:

> **The system can hold a coherent conversation inside one session.**

The complete flow will eventually be:

```text
User
 ↓
Next.js Chat Interface
 ↓
FastAPI /chat
 ↓
Conversation Service
 ↓
Conversation Orchestrator
 ↓
Session Context
 ↓
LLM Service
 ↓
Gemini
 ↓
AI Response
 ↓
Session Updated
 ↓
Frontend
 ↓
User
```

---

# Future Development

After Phase 1 is completed, development will continue through the planned phases:

```text
Phase 1
Basic Conversational AI
        ↓
Phase 2
Reliable Memory
        ↓
Phase 3
Personal Knowledge
        ↓
Phase 4
Continuous Learning
        ↓
Phase 5
Reminders + Proactive AI
        ↓
Phase 6
Privacy + Safety
        ↓
Phase 7
Caregiver + Emergency
        ↓
Phase 8
Voice
        ↓
Phase 9
Companion / Pet Interface
```

The eventual goal is to use the same software intelligence as the backend brain of a future physical companion device.

---

## Status

**Current Phase:** Phase 1 — Basic Conversational AI

**Current Stage:** Foundation and LLM integration

**Project Type:** Prototype

**Hardware:** Not currently included
