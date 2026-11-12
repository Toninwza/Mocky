# Mocky — working guide

Mocky is an open-source GUI for the official AWS Emulator (github.com/aws/aws-emulator),
focused on EC2 and the services around it. It is an unofficial community project:
never present it as an AWS product or use AWS logos.

## Git rules (mandatory)
- Commit author is the repo owner (already set in the repo's local git config). Do not change it.
- NEVER add `Co-Authored-By`, `Generated with`, session links or any AI attribution
  to commit messages, PR bodies, code comments or docs.
- Branches: `main` = releases only. `develop` = integration. Work on `feat/<topic>`
  branched from `develop`. Never push to `main`. Never force-push `develop`.
- Small, focused commits with conventional prefixes (`feat:`, `fix:`, `docs:`, `chore:`, `test:`).

## Stack
- Monorepo with pnpm workspaces: `apps/web` (React + Vite + TypeScript),
  `apps/server` (Node + Hono + AWS SDK for JavaScript v3), `packages/*` for shared code.
- The browser never talks to the emulator directly. The server proxies every call,
  trusts the emulator's self-signed CA, and records request history.

## Local emulator
- Endpoint `https://127.0.0.1:9297`, health at `GET /__admin/health`.
- CA file: `~/.aws/emulator/<port>/ca.pem`. With `-a on` (default), keys are in
  `~/.aws/emulator/<port>/emulator_credentials`; with `-a off` any credentials work.
- Region default `us-east-1`, account `000000000000`. A default VPC exists at boot.
- The emulator only implements part of each API. When a call returns 501 or a stub,
  show it clearly in the UI ("not supported by the emulator yet"), don't crash.

## Quality bar
- TypeScript strict. Lint + typecheck + tests must pass before a commit is merged.
- Every screen must handle loading, empty, error, and "not supported" states.
- Keep secrets out of the repo. No telemetry in Mocky itself.
