# dynamo/log-report

Parses an Apache combined-log-style access log and writes a JSON summary
report to /app/report.json with three keys: total_requests, unique_ips,
and top_path.

## Fixed from the broken submission
- task.toml: artifacts is now a TOML array pointing at the real output path.
- environment/Dockerfile: pinned to an approved base image by @sha256 digest;
  the leaked solution_hint.py was removed from the build context entirely;
  input data moved to environment/data/.
- tests/: verifier now recomputes expected values independently from
  access.log and asserts on them (not just file existence); reward and
  ctrf.json are written to /logs/verifier/ as required.
- instruction.md: names the absolute output path, exact JSON schema, tie-break
  rule, and ends with the required timeout line matching [agent].timeout_sec.

## How to verify
harbor run -p . --agent oracle   # expect reward 1.0
harbor run -p . --agent nop      # expect reward 0
