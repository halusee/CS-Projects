import pygame
import pymunk
import pymunk.pygame_util
import math
import random

pygame.init()

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
scaler = 0.1

def calc_dist(p1, p2):
     return math.sqrt((p2[1] - p1[1])**2 + ((p2[0] - p1[0])**2))

def calc_angle(p1, p2):
     return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def display_text(text, x, y):
    textRect = text.get_rect()
    textRect.center = (x, y)
    window.blit(text, textRect)

def draw(space, window, draw_options, lines, positions, radii):
    window.fill("white")
    space.debug_draw(draw_options)       
    font = pygame.font.Font('freesansbold.ttf', 16)
    white, black = (0, 0, 0,), (255, 255, 255)

    i = 0
    while i < len(radii):
        pygame.draw.circle(window, "black", positions[i], radii[i]) #pos, radius

        text = font.render(str(int(radii[i] * scaler)) + " m", True, white, black)
        display_text(text, positions[i][0], positions[i][1] + radii[i]) #x: circle pos, y = circle pos + radius

        massText = font.render(str(int(masses[i])) + " kg", True, white, black)
        display_text(massText, positions[i][0], positions[i][1]) # center
        i += 1
        
    for line in lines:

        pygame.draw.line(window, "grey", line[0], line[1], 3)

        velocity = calc_dist(line[1], line[0]) * scaler
        text = font.render(str(int(velocity)) + " m/s", True, white, black)
        display_text(text, abs(line[1][0] + line[0][0]) / 2, abs(line[1][1] + line[0][1]) / 2) # abs( coords ) / 2
    


    

    pygame.display.update()    


def boundaries(space, width, height):
    rects = [
        [(width/2, height - 10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(width - 10, height/2), (20, height)],
        [(10, height/2), (20, height)]   
    ]
    
    for pos, size, in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 1
        space.add(body, shape)
     

def create_ball(space, radius, mass, pos):
    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),100)
    shape.elasticity = 1
    space.add(body, shape)
    return shape

def run(window, width, height, max_ball_count):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps
    ball_count = 0
    lines = [] # [(ball_pos1, pressed_pos1), (ball_pos2, pressed_pos2), ...]
    positions = [None] # [ball_pos1, ball_pos2, ...]
    forces = []
    radii = []
    

    space = pymunk.Space()
    boundaries(space, width, height)
    draw_options = pymunk.pygame_util.DrawOptions(window)

    radius = None 
    pressed_pos = None


    while run:      

        ### Live Lines and circles
        if radius: #when choosing speed, between 2nd & 3rd click
            lines[-1] = [positions[-1], pygame.mouse.get_pos()]
        elif positions[-1]: #when choosing radius, between 1st & 2nd click
            radii[-1] = calc_dist(positions[-1], pygame.mouse.get_pos())           


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run = False
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (ball_count < max_ball_count) and (not positions[-1]) and (not radius): #First click, choose position
                    positions[-1] = pygame.mouse.get_pos()
                    radii.append(calc_dist(positions[-1], pygame.mouse.get_pos()) ) # place holder 
                    ball_count += 1
                elif positions[-1] and (not radius): #Second click choose radius.  
                    radius = calc_dist(positions[-1], pygame.mouse.get_pos())
                    radii[-1] = radius
                    lines.append([positions[-1], pygame.mouse.get_pos()]) #placeholder
                elif radius: #Third click choose speed
                    pressed_pos = pygame.mouse.get_pos()
                    lines[-1] = [positions[-1], pressed_pos]
                    forces.append((calc_angle(positions[-1], pressed_pos), calc_dist(positions[-1], pressed_pos) * 1)) #angle, magnitude * multiplier
                    positions.append(None)
                    pressed_pos = None
                    radius = None
                else:
                    i = 0
                    while i < max_ball_count:
                        thing = create_ball(space, radii[i], masses[i], positions[i])
                        thing.body.apply_impulse_at_local_point((forces[i][1] * math.cos(forces[i][0]) * masses[i], forces[i][1] * math.sin(forces[i][0]) * masses[i]), (0, 0))
                        i += 1
                    forces, lines, radii,  =  [], [], []
                    break

        draw(space, window, draw_options, lines, positions, radii)
        space.step(dt)
        clock.tick(fps)
    pygame.quit()

masses = []
n = 1

ball_count = int(input("Number of balls: "))
print("Masses:")
while n <= ball_count:
    masses.append(int(input(f"#{n}: ")))
    n += 1
if __name__ == "__main__":
    run(window, WIDTH, HEIGHT, ball_count)