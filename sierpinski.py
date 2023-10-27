from manim import *

class Sierpinski(Scene):

    plays = {}
    centers = {}
    color = RED_C
    font_size = 50
    max_depth = 6
    upside_down = -1 # +1 or -1

    def construct(self):
        text = Text("Sierpinski-Triangle", font_size=32, weight=ULTRALIGHT).move_to([4, self.upside_down * 3, 0])
        self.add(text)

        p1 = [0, self.upside_down * (4 * 3**0.5 - 3.5), 0]
        p2 = [-4, -self.upside_down * 3.5, 0]
        p3 = [4, -self.upside_down * 3.5, 0]
        triangle = Polygon(p1, p2, p3, color=self.color, fill_opacity=1, stroke_width=0.5)
        self.play(Create(triangle))
        
        self.recursion(triangle)
        for play in self.plays.values():
            if (type(play) is list):
                self.play(*play)
            else:
                self.play(play)
        
        text = Text("Text", font_size=self.font_size, weight=ULTRALIGHT)
        i = 1
        for depth_arrays in self.centers.values():
            if (type(depth_arrays) is list):
                for center_array in depth_arrays:
                    self.add(text.copy().scale(i).move_to(center_array))
            i = i / 2
        self.wait()


    def recursion(self, triangle, depth = 0):
        if depth > self.max_depth:
            return
        p1, p2, p3 = triangle.get_vertices()

        m1x = ( p2[0] + p1[0] ) / 2
        m1y = ( p2[1] + p1[1] ) / 2
        m2x = ( p3[0] + p2[0] ) / 2
        m2y = ( p3[1] + p2[1] ) / 2
        m3x = ( p1[0] + p3[0] ) / 2
        m3y = ( p1[1] + p3[1] ) / 2

        m1 = [m1x, m1y, 0]
        m2 = [m2x, m2y, 0]
        m3 = [m3x, m3y, 0]

        t1_new = Polygon(p1, m1, m3, color=self.color, fill_opacity=1, stroke_width=0.5)
        t2_new = Polygon(p2, m1, m2, color=self.color, fill_opacity=1, stroke_width=0.5)
        t3_new = Polygon(p3, m2, m3, color=self.color, fill_opacity=1, stroke_width=0.5)
        group = Group(t1_new, t2_new, t3_new)

        if (depth not in self.plays):
            self.plays[depth] = []
        self.plays[depth].append(FadeTransform(triangle, group))

        if (depth not in self.centers):
            self.centers[depth] = []
        self.centers[depth].append(center_of_mass([m1, m2, m3]))

        self.recursion(t1_new, depth + 1)
        self.recursion(t2_new, depth + 1)
        self.recursion(t3_new, depth + 1)