from enum import Enum, auto
from project_euler import Measure, Progress, validation, solution
from PIL import Image, ImageDraw


class Desc(Enum):
    BLACK = auto()
    WHITE = auto()
    SPLIT = auto()
    DEBUG = auto()  # no binary encoding, debugging use only

    def __str__(self):
        return {
            Desc.BLACK: "B",
            Desc.WHITE: "W",
            Desc.SPLIT: "X",
            Desc.DEBUG: "D",
        }[self]

    __repr__ = __str__


B = Desc.BLACK
W = Desc.WHITE
D = Desc.DEBUG
X = Desc.SPLIT

#def binary_to_desc(encoded):
#    descs = []
#    pos = 0
#    while pos < len(encoded):
#        if encoded[pos] == "0":
#            descs.append(Desc.SPLIT)
#            pos += 1
#        else:
#            descs.append(Desc.BLACK if encoded[pos + 1] == "0" else Desc.WHITE)
#            pos += 2
#    return descs


LEAF_COLORS = {
    Desc.BLACK: (0, 0, 0),
    Desc.WHITE: (255, 255, 255),
    Desc.DEBUG: (0, 0, 255),  # blue, for debugging only - not part of the encoding
}


def draw_quadtree(descs, n, pixel_size=10, shade_by_depth=False):
    size = 2 ** (n+1)
    assert size <= 1024, f"size too big: {size}"
    img = Image.new("RGB", (size, size), LEAF_COLORS[Desc.WHITE])
    draw = ImageDraw.Draw(img)

    pos = 0

    def read_desc():
        nonlocal pos
        desc = descs[pos]
        pos += 1
        return desc

    def tint_red(color, depth):
        alpha = min(0.7, depth * 0.12)
        r, g, b = color
        return (
            int(r * (1 - alpha) + 255 * alpha),
            int(g * (1 - alpha)),
            int(b * (1 - alpha)),
        )

    def decode_region(x, y, s, depth=0):
        assert s > 0
        desc = read_desc()
        if desc == Desc.SPLIT:
            half = s // 2
            decode_region(x, y, half, depth + 1)
            decode_region(x + half, y, half, depth + 1)
            decode_region(x, y + half, half, depth + 1)
            decode_region(x + half, y + half, half, depth + 1)
        else:
            color = tint_red(LEAF_COLORS[desc], depth) if shade_by_depth else LEAF_COLORS[desc]
            draw.rectangle([x, y, x + s - 1, y + s - 1], fill=color)

    decode_region(0, 0, size)

    if pixel_size != 1:
        img = img.resize((size * pixel_size, size * pixel_size), Image.NEAREST)

    return img

circle = lambda x, y, k: (x-2**(k-1))**2 + (y-2**(k-1))**2 <= 4 ** (k-1)
infi = lambda x, y, k: ((1.5*x-1)**2+y**2) * ((1.5*x+1)**2+y**2) <= 1


def encode_area(area, n, *, x=1, y=1, k=1):
    nxt = [
        (-1,  0),
        ( 0,  0),
        (-1, -1),
        ( 0, -1)
    ]

    res = [X]
    if n == k:
        if n== 2:
            import pdb; pdb.set_trace()
        for t in nxt:
            ox, oy = t
            res.append(B if area(x+ox, y+oy, k) else W)

    else:
        for t in nxt:
            ox, oy = t
            res += encode_area(area, n, x=2*(x+ox)+1, y=2*(y+oy)+1, k=k+1)

    if res == [X, B, B, B, B]:
        res = [B]

    if res == [X, W, W, W, W]:
        res = [W]

    return res

def _encode_area(area, n, *, x=1, y=1, k=1):
    if n < k:
        if area(x, y, k):
            return [B]
        else:
            return [W]

    nxt = [
        (-1,  0),
        ( 0,  0),
        (-1, -1),
        ( 0, -1)
    ]


    res = [X]

    for t in nxt:
        ox, oy = t
        res += encode_area(area, n, x=2*x+ox, y=2*y+oy, k=k+1)
        #if area(x+t[0], y+t[1], k) == area(x, y, k) and area(x, y+t[1], k) == area(x, y, k) and area(x+t[0], y, k) == area(x, y, k):
        #    color = B if area(x+t[0], y+t[1], k) else W
        #    res.append(color)
        #else:
        #    res += encode_area(area, n, x=2*x+t[0], y=2*y+t[1], k=k+1)

    #if res == [X, B, B, B, B]:
    #    res = [B]

    #if res == [X, W, W, W, W]:
    #    res = [W]

    return res


@validation
def validate():
    def contains(lst, sub):
        n, m = len(lst), len(sub)
        return any(lst[i:i+m] == sub for i in range(n - m + 1))

    n1 = encode_area(circle, 1)
    assert n1 == [X, B, B, W, B], n1
    n2 = encode_area(circle, 2)
    assert n2 == [X, X, W, B, B, B, B, X, W, B, W, W, X, B, B, B, W], n2

    for n in range(3, 9):
        uc = encode_area(circle, n)
        assert not contains(uc, [X, B, B, B, B]) and not contains(uc, [X, W, W, W, W])



    n = 2
    pxsize = 100//n
    ucn = encode_area(circle, n)
    print(ucn)
    t = draw_quadtree(ucn, n, pixel_size=pxsize, shade_by_depth=True)
    print(t.size)
    assert t.size[0] == t.size[1] == 2 ** (n+1) * pxsize
    t.show()



@solution
def solve():
    n = 23
    with Measure("encoding"):
        uc = encode_area(circle, n)
    print(uc[:200])
    with Measure("calc length"):
        l = sum([1 if c == Desc.SPLIT else 2 for c in uc])
    return l

