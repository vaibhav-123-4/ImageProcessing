"""
Affine Matrix Module
Implements matrix operations for affine transformations without using numpy
"""

def matrix_multiply_3x3(matrix1, matrix2):
    """
    Multiply two 3x3 matrices
    Returns: 3x3 result matrix
    """
    result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    
    for i in range(3):
        for j in range(3):
            sum_val = 0
            for k in range(3):
                sum_val += matrix1[i][k] * matrix2[k][j]
            result[i][j] = sum_val
    
    return result


def matrix_multiply_point(matrix, x, y):
    """
    Multiply 3x3 transformation matrix with point [x, y, 1]
    Returns: (new_x, new_y)
    """
    # Point in homogeneous coordinates [x, y, 1]
    new_x = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2]
    new_y = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2]
    
    return new_x, new_y


def create_identity_matrix():
    """
    Create a 3x3 identity matrix
    """
    return [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]


def create_scaling_matrix(sx, sy):
    """
    Create a scaling transformation matrix
    sx: horizontal scaling factor
    sy: vertical scaling factor
    """
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]


def create_rotation_matrix(angle_degrees):
    """
    Create a rotation transformation matrix
    angle_degrees: rotation angle in degrees (counter-clockwise)
    """
    # Convert to radians
    import math
    angle_rad = angle_degrees * math.pi / 180.0
    
    cos_theta = math.cos(angle_rad)
    sin_theta = math.sin(angle_rad)
    
    return [
        [cos_theta, -sin_theta, 0],
        [sin_theta, cos_theta, 0],
        [0, 0, 1]
    ]


def create_translation_matrix(tx, ty):
    """
    Create a translation transformation matrix
    tx: horizontal translation
    ty: vertical translation
    """
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]


def create_shear_matrix(shx, shy):
    """
    Create a shear transformation matrix
    shx: horizontal shear factor
    shy: vertical shear factor
    """
    return [
        [1, shx, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ]


def combine_transformations(matrices):
    """
    Combine multiple transformation matrices by multiplying them
    matrices: list of 3x3 matrices
    Returns: combined transformation matrix
    """
    if not matrices:
        return create_identity_matrix()
    
    result = matrices[0]
    for i in range(1, len(matrices)):
        result = matrix_multiply_3x3(result, matrices[i])
    
    return result


def print_matrix(matrix, name="Matrix"):
    """
    Print a matrix in a readable format
    """
    print(f"\n{name}:")
    for row in matrix:
        print(f"  [{row[0]:8.4f} {row[1]:8.4f} {row[2]:8.4f}]")
