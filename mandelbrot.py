from manim import *
from math import log
import time
from numba import njit

cols = config.frame_size[0]
rows = config.frame_size[1]
ratio = cols / rows

""" z = 10000000
center_x = -1.308109
center_y = -0.062998 
max_iter = 10000 """
""" z = 300000
center_x = -0.51012
center_y = -0.522997 
max_iter = 1000 """
""" z = 10000
center_x = -0.34853774148008254
center_y = -0.6065922085831237
max_iter = 20000 """
min_zoom = 1
max_zoom = 10000
seconds = 1
frame_count = int(seconds * config.frame_rate)
center_x = -0.34853774148008254
center_y = -0.6065922085831237

class Mandelbrot(Scene):

    def construct(self):
        start_time = time.time()
        
        i = 0
        max_iter = 1000
        for zoom in np.logspace(start=log(min_zoom),stop=log(max_zoom, 10),num=frame_count, endpoint=False):
            max_iter = max_iter * 20 ** ((1/config.frame_rate) / seconds)
            start_loop_time = time.time() 
            inv_zoom = 1 / zoom
            inv_zoom_ratio = inv_zoom * ratio
            re_min = center_x - inv_zoom_ratio
            re_max = center_x + inv_zoom_ratio
            im_min = center_y - inv_zoom
            im_max = center_y + inv_zoom
            pixels_to_render = np.uint8(iterate_rows(re_min, re_max, im_min, im_max, max_iter))
            image = ImageMobject(pixels_to_render)
            image.height = config.frame_height
            image.width  = config.frame_width
            self.add(image)
            self.wait(1/config.frame_rate)

            zoom_string = ("zoom: " + str(zoom)).ljust(27)
            now = time.time()
            loop_string = ('loop time: ' + str(now - start_loop_time)).ljust(31)
            total_string = ('total time: ' + str(now - start_time)).ljust(31)
            frame_string = ('frame: ' + str(i) + '/' + str(frame_count)).ljust(15)
            max_iter_string = ('max_iter: ' + str(max_iter)).ljust(31)
            print(frame_string + zoom_string + loop_string + total_string + max_iter_string)
            i += 1

        """ ax = Axes(
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
        self.add(ax, dot, label) """  

        title = Title(
            "Mandelbrot Set",
            include_underline=False,
            font_size=40,
        ).move_to([-5,3,0])
        
        self.add(title)

@njit #(parallel=True)
def iterate_rows(re_min, re_max, im_min, im_max, max_iter):
    pixels = []
    for y in range(rows):
        pixels.append(iterate_cols(re_min, re_max, im_min, im_max, y, max_iter))
    return pixels

@njit #(parallel=True)
def iterate_cols(re_min, re_max, im_min, im_max, y, max_iter):
    max_betrag_2 = 4
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
    g = round((iter * 3)/max_iter * 255) % 255
    b = round((iter * 6)/max_iter * 255) % 255
    return [r, g, b, 255]