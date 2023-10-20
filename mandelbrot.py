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

        title = Title(
            "Mandelbrot Set",
            include_underline=False,
            font_size=40,
        ).move_to([-5,3,0])

        grid = Axes(
            x_range=[-1 * ratio, 1 * ratio, 0.5],
            y_range=[-1, 1, 0.5],
            x_length=8 * ratio,
            y_length=8,
            axis_config={
                "include_numbers": True
            },
            tips=False,
        )
            
        zoom = 1
        center_x = 0
        center_y = 0
        delta_y = 1
        delta_x = 1
        re_min = (( center_x ) - delta_x / zoom) * ratio
        re_max = (( center_x ) + delta_x / zoom) * ratio
        im_min = (( center_y ) - delta_y / zoom)
        im_max = (( center_y ) + delta_y / zoom)

        print("re_min: ", re_min)
        print("re_max: ", re_max)
        print("im_min: ", im_min)
        print("im_max: ", im_max)

        pixels_to_render = np.uint8(iterate_rows(re_min, re_max, im_min, im_max, rows))
        
        image = ImageMobject(pixels_to_render)
        image.height = height
        image.width  = width
        self.add(image, title, grid)

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
    max_iter = 1000
    c_im = im_min + (im_max-im_min)*y/rows
    row = []
    for x in range(cols):
        c_re = re_min + (re_max-re_min)*x/cols
        iter = julia(c_re, c_im, c_re, c_im, max_betrag_2, max_iter)
        if (sqrt(c_re**2 + c_im**2) < 0.02 or sqrt((c_re+1)**2 + c_im**2) < 0.02):
            color = [255, 255, 255, 255]
        else:
            color = color_picker(iter, max_iter)
        row.append(color)
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
        
    #if betrag_2 == 0 or log(betrag_2) / log(4) <= 0 :
    return max_iter - remain_iter
    #else:
    #    return max_iter - remain_iter - log(log(betrag_2) / log(4)) / log(2)
    
@njit #(parallel=True)
def color_picker(iter, max_iter):
    r = round(iter/max_iter * 255) % 255
    g = round((iter * 2)/max_iter * 255) % 255
    b = round((iter * 3)/max_iter * 255) % 255
    return [r, g, b, 255]