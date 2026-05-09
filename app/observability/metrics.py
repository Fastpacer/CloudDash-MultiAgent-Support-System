from collections import defaultdict


# ---------------------------------------------------
# In-Memory Metrics Store
# ---------------------------------------------------

metrics_store = defaultdict(int)


def increment_metric(
    metric_name: str,
):

    metrics_store[
        metric_name
    ] += 1


def get_metrics():

    return dict(metrics_store)