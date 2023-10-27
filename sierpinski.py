from manim import *

class Sierpinski(Scene):

    plays = {}

    def construct(self):
        text = Text("Sierpinski-Triangle", font_size=32, weight=ULTRALIGHT).move_to([4,3,0])
        self.add(text)

        triangle = Polygon([0, 4 * 3**0.5 - 3.5, 0], [-4, -3.5, 0], [4, -3.5, 0], color=GOLD_E, fill_opacity=1, stroke_width=0.5)
        self.play(Create(triangle))
        
        self.recursion(triangle)

        for play in self.plays.values():
            if (type(play) is list):
                self.play(*play)
            else:
                self.play(play)

    def recursion(self, triangle, depth = 0, max_depth = 6):
        if depth > max_depth:
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

        t1_neu = Polygon(p1, m1, m3, color=GOLD_E, fill_opacity=1, stroke_width=0.5)
        t2_neu = Polygon(p2, m1, m2, color=GOLD_E, fill_opacity=1, stroke_width=0.5)
        t3_neu = Polygon(p3, m2, m3, color=GOLD_E, fill_opacity=1, stroke_width=0.5)
        group = Group(t1_neu, t2_neu, t3_neu)

        if (depth in self.plays):
            self.plays[depth].append(FadeTransform(triangle, group))
        else:
            self.plays[depth] = []
            self.plays[depth].append(FadeTransform(triangle, group))

        self.recursion(t1_neu, depth + 1)
        self.recursion(t2_neu, depth + 1)
        self.recursion(t3_neu, depth + 1)