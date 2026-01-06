import time
import random
import itertools
import pyperclip

class Progress:
    def __init__(self, iterable, op_name="iterating", *, announce_every=7, announce_every_seconds=43, on_demand_only=False, bar_len=25, iterable_len=None, measure_window=1000, noise=True):
        self._iterable = iterable
        self._len = iterable_len
        self._op_name = op_name
        if noise and announce_every:
            announce_every += random.random()
        self._announce_every = float(announce_every) / 100
        self._announce_every_seconds = announce_every_seconds
        self._on_demand_only = on_demand_only
        self._bar_len = bar_len

    def in_case(condition, iterable, *args, **kwargs):
        if condition:
            return Progress(iterable, *args, **kwargs)
        else:
            return enumerate(iterable)
    
    def bar(self):
        i, _ = self._i
        fill = int(float(self._bar_len * i) / self._len)
        if self._bar_len >= fill:
            return "[%s%s]" % ("#"*fill, " "*(self._bar_len - fill))
        else:
           return "[%s]" % ">"* self._bar_len
    
    def __iter__(self):
        self._enumerator = enumerate(self._iterable)
        if self._len is None:
            self._len = len(self._iterable)
        self._i = None
        self._next_announce = 0
        self._announce_every_len = int(self._announce_every * self._len)
        self._start_time = time.time()
        self._next_announce_seconds = self._announce_every_seconds
        print("%s going to iterate over %s elements" % (self._op_name, self._len))
        if self._announce_every_len > 1:
            return self
        else:
            #print("ShowProgress '%s': cannot show progress for %s elements." % (self._op_name, self._len))
            return self._enumerator

    def elapsed_time(self):
        return time.time() - self._start_time
    
    def show_progress(self):
        i, _ = self._i
        perc = round(float(i) * 100 / self._len, 2)
        print("%s completed: %s/%s %s (%s%%)" % (self._op_name, i, self._len, self.bar(), perc))
    
    def __next__(self):
        self._i = next(self._enumerator)
        i, _ = self._i
        should_announce = False

        if not self._on_demand_only:        
            while i >= self._next_announce:
                should_announce = True
                self._next_announce += self._announce_every_len
            while self.elapsed_time() >= self._next_announce_seconds:
                should_announce = True
                self._next_announce_seconds += self._announce_every_seconds

        if should_announce:
            self.show_progress()

        return self._i

class Measure:
    def __init__(self, msg="unnamed", print_threshold_sec=0, start_print=False):
        self.msg = msg
        self.entered = None
        self.exited = None
        self.print_threshold_sec = print_threshold_sec
        self.start_print = start_print

    def start(self):
        self.entered = time.time()

    def stop(self):
        self.exited = time.time()

    def reset(self):
        self.entered = None
        self.exited = None

    @property
    def elapsed(self):
        return time.time() - self.entered

    def print(self, msg, *args, **kwargs):
        if time.time() - self.entered >= self.print_threshold_sec:
            print(msg, *args, **kwargs)

    def __enter__(self):
        if self.start_print:
            print("'%s' started" % self.msg)
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()
        if self.exited - self.entered >= self.print_threshold_sec:
            print(self.__str__())

    def __str__(self):
        if not self.entered:
            return "does not measuring"
        elif self.entered and not self.exited:
            t = round(time.time() - self.entered, 3)
            return "operation '%s' takes %s sec already." % (self.msg, t)
        else:
            t = round(self.exited - self.entered, 3)
            return "operation '%s' took %s sec." % (self.msg, t)

def str_percentage(frac, total, rounded=2):
    assert frac >= 0
    assert total > 0
    return f"{frac}/{total} ({round(frac*100/total, rounded)}%)"

def solution(func):
    with Measure("Main Calculation"):
        sol = func()

    # \033[44;1;37m = Blue Background, Bold White Text
    HEADER = "\033[44;1;37m"
    RESET = "\033[0m"

    print(f"\n{HEADER}  🏆  SOLUTION IDENTIFIED  {RESET}")
    print(f"  ➥  {sol}\n")

    return sol

def validation(func):
    count_errs = 0
    with Measure("Validation"):
        try:
            func()
        except AssertionError as e:
            ERR = "\033[1;97;41m"
            # Red Text
            TXT = "\033[91m"
            RST = "\033[0m"

            print(f"\n{ERR} ⚡ VALIDATION FAILED ⚡ {RST}")
            print(f"{TXT}▶ REASON: {RST}{str(e) or "assert failed"}")
            print(f"{TXT}━━━━━━━━━━━━━━━━━━━━━━{RST}\n")

            raise e

        # Green Background + White Bold Text
        GO = "\033[1;97;42m"
        # Green Text
        TXT = "\033[92m"
        RST = "\033[0m"

        print(f"\n{GO} ✨ VALIDATION PASSED ✨ {RST}")
        print(f"{TXT}━━━━━━━━━━━━━━━━━━━━━━{RST}\n")

class Test:
    def equals(expected, func, *args, **kwargs):
        calc = func(*args, **kwargs)
        str_args = ",".join([str(a) for a in args] + [f"{k}={v}" for k, v in kwargs.items()])
        func_str = f"{func.__name__}({str_args})={calc}"
        assert calc == expected, f"{func_str}, not {expected}"
        #print(f"{func_str} as expected!")

    def funcs_equal(f1, f2, *args, **kwargs):
        calc1 = f1(*args, **kwargs)
        calc2 = f2(*args, **kwargs)
        str_args = ",".join([str(a) for a in args] + [f"{k}={v}" for k, v in kwargs.items()])
        f1_str = f"{f1.__name__}({str_args})"
        f2_str = f"{f2.__name__}({str_args})"
        assert calc1 == calc2, f"funcs not equal: {f1_str}={calc1}, but {f2_str}={calc2}"
        #print(f"{f1_str}={f2_str}={calc1}")

    def are_the_same(f1, f2, *args, **kwargs):
        assert all([type(a) == range for a in args])
        assert all([type(a) == range for _, a in kwargs.items()])

        for tup in itertools.product(*args):
            Test.funcs_equal(f1, f2, *tup)        
        
