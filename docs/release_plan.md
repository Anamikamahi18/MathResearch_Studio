# Release Plan

This table defines milestone goals, key risks, and measurable success criteria for the planned roadmap versions.

| Version | Goals | Key Risks | Success Criteria |
|---|---|---|---|
| 1.0.0 | Deliver first end-to-end MVP workflow: PDF upload, text extraction, basic section detection, semantic search, grounded assistant, and notes export with Streamlit plus FastAPI integration. | PDF parsing quality may vary across paper formats; retrieval quality may be weak with initial chunking/embeddings; integration complexity between UI and API may slow delivery. | Users can upload PDFs and consistently run the full pipeline; search returns relevant paper-grounded results; assistant answers are source-grounded; notes export works for processed papers; core workflow is demo-ready and documented. |
| 1.1.0 | Stabilize and improve quality: better metadata extraction, stronger theorem-like structure detection, improved chunking/embeddings, cleaner UX, improved exports, initial notation dictionary. | Overfitting extraction heuristics to limited samples; increased complexity from iterative model tuning; regressions in existing MVP behavior while improving quality. | Measurable improvement in extraction and retrieval quality on an internal evaluation set; reduced user friction in core UI flows; notation dictionary available for at least initial use cases; backward compatibility with 1.0.0 workflows maintained. |
| 2.0.0 | Evolve into structured mathematical knowledge workspace: dependency graphs, stronger notation tracking, multi-paper organization, richer retrieval/filtering, more durable persistence. | Graph generation can become noisy without robust entity linking; notation ambiguity across papers may reduce trust; persistence migration may introduce data consistency issues. | Dependency graph is generated and explorable for multi-paper datasets; notation tracking improves cross-paper comprehension; retrieval supports practical filters and yields better relevance; persistence layer supports reliable save/load of research workspaces. |
| 3.0.0 | Expand to collaborative, extensible platform: research-group workflows, larger-scale libraries, external literature integrations, analytics dashboards, plugin/provider extensibility. | Collaboration features add access-control and synchronization complexity; scaling search/indexing may raise performance costs; external integrations may break due to API changes. | Multi-user or team workflows are operational; system handles larger collections with acceptable performance; external source integrations are stable; analytics surfaces actionable research insights; extension points allow adding providers with minimal core changes. |

## Notes

- Reassess risks at the start of each milestone and update mitigation actions.
- Keep success criteria observable and testable to support release decisions.
- Treat this document as the planning companion to the milestone summaries in `CHANGELOG.md` and `docs/tasks.md`.
