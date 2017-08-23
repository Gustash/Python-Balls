from graphics import *
from math import sqrt
import random


_update_last_time = time.time()


########################################################################################################################
# Use this function to update the screen at a constant framerate. This function is available in graphics.py v5.0
def update_with_rate(rate):
    global _update_last_time
    now = time.time()
    pause_length = 1/rate-(now-_update_last_time)
    if pause_length > 0:
        time.sleep(pause_length)
        _update_last_time = now + pause_length
    else:
        _update_last_time = now
    update()


# Use this function to check if the circle is at the horizontal edge
def is_at_edge_hor(circle_center, circle_radius, window_width):
    return circle_center + circle_radius >= window_width \
        or circle_center - circle_radius <= 0


# Use this function to check if the circle is at the vertical edge
def is_at_edge_ver(circle_center, circle_radius, window_height):
    return circle_center - circle_radius <= 0 \
        or circle_center + circle_radius >= window_height


# Use this function to set the line that will be the diameter of the circle
def draw_line(p1, p2):
    line = Line(p1, p2)
    return line


# Use this function to draw the circle based on the line provided (which is the diameter)
def draw_circle_with_line(point, line, window):
    c_center = line.getCenter()

    last_point_x = point.getX()
    last_point_y = point.getY()
    center_x = c_center.getX()
    center_y = c_center.getY()

    w = last_point_x - center_x
    h = last_point_y - center_y
    r_sqr = w ** 2 + h ** 2
    circle_radius = sqrt(r_sqr)

    line.undraw()
    circle = Circle(c_center, circle_radius)
    circle.setFill(gen_hex_colour_code())
    circle.draw(window)
    return circle


# Use this function to generate a random hex color code
def gen_hex_colour_code():
    color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
    return '#' + color


# Use this function to get the direction in the X vector
def get_dir_x(last_point_x, circle_center_x):
    return last_point_x - circle_center_x


# Use this function to get the direction in the Y vector
def get_dir_y(last_point_y, circle_center_y):
    return last_point_y - circle_center_y


# Use this function to calculate the direction and speed for both vectors, to later apply to the circle movement
def calculate_direction(last_point_x, last_point_y, circle_center_x, circle_center_y, speed):
    x = get_dir_x(last_point_x, circle_center_x)
    y = get_dir_y(last_point_y, circle_center_y)

    x_pos = (-x) ** 2
    y_pos = (-y) ** 2

    if x_pos > y_pos:
        x /= x_pos
        y /= x_pos
    elif y_pos > x_pos:
        x /= y_pos
        y /= y_pos

    x *= speed
    y *= speed
    return {
        'x': x,
        'y': y
    }


# Use this function to check if the given coordinates are inside the circle
def in_circle(center_x, center_y, radius, x, y):
    return (center_x - x) ** 2 + (center_y - y) ** 2 <= radius**2
########################################################################################################################


# Create the window
win_width = 500
win_height = 500
win = GraphWin("My Window", win_width, win_height, autoflush=False)

# Set up some informative Texts
text_size = 8
texts = [
    Text(Point(win_width / 2, 15), """
Click twice to create a circle with the diameter of the distance between the two clicks.
    """),
    Text(Point(win_width/2, 30), """
Note: The circle will move in the direction of the last click.
    """)
]

for t in texts:
    t.setSize(text_size)
    t.draw(win)

# Get the points to draw the line with
first_point = win.getMouse()
last_point = win.getMouse()

# Draw the line and then the circle using it
l = draw_line(first_point, last_point)
c = draw_circle_with_line(last_point, l, win)

# Define the speed and calculate the direction in which to move the circle in
spd = 60
direction = calculate_direction(last_point.getX(), last_point.getY(), c.getCenter().getX(), c.getCenter().getY(), spd)
dx = direction['x']
dy = direction['y']

# Undraw Texts elements
for t in texts:
    t.undraw()

# Draw new Text explaining how to close window
t = Text(Point(win_width / 2, 15), """
Click the circle you just created to close the window. Better be fast!
""")
t.setSize(text_size)
t.draw(win)

# Loop the animation forever, moving the circle in the direction calculated and bounce off the "walls"
cr = c.getRadius()
while True:
    cp = c.getCenter()
    cpx = cp.getX()
    cpy = cp.getY()
    if is_at_edge_hor(cpx, cr, win_width):
        dx = -dx
    elif is_at_edge_ver(cpy, cr, win_height):
        dy = -dy
    c.move(dx, dy)
    # If mouse is clicked, close the window and stop the loop
    point_clicked = win.checkMouse()
    if point_clicked is not None:
        # Only close the window if the user clicked inside the circle
        if in_circle(cpx, cpy, cr, point_clicked.getX(), point_clicked.getY()):
            win.close()
            break
    # Update the screen at 60 FPS
    update_with_rate(60)
