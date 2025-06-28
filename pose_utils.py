import math

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points (in degrees).
    a, b, c are each (x, y) tuples representing joints.
    The angle is at point b.
    """
    try:
        a = [a.x, a.y]
        b = [b.x, b.y]
        c = [c.x, c.y]

        ba = [a[0] - b[0], a[1] - b[1]]
        bc = [c[0] - b[0], c[1] - b[1]]

        # Dot product and magnitude
        dot_product = ba[0]*bc[0] + ba[1]*bc[1]
        magnitude_ba = math.sqrt(ba[0]**2 + ba[1]**2)
        magnitude_bc = math.sqrt(bc[0]**2 + bc[1]**2)

        if magnitude_ba * magnitude_bc == 0:
            return 0
    except AttributeError:
        return 0
