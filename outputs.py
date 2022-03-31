from datetime import datetime


def time_function() -> tuple[str, ...]:
    """Shows the date and time."""
    # https://docs.python.org/3/library/time.html#time.strftime
    now = datetime.now()
    return now.strftime("%a %b %d %Y"), \
           now.strftime("%H:%M:%S")


OUTPUT_FUNCTIONS = {
    "time": time_function
}
