import time
import random
import itertools
try:
    import pyperclip
except ModuleNotFoundError:
    pyperclip = None


def export_binary_tree_png(root, path, *, left="left", right="right", value=str,
                           node_radius=18, x_spacing=56, y_spacing=72,
                           margin=32, background="white", node_fill="#f5f5f5",
                           node_outline="black", edge_fill="black",
                           text_fill="black"):
    """
    Export a binary tree to a PNG file.

    By default this expects each node to have left/right attributes. If your
    nodes use different names, pass left="_left", right="_right", etc. Accessors
    can also be callables. The value argument can be a callable or an attribute
    name.
    """
    from PIL import Image, ImageDraw, ImageFont

    if root is None:
        raise ValueError("cannot export an empty tree")

    def read(node, accessor):
        if callable(accessor):
            return accessor(node)
        return getattr(node, accessor)

    def label(node):
        if callable(value):
            return str(value(node))
        return str(getattr(node, value))

    positions = {}
    nodes = []
    next_x = 0

    def place(node, depth=0):
        nonlocal next_x
        if node is None:
            return

        lchild = read(node, left)
        rchild = read(node, right)
        place(lchild, depth + 1)

        nodes.append(node)
        positions[id(node)] = (next_x, depth)
        next_x += 1

        place(rchild, depth + 1)

    place(root)

    max_depth = max(depth for _, depth in positions.values())
    width = max(1, next_x - 1) * x_spacing + margin * 2 + node_radius * 2
    height = max_depth * y_spacing + margin * 2 + node_radius * 2
    img = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    def pixel_pos(node):
        x, y = positions[id(node)]
        return margin + node_radius + x * x_spacing, margin + node_radius + y * y_spacing

    for node in nodes:
        x1, y1 = pixel_pos(node)
        for child in (read(node, left), read(node, right)):
            if child is not None:
                x2, y2 = pixel_pos(child)
                draw.line((x1, y1, x2, y2), fill=edge_fill, width=2)

    for node in nodes:
        x, y = pixel_pos(node)
        draw.ellipse(
            (x - node_radius, y - node_radius, x + node_radius, y + node_radius),
            fill=node_fill,
            outline=node_outline,
            width=2,
        )

        text = label(node)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x - tw / 2, y - th / 2), text, fill=text_fill, font=font)

    img.save(path, "PNG")
    return path


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
    def almost_equals(expected, func, *, precision, **kwargs):
        expected = round(expected, precision)
        calc = round(func(**kwargs), precision)
        str_args = ",".join([f"{k}={v}" for k, v in kwargs.items()])
        func_str = f"{func.__name__}({str_args})={calc}"
        assert calc == expected, f"{func_str}, not {expected}"
        #print(f"{func_str} as expected!")

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
        
