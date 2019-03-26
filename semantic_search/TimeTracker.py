import time
from functools import wraps


class Logger:
    def log(self, message):
        print('[TimeTracking] {function_name:16} - total: {total_time:3.6f} s - partial: {partial_time:3.6f} s'.format(**message))


_time_tracker_global_entering_times = []
_time_tracker_global_total_times = [0]


class TimeTracker:
    def __init__(self, do_time_tracking=False, isolated=True):
        self.logger = Logger()
        self.do_time_tracking = do_time_tracking

        if isolated:
            self.entering_times = []
            self.total_times = [0]
        else:
            self.entering_times = _time_tracker_global_entering_times
            self.total_times = _time_tracker_global_total_times

    def _enter(self):
        self.entering_times.append(time.time())
        self.total_times.append(0)

    def _exit(self, function_name, args, kwargs):
        enter_time = self.entering_times.pop()
        inner_total_time = self.total_times.pop()

        exit_time = time.time()
        total_time = exit_time - enter_time
        partial_time = total_time - inner_total_time

        self.total_times[-1] += total_time

        self.logger.log({
            'function_name': function_name,
            'total_time': total_time,
            'partial_time': partial_time,
        })

    def __str__(self):
        return 'entering_times: {entering_times}, total_times: {total_times}'.format(
            entering_times=self.entering_times,
            total_times=self.total_times,
        )

    def time_track(self):
        def _time_track(function):
            @wraps(function)
            def wrapped(*args, **kwargs):
                self._enter()
                try:
                    result = function(*args, **kwargs)
                finally:
                    self._exit(function.__name__, args, kwargs)

                return result
            return wrapped

        return _time_track if self.do_time_tracking else lambda function: function
