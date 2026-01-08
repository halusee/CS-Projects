import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

def calc_dist(p1, p2):
     return math.sqrt((p2[1] - p1[1])**2 + ((p2[0] - p1[0])**2))

def calc_angle(p1, p2):
     return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def draw(space, window, draw_options, live_line, live_circle, lines, positions, radii):
    window.fill("white")
    space.debug_draw(draw_options)        
    
    if live_line:
        pygame.draw.line(window, "black", live_line[0], live_line[1], 3)
    if live_circle:
        pygame.draw.circle(window, "black", live_circle[0], live_circle[1])

    i = 0
    while i < len(radii):
       pygame.draw.circle(window, "red", positions[i], radii[i]) #pos, radius
       i += 1

    for line in lines:
        pygame.draw.line(window, "red", line[0], line[1])

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
    shape.color = (255,0,0,100)
    shape.elasticity = 1
    space.add(body, shape)
    return shape

def run(window, width, height, max_ball_count):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps
    ball_count = 0
    lines = []
    positions = []
    forces = []
    radii = []
    mass = 10
    

    space = pymunk.Space()
    boundaries(space, width, height)
    draw_options = pymunk.pygame_util.DrawOptions(window)

    ball_pos = None
    pressed_pos = None
    live_line = None
    live_circle = None
    radius = None

    while run:      
        if radius:
            live_line = [ball_pos, pygame.mouse.get_pos()]
        elif ball_pos:
            live_circle = [ball_pos, calc_dist(ball_pos, pygame.mouse.get_pos())]       

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run = False
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (ball_count < max_ball_count) and (not ball_pos) and (not radius): 
                    ball_pos = pygame.mouse.get_pos()
                    positions.append(ball_pos)
                    ball_count += 1
                elif ball_pos and (not radius):
                    radius = calc_dist(ball_pos, pygame.mouse.get_pos())
                    radii.append(radius)
                elif radius:
                    pressed_pos = pygame.mouse.get_pos()
                    lines.append((ball_pos, pressed_pos))
                    forces.append((calc_angle(ball_pos, pressed_pos), calc_dist(ball_pos, pressed_pos) * 25)) #angle, magnitude * multiplier
                    ball_pos = None
                    pressed_pos = None
                    radius = None
                else:
                    i = 0
                    while i < max_ball_count:
                        thing = create_ball(space, radii[i], masses[i], positions[i])
                        thing.body.apply_impulse_at_local_point((forces[i][1] * math.cos(forces[i][0]), forces[i][1] * math.sin(forces[i][0])), (0, 0))
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
    print("Commit and push test!!!!")
if __name__ == "__main__":
    run(window, WIDTH, HEIGHT, ball_count)