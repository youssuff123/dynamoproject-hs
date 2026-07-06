import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected_stats():
    """Independently recompute the expected values from access.log itself,
    rather than hardcoding numbers or importing the solution's logic."""
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    top_path = paths.most_common(1)[0][0] if paths else None
    return total, len(ips), top_path


def test_report_exists_and_valid_json():
    """Criterion 1: the agent must write a valid JSON file to /app/report.json."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    try:
        json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as e:
        raise AssertionError(f"report.json is not valid JSON: {e}")


def test_report_has_required_keys():
    """Criterion 2: report.json must contain exactly the keys
    total_requests, unique_ips, and top_path."""
    data = json.loads(REPORT_PATH.read_text())
    required = {"total_requests", "unique_ips", "top_path"}
    assert required <= data.keys(), f"missing keys: {required - data.keys()}"


def test_total_requests_correct():
    """Criterion 3: total_requests must equal the number of non-blank
    lines in /app/access.log."""
    expected_total, _, _ = _expected_stats()
    data = json.loads(REPORT_PATH.read_text())
    assert data["total_requests"] == expected_total, (
        f"expected total_requests={expected_total}, got {data['total_requests']}"
    )


def test_unique_ips_correct():
    """Criterion 4: unique_ips must equal the number of distinct client
    IP addresses (first field of each log line)."""
    _, expected_unique_ips, _ = _expected_stats()
    data = json.loads(REPORT_PATH.read_text())
    assert data["unique_ips"] == expected_unique_ips, (
        f"expected unique_ips={expected_unique_ips}, got {data['unique_ips']}"
    )


def test_top_path_correct():
    """Criterion 5: top_path must equal the most frequently requested
    path across all log entries."""
    _, _, expected_top_path = _expected_stats()
    data = json.loads(REPORT_PATH.read_text())
    assert data["top_path"] == expected_top_path, (
        f"expected top_path={expected_top_path!r}, got {data['top_path']!r}"
    )


def test_access_log_not_modified():
    """Criterion 6: the agent must not modify /app/access.log."""
    lines = [l for l in LOG_PATH.read_text().splitlines() if l.strip()]
    assert len(lines) == 6, "access.log appears to have been modified"
