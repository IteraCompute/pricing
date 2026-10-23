# IteraCompute Pricing CLI

## Default publication policy (2026-10-23)

- Keep GitHub Actions disabled. Fetch current `origin/main` and tags, select one owner and exact commits, and run checks relevant to the changed CLI behavior locally before merging. Never substitute an older branch for newer production work.
- This repository publishes a CLI and documentation; it has no independent production service. Documentation-only changes do not deploy applications. Price claims come from the public model catalogue; do not interpret missing pricing metadata as free usage.
- Shared Platform/Gateway changes must use the LLMProxy [local release workflow](https://github.com/IteraCompute/LLMProxy/blob/main/docs/local-release-workflow.md): `doctor` → `prepare` → `pipeline`, detached controller jobs, then `verify-live` → `report` → `finish`. Bind this clean repository's commit with `--related-repo`; the commands run in LLMProxy, not this repository.
- Build images on the device initiating the release. Reuse only verified identical-input offline evidence; production migration, health, streaming and rollback gates remain fresh. Query the original job after disconnects; never replay an unknown mutation. Retain exact commits, immutable digests and results. This policy supersedes old Actions or remote-build instructions.
- Never commit populated credentials, customer data or private infrastructure details.
