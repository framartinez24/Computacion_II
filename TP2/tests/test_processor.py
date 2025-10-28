
from processor.performance import analyze_performance

def test_performance_basic():
    perf = analyze_performance("https://example.com", links_count=2, images_count=1)
    assert "load_time_ms" in perf and perf["total_size_kb"] >= 0 and perf["num_requests"] >= 1
