# Continuous documentation and safe publishing

Date: 2026-08-31
Status: accepted

## Context

Project decisions must remain recoverable from the repository without relying on external conversations. Preparing commits in a project that uses API and messaging credentials also requires consistent, easy-to-run checks. Agentic Twin already provides a lightweight implementation suited to this repository.

## Decision

Adopt the Agentic Twin documentation and publishing structure. Keep architecture, operations, and ADRs in the repository. Centralize verification in a dependency-free Python script used by a shell wrapper, the pre-commit hook, and GitHub Actions. Generate commit metadata through the same ordered Gemini-to-Groq fallback, while requiring explicit human confirmation before staging, committing, or pushing.

## Consequences

- Code and documentation evolve in the same change.
- Local hooks and CI run the same verification.
- Publication requires explicit human confirmation.
- Commit metadata can tolerate individual model or provider failures.
- The secret scan is preventive and does not replace human review.
