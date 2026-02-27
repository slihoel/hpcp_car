import Obstacle as obs
import math

start = tuple([200, 100])
r = 200
n = 50
t = 10
def getMap(level=1):
    obstacles = []
    if level == 1:
        obstacles.append(obs.Obstacle(start[0] + 2 * n, start[1], n, n, "assets/white_wall.png", -1, 0))
        obstacles.append(obs.Obstacle(start[0] - 2 * n, start[1], n, n, "assets/white_wall.png", -1, 0))
        for i in range(t):
            alpha = ((i + 1) * math.pi) / (2 * (t + 1))
            M = tuple([start[0] + r - r * math.cos(alpha), start[1] + r * math.sin(alpha)])
            obstacles.append(obs.Obstacle(M[0] + math.cos(alpha) * 2 * n, M[1] - math.sin(alpha) * 2 * n, n, n, "assets/red_wall.png" if i % 2 == 0 else "assets/white_wall.png", i, alpha))
            obstacles.append(obs.Obstacle(M[0] - math.cos(alpha) * 2 * n, M[1] + math.sin(alpha) * 2 * n, n, n, "assets/red_wall.png" if i % 2 == 0 else "assets/white_wall.png", i + t, alpha))

    return obstacles