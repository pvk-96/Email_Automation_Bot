import threading
import schedule
import time
from datetime import datetime

class Scheduler:
    def __init__(self):
        self.jobs = []
        self.running = False

    def schedule_send(self, send_time, callback, *args, **kwargs):
        # send_time: datetime object
        def job():
            callback(*args, **kwargs)
        delay = (send_time - datetime.now()).total_seconds()
        if delay <= 0:
            job()
        else:
            timer = threading.Timer(delay, job)
            timer.start()
            self.jobs.append(timer)

    def run_pending(self):
        schedule.run_pending() 