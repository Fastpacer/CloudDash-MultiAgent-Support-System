import time


def start_trace():

    return time.time()


def end_trace(
    start_time: float,
):

    duration = (
        time.time()
        - start_time
    )

    return round(duration, 4)