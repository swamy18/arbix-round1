# Arbix Round 1 - Credit Scoring Assessment

## Project Overview

This project implements a small full-stack scoring application for an agricultural credit assessment workflow.

The backend exposes a FastAPI `POST /score` endpoint that validates applicant inputs and returns a rule-based score, reason codes, request ID, and timestamp. The frontend provides a minimal React form that calls the backend and displays success, validation, and network-error states.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Pytest
- React
- Vite
- JavaScript
- CSS

## Setup Instructions

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Swagger docs are available at:

```text
http://127.0.0.1:8000/docs
```

Run backend tests from the repository root:

```bash
pytest -q backend/tests
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite app runs at:

```text
http://localhost:5173
```

Build verification:

```bash
npm run build
```

## Design Choices and Tradeoffs

- Kept scoring logic separate from the FastAPI route layer in `backend/scoring.py`.
- Used Pydantic models for request validation and response shape enforcement.
- Used explicit reason codes so the score is explainable.
- Used a simple weighted rule-based score instead of a model-driven approach because the assessment requested a simple rule system.
- Added CORS for `http://localhost:5173` only, which is appropriate for local development but should be environment-configured in production.
- Kept frontend styling minimal and dependency-free to prioritize correctness and speed.
- Included a `package-lock.json` for reproducible frontend installs.

## Time Spent

- Start time: 08:06 IST
- End time: 08:41 IST
- Approximate total time spent: 35 minutes

## Completed Items

- FastAPI backend with `POST /score`
- Pydantic validation for all required fields
- Rule-based scoring logic with exactly three reason codes
- Request and validation logging using Python logging
- Pytest happy-path and validation-error tests
- React frontend form using functional components and hooks
- Loading, success, validation-error, and network-error UI states
- Local CORS configuration for frontend-backend integration
- Vite build fix with `frontend/index.html`
- Repository cleanup rules for common generated artifacts

## Skipped Items

- No database persistence
- No authentication or authorization
- No deployment configuration
- No advanced frontend styling or component library
- No exhaustive scoring boundary test suite
- No centralized environment configuration for API URLs or CORS origins

## LLM / Tool Disclosure

This project was developed using a combination of personal implementation decisions and AI-assisted development.

I designed the solution structure, reviewed and modified generated code, validated behavior through tests and manual checks, and made the implementation, integration, and debugging decisions. AI assistance was used as a productivity tool for scaffolding, code review, debugging suggestions, testing ideas, and documentation support. It was not used as a replacement for engineering judgement.

## What I Would Improve With 2 More Hours

- Add more backend tests for scoring boundaries and invalid payload variants.
- Improve logging for invalid requests to include sanitized request input.
- Move API base URL and CORS origins into environment-based configuration.
- Add frontend tests for form submission and error rendering.
- Add a small health-check endpoint.
- Improve frontend accessibility details such as error focus handling and field-level validation messages.
