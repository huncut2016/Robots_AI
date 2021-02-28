import numpy as np
import math


def fromAngle(angle, length):
    return (
        np.array(
            [
                length * math.cos(angle),
                length * math.sin(angle)
            ]
        )
    )
