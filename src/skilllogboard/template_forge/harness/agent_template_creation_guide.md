# Agent Template Creation Guide

1. Read `ResearchBrief.md`.
2. Review or create `TemplateSpec.md`.
3. Run `skilllog forge scaffold --spec TemplateSpec.md`.
4. Fill TODOs in plugin, synthetic example, tests, and docs.
5. Keep the synthetic example dependency-light and external-data-free.
6. Run `skilllog forge validate TEMPLATE_NAME`.
7. Mark the template Implemented only after validation and regression tests pass.

Do not add built-in LLM calls, cloud sync, automatic code generation, or heavy dependencies to core.
