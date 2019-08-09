import math


def get_distance_between_points(point_a, point_b):
    return math.sqrt((point_b[0] - point_a[0])**2+(point_b[1] - point_a[1])**2)


def add(point_a, point_b):
    return point_a[0]+point_b[0], point_a[1]+point_b[1]


def sub(point_a, point_b):
    return point_a[0]-point_b[0], point_a[1]-point_b[1]


def multiply(point, scalar):
    return point[0]*scalar, point[1]*scalar


def is_polygon_clockwise(polygon):
    if len(polygon) < 3:
        return False
    sum = [0]
    for i in range(len(polygon)-1):
        sum[0] = sum[0] + (polygon[i+1][0]-polygon[i][0]) * (polygon[i+1][1]+polygon[i][1])
    sum[0] = sum[0] + (polygon[0][0] - polygon[len(polygon)-1][0]) * (polygon[0][1] + polygon[len(polygon)-1][1])
    return sum[0] > 0


def is_point_on_the_left(point_a, point_b, point):
    position = ((point_b[0] - point_a[0]) * (point[1] - point_a[1]) -
               (point_b[1] - point_a[1]) * (point[0] - point_a[0]))
    return position


def get_vector(point_a, point_b):
    dx = point_b[0] - point_a[0]
    dy = point_b[1] - point_a[1]
    return dx, dy


def get_angle(center, mouse_pos):
    dx = mouse_pos[0] - center[0]
    dy = mouse_pos[1] - center[1]
    in_rads = math.atan2(dy, dx)
    if in_rads < 0:
        return math.fabs(in_rads)
    else:
        return 2 * math.pi - in_rads


def normalise_vector(vector):
    ln = math.sqrt(vector[0]**2+vector[1]**2)
    if ln == 0:
        return 0, 0
    return vector[0]/ln, vector[1]/ln
