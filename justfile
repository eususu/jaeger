all:


new_metric:
    uv run python send_test_metrics.py
new_trace:
    uv run python send_test_traces.py