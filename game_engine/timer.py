"""
Handles game timer logic.
"""

import time

def start_timer():
    return time.time()

def stop_timer():
    return time.time()

def get_time_difference(start, end):
    return round(end - start, 2)

