"""HTML report generator."""

from pathlib import Path

from jinja2 import Template

from eval_fw.reporting.base import Reporter, TestReport

DEFAULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Evaluation Report</title>
    <style>
        :root {
            --bg: #1a1a2e;
            --card: #16213e;
            --text: #eee;
            --muted: #888;
            --success: #00d26a;
            --danger: #ff6b6b;
            --warning: #ffc107;
            --border: #333;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 2rem;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { margin-bottom: 1rem; color: #fff; }
        h2 { margin: 2rem 0 1rem; color: #fff; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat {
            background: var(--card);
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value { font-size: 2rem; font-weight: bold; }
        .stat-label { color: var(--muted); font-size: 0.875rem; }
        .stat.success .stat-value { color: var(--success); }
        .stat.danger .stat-value { color: var(--danger); }
        .stat.warning .stat-value { color: var(--warning); }
        .meta { color: var(--muted); margin-bottom: 2rem; font-size: 0.875rem; }
        .test-card {
            background: var(--card);
            border-radius: 8px;
            margin-bottom: 1rem;
            overflow: hidden;
        }
        .test-header {
            padding: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            border-bottom: 1px solid var(--border);
        }
        .test-header:hover { background: rgba(255,255,255,0.05); }
        .test-id { font-weight: bold; font-family: monospace; }
        .badge {
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
        }
        .badge.pass { background: var(--success); color: #000; }
        .badge.fail { background: var(--danger); color: #fff; }
        .badge.error { background: var(--warning); color: #000; }
        .test-body { padding: 1rem; display: none; }
        .test-card.open .test-body { display: block; }
        .prompt-section { margin-bottom: 1rem; }
        .prompt-label { color: var(--muted); font-size: 0.75rem; text-transform: uppercase; margin-bottom: 0.25rem; }
        .prompt-content {
            background: rgba(0,0,0,0.3);
            padding: 1rem;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.875rem;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .response { border-left: 3px solid var(--muted); }
        .response.jailbroken { border-color: var(--danger); }
        .response.safe { border-color: var(--success); }
    </style>
</head>
<body>
    <div class="container">
        <h1>Security Evaluation Report</h1>
        <div class="meta">
            <p>Target Model: <strong>{{ target_model }}</strong> | Guard Model: <strong>{{ guard_model }}</strong></p>
            <p>Generated: {{ generated_at }} | Duration: {{ duration_seconds }}s</p>
        </div>

        <div class="summary">
            <div class="stat">
                <div class="stat-value">{{ summary.total }}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat success">
                <div class="stat-value">{{ summary.passed }}</div>
                <div class="stat-label">Passed (Safe)</div>
            </div>
            <div class="stat danger">
                <div class="stat-value">{{ summary.failed }}</div>
                <div class="stat-label">Failed (Jailbroken)</div>
            </div>
            <div class="stat warning">
                <div class="stat-value">{{ summary.errors }}</div>
                <div class="stat-label">Errors</div>
            </div>
            <div class="stat">
                <div class="stat-value">{{ summary.pass_rate }}%</div>
                <div class="stat-label">Pass Rate</div>
            </div>
        </div>

        <h2>Test Results</h2>
        {% for result in results %}
        <div class="test-card">
            <div class="test-header" onclick="this.parentElement.classList.toggle('open')">
                <span>
                    <span class="test-id">{{ result.test_id }}</span>
                    <span style="color: var(--muted); margin-left: 1rem;">{{ result.description[:60] }}{% if result.description|length > 60 %}...{% endif %}</span>
                </span>
                {% if result.error %}
                <span class="badge error">Error</span>
                {% elif result.jailbroken %}
                <span class="badge fail">Jailbroken</span>
                {% else %}
                <span class="badge pass">Safe</span>
                {% endif %}
            </div>
            <div class="test-body">
                <div class="prompt-section">
                    <div class="prompt-label">System Prompt</div>
                    <div class="prompt-content">{{ result.system_prompt }}</div>
                </div>
                <div class="prompt-section">
                    <div class="prompt-label">User Prompt</div>
                    <div class="prompt-content">{{ result.user_prompt }}</div>
                </div>
                <div class="prompt-section">
                    <div class="prompt-label">Expected Behavior</div>
                    <div class="prompt-content">{{ result.expectation }}</div>
                </div>
                <div class="prompt-section">
                    <div class="prompt-label">Model Response</div>
                    <div class="prompt-content response {% if result.jailbroken %}jailbroken{% else %}safe{% endif %}">{{ result.target_response or 'N/A' }}</div>
                </div>
                <div class="prompt-section">
                    <div class="prompt-label">Guard Verdict: {{ result.verdict or 'N/A' }}</div>
                    <div class="prompt-content">{{ result.guard_raw or 'N/A' }}</div>
                </div>
                {% if result.error %}
                <div class="prompt-section">
                    <div class="prompt-label">Error</div>
                    <div class="prompt-content" style="color: var(--danger);">{{ result.error }}</div>
                </div>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""


class HTMLReporter(Reporter):
    """Generate HTML format reports."""

    def __init__(self, template: str | None = None) -> None:
        """
        Initialize the HTML reporter.

        Args:
            template: Custom Jinja2 template string (optional).
        """
        self.template = Template(template or DEFAULT_TEMPLATE)

    def generate(self, report: TestReport, output_path: Path) -> Path:
        """
        Generate an HTML report file.

        Args:
            report: The test report data.
            output_path: Path to write the report to.

        Returns:
            Path to the generated report file.
        """
        output_path = output_path.with_suffix(".html")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = report.to_dict()
        html = self.template.render(**data)

        with output_path.open("w", encoding="utf-8") as f:
            f.write(html)

        return output_path
