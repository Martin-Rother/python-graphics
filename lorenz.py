from manim import *
from colorsys import hsv_to_rgb

class Lorenz(ThreeDScene):

    rho = 28
    sigma = 10
    beta = 8/3
    points = [
        [2, 1, 1],
        [2.01, 1, 1],
        [2.02, 1, 1]
    ]
    curves = []
    dots = []
    dt = 0.01

    def construct(self):
        title = Title(
            "Lorenz Attractor",
            font_size=40,
            include_underline=False,
        ).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES, frame_center=[0,0,3])
        axes = ThreeDAxes(x_range=(-30, 30, 10), y_range=(-30, 30, 10), z_range=(0, 60, 10))
        self.add(axes)

        texts = VGroup()
        for i in range(len(self.points)):
            text = Text(str(self.points[i]).replace('[', '(').replace(']', ')'), font_size=24)
            texts.add(text)
            self.add_fixed_in_frame_mobjects(text)
            self.curves.append(VMobject())
            self.curves[i].add(Line(self.points[i], self.points[i]))
            self.dots.append(VMobject())
            self.dots[i].add(Dot3D(self.points[i]))

        texts.arrange(DOWN).next_to(title, DOWN)

        def get_curves():
            points_scale = []
            for i in range(len(self.points)):
                last_line = self.curves[i][-1]
                self.step(i)
                points_scale.append([
                                self.points[i][0]/10,
                                self.points[i][1]/10,
                                self.points[i][2]/10
                            ])
                color = self.get_color(i)
                new_line = Line(last_line.get_end(),
                                points_scale[i],
                                color=color,
                                stroke_width=2)
                self.curves[i].add(new_line)
                self.dots[i].color = color
                self.dots[i].add_updater(lambda x, i=i: x.move_to(points_scale[i]))

            group = VGroup()
            group.add(*self.curves)
            return group
        
        self.add(*self.dots)
        self.add(always_redraw(get_curves))

        self.begin_ambient_camera_rotation(rate=0.5)
        self.wait(60)        

    def step(self, point_index):
        dx = self.sigma * (self.points[point_index][1] - self.points[point_index][0])
        self.points[point_index][0] += self.dt * dx
        dy = self.points[point_index][0] * (self.rho - self.points[point_index][2]) - self.points[point_index][1]
        self.points[point_index][1] += self.dt * dy
        dz = self.points[point_index][0] * self.points[point_index][1] - self.beta * self.points[point_index][2]
        self.points[point_index][2] += self.dt * dz

    def get_color(self, point_index):
        if len(self.points) == 1:
            x_shift = self.points[0][0] + 30
            y_shift = self.points[0][1] + 30
            rgb = hsv_to_rgb((x_shift + y_shift) / 80, 0.8, 1)
        else:
            x_shift = self.points[point_index][0] + 30
            y_shift = self.points[point_index][1] + 30
            rgb = hsv_to_rgb(point_index * 0.3, 0.8, 1)
        return rgb_to_color(rgb)
        

