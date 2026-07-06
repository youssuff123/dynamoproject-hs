There is an access log at /app/access.log, in Apache combined-log-style format
(one request per line: client IP, timestamp, quoted request line, status, size).

Parse it and write a JSON report to /app/report.json containing exactly these
three keys:

1. "total_requests": the total number of non-blank lines in the log.
2. "unique_ips": the number of distinct client IP addresses (the first
   whitespace-delimited field of each line).
3. "top_path": the request path (e.g. "/index.html") that appears most often
   across all requests, taken from the quoted request line and excluding the
   HTTP method and protocol version. If there is a tie, use whichever path
   appears first in the log.

Do not modify /app/access.log.

You have 120 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
