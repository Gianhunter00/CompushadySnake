import random
import numpy
import glfw
import struct

class Body():
    
    def __init__(self, parent):
        self.parent = parent
        self.grid_position = parent.grid_position
        self.size = parent.size
        self.position = [self.grid_position[0] * self.size[0], self.grid_position[1] * self.size[1]]

    def move(self):
        self.grid_position = self.parent.grid_position.copy()
        self.position = [self.grid_position[0] * self.size[0], self.grid_position[1] * self.size[1]]
        
        
class Snake():
    def __init__(self, world_size, power_up):
        self.power_up = power_up
        self.world = world_size
        self.direction = [0, 0]
        self.size = [20, 20]
        self.grid = [world_size[0] // self.size[0], world_size[1] // self.size[1]]
        self.grid_position = [self.grid[0] // 2, self.grid[1] // 2]
        self.position = [self.grid_position[0] * self.size[0], self.grid_position[1] * self.size[1]]
        self.speed = 2
        self.alive = True
        self.body = []
        self.line = 0
    
    def input(self, window):
        direction = self.direction
        if glfw.get_key(window, glfw.KEY_W) and direction != [0,1]:
            direction = [0, -1]
        elif glfw.get_key(window, glfw.KEY_S) and direction != [0,-1]:
            direction = [0, 1]
        elif glfw.get_key(window, glfw.KEY_A) and direction != [1,0]:
            direction = [-1, 0]
        elif glfw.get_key(window, glfw.KEY_D) and direction != [-1,0]:
            direction = [1, 0]
        self.direction = direction
        self.check_collision()
    
    def check_collision(self):
        if(self.grid_position == self.power_up.grid_position):
            self.power_up.change_position()
            self.add_body()
        for body in self.body[1:]:
            if(self.grid_position == body.grid_position):
                self.alive = False
     
    def pack_snake(self):
        complete_buffer = bytes(0)
        complete_buffer += struct.pack('4i', *numpy.concatenate((self.position, self.size)))
        body_buffer = self.calculate_pack_line()
        if body_buffer:
            self.line = len(body_buffer)
            for buffer in body_buffer:
                complete_buffer += struct.pack('4i', *buffer)
        return complete_buffer
                                  
    def move(self):
        for body in reversed(self.body):
            body.move()
        self.grid_position[0] += self.direction[0]
        self.grid_position[1] += self.direction[1]
        self.position = [self.grid_position[0] * self.size[0], self.grid_position[1] * self.size[1]]
            
    def add_body(self):
        if not self.body:
            self.body.append(Body(self))
        else:
            self.body.append(Body(self.body[-1]))
            
    def calculate_pack_line(self):
        if not self.body:
            return []
        start = numpy.concatenate((self.body[0].position, self.body[0].size))
        pack_line = []
        current_pos = self.body[0].grid_position.copy()
        rule = []
        movement = []
        for body in self.body[1:]:
            movement = body.grid_position.copy()
            movement[0] -= current_pos[0]
            movement[1] -= current_pos[1]
            if not rule:
                rule = movement.copy()
            if movement != rule:
                rule = []
                pack_line.append(start.copy())
                start = numpy.concatenate((body.position, body.size))
            
            current_pos = body.grid_position.copy()
            if not rule:
                continue
            if(movement[0] < 0):
                start[0] += movement[0] * body.size[0]
                start[2] += -movement[0] * body.size[0]
            elif(movement[1] < 0):
                start[1] += movement[1] * body.size[1]
                start[3] += -movement[1] * body.size[1]
            else:
                start[2] += movement[0] * body.size[0]
                start[3] += movement[1] * body.size[1]
        pack_line.append(start.copy())
        return pack_line
                
class PowerUp():
    def __init__(self, world_size):
        self.world = world_size
        self.fake_size = [19, 20]
        self.size = [20, 20]
        self.grid = [world_size[0] // self.size[0], world_size[1] // self.size[1]]
        self.grid_position = [random.randrange(0, self.grid[0]), random.randrange(0, self.grid[1])]
        self.position = [self.grid_position[0] * self.size[0], self.grid_position[1] * self.size[1]]
        
    def pack(self):
        return struct.pack('4i', *numpy.concatenate((self.position, self.fake_size)))
    
    def change_position(self):
        self.grid_position = [random.randrange(0, self.grid[0]), random.randrange(0, self.grid[1])]
        self.position = [self.grid_position[0] * self.size[0], self.grid_position[1] * self.size[1]]
        