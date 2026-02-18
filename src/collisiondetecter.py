
from typing import List, Tuple

#orthogonal projection of vector1 onto vector2
def orthogonal_projection(vector1: Tuple[float, float], vector2:Tuple[float, float]) -> Tuple[float, float]:
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude_squared = vector2[0] ** 2 + vector2[1] ** 2
    if magnitude_squared == 0:
        return (0.0, 0.0)
    projection_scale = dot_product / magnitude_squared
    return (projection_scale * vector2[0], projection_scale * vector2[1])


def isColided(object1: List[Tuple[float, float]], object2: List[Tuple[float, float]], issecond = False, debug = False) -> bool:
    startpoint = object1[0]
    vector1 = (object1[1][0] - startpoint[0], object1[1][1] - startpoint[1])
    vectors2 = [
        (object2[0][0] - startpoint[0], object2[0][1] - startpoint[1]),
        (object2[1][0] - startpoint[0], object2[1][1] - startpoint[1]),
        (object2[2][0] - startpoint[0], object2[2][1] - startpoint[1]),
        (object2[3][0] - startpoint[0], object2[3][1] - startpoint[1])
    ]
    orthogonal_projected_vectors2 = [orthogonal_projection(v, vector1) for v in vectors2]
    min_orthogonal_projected_vector2 = orthogonal_projected_vectors2[0]
    max_orthogonal_projected_vector2 = orthogonal_projected_vectors2[0]
    divisor = 0 if vector1[0] != 0 else 1
    
    for v in orthogonal_projected_vectors2:
        if v[divisor] / vector1[divisor] < min_orthogonal_projected_vector2[divisor] / vector1[divisor]:
            min_orthogonal_projected_vector2 = v
        if v[divisor] / vector1[divisor] > max_orthogonal_projected_vector2[divisor] / vector1[divisor]:
            max_orthogonal_projected_vector2 = v
    if min_orthogonal_projected_vector2[divisor] / vector1[divisor] > 1 or max_orthogonal_projected_vector2[divisor] / vector1[divisor] < 0:    
        return False
    if not issecond:
        object1.pop(0)
        return isColided(object1, object2, issecond=True, debug=debug)
    else:
        if debug:
            print("Collided with obstacle")
            print("vector1:", vector1)
            print("orthogonal_projected_vectors2:", orthogonal_projected_vectors2)  
            print("min_orthogonal_projected_vector2:", min_orthogonal_projected_vector2)
            print("max_orthogonal_projected_vector2:", max_orthogonal_projected_vector2)
        return True
    
