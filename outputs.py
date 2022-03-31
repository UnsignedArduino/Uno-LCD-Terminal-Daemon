from datetime import datetime

import psutil


def time_function() -> tuple[str, ...]:
    """Shows the date and time."""
    # https://docs.python.org/3/library/time.html#time.strftime
    now = datetime.now()
    return now.strftime("%a %b %d %Y"), \
           now.strftime("%H:%M:%S")


def cpu_function() -> tuple[str, ...]:
    """Shows the CPU utilization"""
    percent = psutil.cpu_percent()
    times = psutil.cpu_times()
    all_times = (
        f"U: {times.user:.3f}",
        f"S: {times.system:.3f}",
        f"I: {times.idle:.3f}"
    )
    try:
        cpu_function.curr_stat_time -= 1
        if cpu_function.curr_stat_time == 0:
            cpu_function.curr_stat_time = 5
            cpu_function.stat_cycle += 1
            if cpu_function.stat_cycle > len(all_times) - 1:
                cpu_function.stat_cycle = 0
    except AttributeError:
        cpu_function.curr_stat_time = 5
        cpu_function.stat_cycle = 0
    return f"CPU: {percent}%", \
           all_times[cpu_function.stat_cycle]


OUTPUT_FUNCTIONS = {
    "time": time_function,
    "cpu": cpu_function
}
