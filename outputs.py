from datetime import datetime

import psutil
from human_bytes import HumanBytes


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


def memory_function() -> tuple[str, ...]:
    """Shows the memory utilization"""
    mem = psutil.virtual_memory()
    percent = (mem.used / mem.total) * 100
    return f"Memory: {percent:.2f}%", \
           f"{HumanBytes.format(mem.used, label=False).strip()}/" \
           f"{HumanBytes.format(mem.total)}"


def disk_function() -> tuple[str, ...]:
    """Shows the disk IO counters"""
    io = psutil.disk_io_counters()
    return f"DR: {HumanBytes.format(io.read_bytes, precision=3)}", \
           f"DW: {HumanBytes.format(io.write_bytes, precision=3)}"


def network_function() -> tuple[str, ...]:
    """Shows the network IO counters"""
    io = psutil.net_io_counters()
    return f"NS: {HumanBytes.format(io.bytes_recv, precision=3)}", \
           f"NR: {HumanBytes.format(io.bytes_sent, precision=3)}"


OUTPUT_FUNCTIONS = {
    "time": time_function,
    "cpu": cpu_function,
    "memory": memory_function,
    "disk": disk_function,
    "network": network_function
}
