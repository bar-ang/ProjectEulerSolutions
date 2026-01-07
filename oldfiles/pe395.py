from project_euler import Measure, Progress, validation, solution
from PIL import Image, ImageDraw
import numpy as np
from itertools import product

def rot_matrix(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

def ortho(vec):
    return np.array([vec[1], -vec[0]])

def conv_mat(alpha):
    return np.eye(2) + np.array([[0, 1],[-1, 0]]) * (np.tan(alpha)+0.5)

def draw_vec(draw, pos, base, color="green"):
    draw.line((pos[0], pos[1], pos[0]+base[0], pos[1]+base[1]), fill=color, width=4)

def mk_r_mat(alpha):   
    return np.sin(alpha)*rot_matrix(alpha-np.pi/2)
    
def mk_l_mat(alpha):
    return np.cos(alpha)*rot_matrix(alpha)

def mk_l_minor(alpha):
    return (np.tan(alpha)/2)
    
def mk_r_minor(alpha):
    return 1/(2*np.tan(alpha))

def make_mat_from_path(alpha, path, repeat):
    m = np.eye(2)
    dir = np.eye(2)
    for lr in path:
        if lr.upper() == "R":
            m += (dir @ mk_r_mat(alpha)) * (mk_r_minor(alpha) + 1)
            dir @= mk_r_mat(alpha)
        elif lr.upper() == "L":
            m += (dir @ mk_l_mat(alpha)) * (mk_l_minor(alpha) + 1)
            dir @= mk_l_mat(alpha)

    if repeat:
        m -= np.eye(2)
        m @= np.linalg.inv(np.eye(2) - dir)
        m += np.eye(2)
    
    return m

count = 0
gdepth = 50
def draw_pythagorian_tree(draw, pos, base, depth, alpha, draw_squares=True, referrer=0):
    global count
    global gdepth
    if depth <= 0:
        return
    if np.linalg.norm(base) < 0.9:
        count += 2 ** depth
        return
    count += 1
    if count % 92131 == 11111:
        print(f"{count}/{2**gdepth} ({round(100*count/(2**gdepth),2)}%)")

    l_mat = mk_l_mat(alpha)
    r_mat = mk_r_mat(alpha)
    
    r_small = mk_r_minor(alpha) * r_mat
    l_small = mk_l_minor(alpha) * l_mat

    
    if draw_squares:
        points = [
            pos - ortho(base)/2,
            pos + ortho(base)/2,
            pos + ortho(base)/2 + base,
            pos - ortho(base)/2 + base,
        ]
        points = [tuple(p) for p in points]
        draw.polygon(points, fill="pink")

    draw_vec(draw, pos, base, color=(255, 255, 0))
    draw_vec(draw, pos + base, r_small @ base, color=(0, 30, 160))
    draw_vec(draw, pos + base, l_small @ base, color=(0, 30, 160))

    next_pos_r = pos + base + r_small @ base
    next_pos_l = pos + base + l_small @ base

    draw_pythagorian_tree(
            draw, next_pos_r, r_mat @ base,
            alpha=alpha, depth=depth-1, draw_squares=draw_squares, referrer=1
    )

    draw_pythagorian_tree(
            draw, next_pos_l, l_mat @ base,
            alpha=alpha, depth=depth-1, draw_squares=draw_squares, referrer=2
    )


def draw_path(draw, alpha, path, pos, base, repeat=False, color="red"):
    m = make_mat_from_path(alpha, path, repeat=False)
    draw_vec(draw, pos, m @ base, color)
    print(f"path {path} (len: {len(path)})") # produces matrix:\n{m}")
    if repeat:
        m = make_mat_from_path(alpha, path, repeat=True)
        draw_vec(draw, pos, m @ base, "orange")
        print(f"path {path} (len: {len(path)})") # produces matrix:\n{m}")

 
def all_paths_of_len(len):
    return [''.join(p) for p in product('RL', repeat=len)]

def max_path(paths, val, alpha, base=np.array([0, 1]), rotation=np.eye(2)):
    return max(paths, key=lambda path: val((make_mat_from_path(alpha, path, repeat=False) @ rot_matrix(rotation)) @ base))
        

def make_path_heuristic(order, val, alpha, init="", threshold=10**-19):
    path = init
    scale = 1
    rotation = 0
    while scale > threshold:
        maxpath = max_path(all_paths_of_len(order), val, alpha, rotation=rotation)
        path += maxpath
        for lr in maxpath:
            if lr == "R":
                scale *= np.sin(alpha)
                rotation += alpha - np.pi/2
            else:
                scale *= np.cos(alpha)
                rotation += alpha
    return path


#@validation
def validate():
    alpha = np.arctan(4.0/3)
    # Create a black background image
    width, height = 2200, 1500
    img = Image.new("RGB", (width, height), "black")

    # Draw a white line
    draw = ImageDraw.Draw(img)
    base = np.array([0, -height/6])
    pos = np.array([width/2, 7*height/8])

    PATHS = []

    for i in range(1, 8):
        PATHS.append(make_path_heuristic(i, lambda v: v[1], alpha))
        PATHS.append(make_path_heuristic(i, lambda v: -v[1], alpha))
        PATHS.append(make_path_heuristic(i, lambda v: v[0], alpha))
        PATHS.append(make_path_heuristic(i, lambda v: -v[0], alpha))
    
    draw_pythagorian_tree(
        draw, pos, base,
        depth=gdepth, draw_squares=False, alpha=alpha
    )
    
    for path in PATHS[:-4]:
        draw_path(draw, alpha, path, pos, base)
    for path in PATHS[-4:]:
        draw_path(draw, alpha, path, pos, base, color="green")
        

    img.save("pyth_tree.jpg", "JPEG")

    

@solution
def solve():
    base = np.array([0, 1])
    alpha = 0.643501108793284386802809228717323 # arccos(0.6)
    order = 7

    top = make_mat_from_path(alpha, make_path_heuristic(order, lambda v: v[1], alpha), repeat=False) @ base
    right = make_mat_from_path(alpha, make_path_heuristic(order, lambda v: v[0], alpha), repeat=False) @ base
    left = make_mat_from_path(alpha, make_path_heuristic(order, lambda v: -v[0], alpha), repeat=False) @ base
    down = make_mat_from_path(alpha, make_path_heuristic(order, lambda v: -v[1], alpha), repeat=False) @ base

    return round((top-down)[1] * (right - left)[0], 10)
