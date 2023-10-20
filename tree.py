from manim import *

class Tree(Scene):
    angle = PI/2
    run_time = 0.1
    width = 4
    creations = {}
    colors = [GREEN_A, GREEN_B, GREEN_C, GREEN_D, GREEN_E, '#5C4827', '#9F5927', DARK_BROWN]

    def construct(self):
        text = Text("Tree", font_size=48, weight=ULTRALIGHT).move_to([5,2.4,0])
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
            end_1 = [
                    end[0] + np.cos(line.get_angle() - self.angle) * new_line_length,
                    end[1] + np.sin(line.get_angle() - self.angle) * new_line_length,
                    0
                ]
            line_1 = Line(end,end_1).set_stroke(color=self.colors[iterations], width=width)
            create_1 = Create(line_1).set_run_time(run_time)
            self.creations[key + 'r'] = create_1

            end_2 = [
                    end[0] + np.cos(line.get_angle()) * new_line_length,
                    end[1] + np.sin(line.get_angle()) * new_line_length,
                    0
                ]
            line_2 = Line(end,end_2).set_stroke(color=self.colors[iterations], width=width)
            create_2 = Create(line_2).set_run_time(run_time)
            self.creations[key + 'm'] = create_2

            end_3 = [
                    end[0] + np.cos(line.get_angle() + self.angle) * new_line_length,
                    end[1] + np.sin(line.get_angle() + self.angle) * new_line_length,
                    0
                ]
            line_3 = Line(end,end_3).set_stroke(color=self.colors[iterations], width=width)
            create_3 = Create(line_3).set_run_time(run_time)
            self.creations[key + 'l'] = create_3

            self.drawTwig(line_1.get_start(), line_1.get_end(), iterations - 1, key + 'r', run_time, width)
            self.drawTwig(line_2.get_start(), line_2.get_end(), iterations - 1, key + 'm', run_time, width)
            self.drawTwig(line_3.get_start(), line_3.get_end(), iterations - 1, key + 'l', run_time, width)