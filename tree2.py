from manim import *

class Tree2(Scene):
    angle = PI/5
    run_time = 0.1
    width = 4
    creations = {}
    colors = [GREEN_B, GREEN_C, GREEN_D, GREEN_E, '#5C4827', '#9F5927', DARK_BROWN]

    def construct(self):
        text = Text("Tree2", font_size=48, weight=ULTRALIGHT).move_to([5,2.4,0])
        self.add(text)
    
        start = [0,-4,0]
        end   = [0,-.5,0]
        self.play(Create(Line(start,end).set_stroke(color=self.colors[len(self.colors) - 1])).set_run_time(self.run_time))
        self.drawTwig(start, end, 6, '', self.run_time, self.width)
        
        # reorder Animations
        new_creations = {}
        for k in sorted(self.creations, key=len):
            new_creations[k] = self.creations[k]

        for key, value in new_creations.items():
            self.play(value)
    
    def drawTwig(self, start, end, iterations, key, run_time, width):
        if (iterations > 0):
            line = Line(start, end)
            new_line_length = line.get_length() / 2
            run_time = run_time / 2
            width = width / 1.25

            end_1 = self.new_end(end, line.get_angle() - 3 * self.angle, new_line_length)
            self.creations[key + 'a'] = self.creation(end, end_1, iterations, width, run_time, key + 'a')

            end_2 = self.new_end(end, line.get_angle() - self.angle, new_line_length)
            self.creations[key + 'b'] = self.creation(end, end_2, iterations, width, run_time, key + 'b')

            end_3 = self.new_end(end, line.get_angle() + self.angle, new_line_length)
            self.creations[key + 'c'] = self.creation(end, end_3, iterations, width, run_time, key + 'c')

            end_4 = self.new_end(end, line.get_angle() + 3 * self.angle, new_line_length)
            self.creations[key + 'd'] = self.creation(end, end_4, iterations, width, run_time, key + 'd')

    def new_end(self, end_point, angle, new_line_length):
        return [
                    end_point[0] + np.cos(angle) * new_line_length,
                    end_point[1] + np.sin(angle) * new_line_length,
                    0
                ]
    
    def creation(self, old_end_point, new_end_point, iterations, width, run_time, key):
        line = Line(old_end_point,new_end_point).set_stroke(color=self.colors[iterations], width=width)
        create = Create(line).set_run_time(run_time)
        self.drawTwig(line.get_start(), line.get_end(), iterations - 1, key, run_time, width)
        return create