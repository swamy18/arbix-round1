# LLM Usage Notes

## Development Approach

The project was developed with a combination of personal engineering decisions and AI-assisted workflow support. I designed the solution structure, reviewed and modified generated code, validated the implementation, and made the final decisions on backend behavior, frontend integration, debugging, and repository commits.

AI was used as a productivity tool for scaffolding, review, debugging, test suggestions, and documentation. The project should not be interpreted as fully AI-generated.

## Representative Prompts Used

1. "Build the complete backend for the coding assessment using FastAPI, Pydantic, Pytest, and a POST /score endpoint."

2. "Review the backend implementation against the assessment requirements and identify critical issues, nice-to-have improvements, and final recommendation."

3. "Build a minimal React frontend for the existing FastAPI backend with form fields, loading state, validation errors, network errors, and success response display."

4. "Review whether the React frontend on localhost:5173 can call the FastAPI backend on localhost:8000, and add minimal CORS middleware if missing."

5. "Perform a complete pre-submission verification for backend, tests, frontend, integration, CORS, and repository cleanliness."

## Example of Reviewed and Improved Output

During verification, the generated React frontend initially failed Vite build because `frontend/index.html` was missing. I reviewed the build error:

```text
Could not resolve entry module "index.html".
```

I identified this as a Vite project-structure issue, added the correct `frontend/index.html` entry file, reran `npm run build`, and confirmed the build succeeded. This was an example where generated output was not accepted as complete until it was tested, debugged, and corrected.

## Validation and Review

The backend was validated by starting the FastAPI server, checking Swagger docs, testing `POST /score` with valid and invalid payloads, and running Pytest.

The frontend was validated by installing dependencies, running a production build, starting the Vite development server, and confirming the app served successfully.

Repository cleanliness was reviewed by checking Git status and removing local artifacts such as logs, `__pycache__`, and `.pytest_cache`. Generated code and documentation were reviewed before committing.
