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

def draw(space, window, draw_options, live_line, live_circle, lines, positions, radii):
    window.fill("white")
    space.debug_draw(draw_options)       
    font = pygame.font.Font('freesansbold.ttf', 16)
    white, black = (0, 0, 0,), (255, 255, 255)

    if live_circle:
        pygame.draw.circle(window, "red", live_circle[0], live_circle[1])

        textX, textY = live_circle[0][0], live_circle[0][1] + live_circle[1] #x: circle pos, y = circle pos + mouse dist from pos
        text = font.render(str(int(live_circle[1] * scaler)) + " m", True, white, black)
        display_text(text, textX, textY)

    i = 0
    while i < len(radii):
        pygame.draw.circle(window, "black", positions[i], radii[i]) #pos, radius

        text = font.render(str(int(radii[i] * scaler)) + " m", True, white, black)
        display_text(text, positions[i][0], positions[i][1] + radii[i]) #x: circle pos, y = circle pos + radius

        massText = font.render(str(int(masses[i])) + " kg", True, white, black)
        display_text(massText, positions[i][0], positions[i][1]) # center
        i += 1
    
    if live_line:
        pygame.draw.line(window, "red", live_line[0], live_line[1], 3)

        velocity = calc_dist(live_line[1], live_line[0]) * scaler
        text = font.render(str(int(velocity)) + " m/s", True, white, black)
        display_text(text, abs(live_line[1][0] + live_line[0][0]) / 2, abs(live_line[1][1] + live_line[0][1]) / 2) # abs( coords ) / 2

        
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
    positions = [] # [ball_pos1, ball_pos2, ...]
    forces = []
    radii = []
    

    space = pymunk.Space()
    boundaries(space, width, height)
    draw_options = pymunk.pygame_util.DrawOptions(window)

    ball_pos = None
    pressed_pos = None
    live_line = None
    live_circle = None
    radius = None

    while run:      
        if radius: #when choosing speed, between 2nd & 3rd click
            live_line = [ball_pos, pygame.mouse.get_pos()]
        elif ball_pos: #when choosing radius, between 1st & 2nd click
            live_circle = [ball_pos, calc_dist(ball_pos, pygame.mouse.get_pos())]       

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run = False
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (ball_count < max_ball_count) and (not ball_pos) and (not radius): #First click, choose position
                    ball_pos = pygame.mouse.get_pos()
                    positions.append(ball_pos)
                    ball_count += 1
                elif ball_pos and (not radius): #Second click choose radius
                    radius = calc_dist(ball_pos, pygame.mouse.get_pos())
                    radii.append(radius)
                elif radius: #Third click choose speed
                    pressed_pos = pygame.mouse.get_pos()
                    lines.append((ball_pos, pressed_pos))
                    forces.append((calc_angle(ball_pos, pressed_pos), calc_dist(ball_pos, pressed_pos) * 1)) #angle, magnitude * multiplier
                    ball_pos = None
                    pressed_pos = None
                    radius = None
                else:
                    i = 0
                    while i < max_ball_count:
                        thing = create_ball(space, radii[i], masses[i], positions[i])
                        thing.body.apply_impulse_at_local_point((forces[i][1] * math.cos(forces[i][0]) * masses[i], forces[i][1] * math.sin(forces[i][0]) * masses[i]), (0, 0))
                        i += 1
                    circles, forces, lines, radii, live_circle, live_line = [], [], [], [], None, None
                    break




        draw(space, window, draw_options, live_line, live_circle, lines, positions, radii)
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