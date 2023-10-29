from manim import *
from colorsys import hsv_to_rgb

class Lorenz(ThreeDScene):

    rho = 28
    sigma = 10
    beta = 8/3
    x = 2
    y = 1
    z = 1
    dt = 0.01

    def construct(self):
        title = Title(
            "Lorenz Attractor",
            font_size=40,
            include_underline=False,
        ).move_to([-5,3,0]).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES, frame_center=[0,0,3])
        axes = ThreeDAxes(x_range=(-30, 30, 10), y_range=(-30, 30, 10), z_range=(0, 60, 10))
        self.add(axes)

        point = [self.x, self.y, self.z]
        self.curve = VMobject()
        self.curve.add(Line(point, point))
        def get_curve():
            last_line = self.curve[-1]
            self.step()
            new_line = Line(last_line.get_end(),[self.x/10,self.y/10,self.z/10], color=self.get_color(), stroke_width=2)
            self.curve.add(new_line)

            return self.curve
        
        self.add(always_redraw(get_curve))
        self.begin_ambient_camera_rotation(rate=0.8)
        self.wait(60)        

    def step(self):
        dx = self.sigma * (self.y - self.x)
        self.x += self.dt * dx
        dy = self.x * (self.rho -self.z) - self.y
        self.y += self.dt * dy
        dz = self.x * self.y - self.beta * self.z
        self.z += self.dt * dz

    def get_color(self):
        x_shift = self.x + 30
        y_shift = self.y + 30
        z_shift = self.z
        rgb = hsv_to_rgb((x_shift + y_shift) / 80, 0.8, 1)
        return rgb_to_color(rgb) 
    
        

