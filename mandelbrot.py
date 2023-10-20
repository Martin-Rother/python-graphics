from manim import *
from math import log, ceil, sqrt
import time
from numba import jit, njit
from numba.experimental import jitclass
from numba.typed import List

ratio_x = 16
ratio_y = 9
ratio = ratio_x / ratio_y
rows = config.frame_size[1]
cols = ceil(rows * ratio)
height = config.frame_height
width = height * ratio

#@jitclass
class Mandelbrot(Scene):

    def construct(self):
        global rows
        global height
        global width
        global ratio

        start_time = time.time()
            
        zoom = 10000000
        center_x = -1.308109
        center_y = -0.062998
        inv_zoom = 1 / zoom
        inv_zoom_ratio = inv_zoom * ratio
        re_min = center_x - inv_zoom_ratio
        re_max = center_x + inv_zoom_ratio
        im_min = center_y - inv_zoom
        im_max = center_y + inv_zoom

        print("re_min: ", re_min)
        print("re_max: ", re_max)
        print("im_min: ", im_min)
        print("im_max: ", im_max)

        ax = Axes(
            x_range=[re_min, re_max, inv_zoom],
            y_range=[im_min, im_max, inv_zoom],
            x_length=8 * ratio,
            y_length=8,
            axis_config={
                #"include_numbers": True,
            },
            tips=False,
        )
        dot = Dot(ax.coords_to_point(center_x, center_y), color=WHITE)
        label = Text('(' + str(center_x) + ',' + str(center_y) + ')').scale(.5).next_to(dot)

        title = Title(
            "Mandelbrot Set",
            include_underline=False,
            font_size=40,
        ).move_to([-5,3,0])

        pixels_to_render = np.uint8(iterate_rows(re_min, re_max, im_min, im_max, rows))
        
        image = ImageMobject(pixels_to_render)
        image.height = height
        image.width  = width
        self.add(image, title, ax, dot, label)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print('Execution time:', elapsed_time, 'seconds')

@njit #(parallel=True)
def iterate_rows(re_min, re_max, im_min, im_max, rows):
    pixels = List()
    for y in range(rows):
        pixels.append(iterate_cols(re_min, re_max, im_min, im_max, y))
    return pixels

@njit #(parallel=True)
def iterate_cols(re_min, re_max, im_min, im_max, y):
    global ratio
    global rows
    global cols
    
    max_betrag_2 = 4
    max_iter = 2000
    c_im = im_min + (im_max-im_min)*y/rows
    row = []
    for x in range(cols):
        c_re = re_min + (re_max-re_min)*x/cols
        iter = julia(c_re, c_im, c_re, c_im, max_betrag_2, max_iter)
        row.append(color_picker(iter, max_iter))
    return row

@njit #(parallel=True)
def julia(x, y, xadd, yadd, max_betrag_2, max_iter):
    remain_iter = max_iter
    xx = x*x
    yy = y*y
    xy = x*y
    betrag_2 = xx + yy

    while (betrag_2 <= max_betrag_2) and (remain_iter > 0):
        remain_iter = remain_iter - 1
        x  = xx - yy + xadd
        y  = xy + xy + yadd
        xx = x*x
        yy = y*y
        xy = x*y
        betrag_2 = xx + yy
        
    return max_iter - remain_iter
    
@njit #(parallel=True)
def color_picker(iter, max_iter):
    r = round(iter/max_iter * 255) % 255
    g = round((iter * 2)/max_iter * 255) % 255
    b = round((iter * 3)/max_iter * 255) % 255
    return [r, g, b, 255]