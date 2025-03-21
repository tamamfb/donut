import numpy as np
from time import sleep

screen_size = 40
theta_spacing = 0.07
phi_spacing = 0.02
illumination = np.fromiter(".,-~:;=!*#$@", dtype="<U1")

A, B = 1, 1
R1, R2, K2 = 1, 2, 5
K1 = screen_size * K2 * 3 / (8 * (R1 + R2))

def render_frame(A, B):
    cos_A, sin_A = np.cos(A), np.sin(A)
    cos_B, sin_B = np.cos(B), np.sin(B)
    
    output = np.full((screen_size, screen_size), " ")
    zbuffer = np.zeros((screen_size, screen_size))
    
    phi = np.arange(0, 2 * np.pi, phi_spacing)
    theta = np.arange(0, 2 * np.pi, theta_spacing)
    cos_phi, sin_phi = np.cos(phi), np.sin(phi)
    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    circle_x, circle_y = R2 + R1 * cos_theta, R1 * sin_theta
    
    x = (np.outer(cos_B * cos_phi + sin_A * sin_B * sin_phi, circle_x) - circle_y * cos_A * sin_B).T
    y = (np.outer(sin_B * cos_phi - sin_A * cos_B * sin_phi, circle_x) + circle_y * cos_A * cos_B).T
    z = ((K2 + cos_A * np.outer(sin_phi, circle_x)) + circle_y * sin_A).T
    ooz = np.reciprocal(z)
    xp = (screen_size / 2 + K1 * ooz * x).astype(int)
    yp = (screen_size / 2 - K1 * ooz * y).astype(int)
    
    L1 = ((np.outer(cos_phi, cos_theta) * sin_B) - cos_A * np.outer(sin_phi, cos_theta)) - sin_A * sin_theta
    L2 = cos_B * (cos_A * sin_theta - np.outer(sin_phi, cos_theta * sin_A))
    L = np.around((L1 + L2) * 8).astype(int).T
    mask_L = L >= 0
    chars = illumination[L]
    
    for i in range(90):
        mask = mask_L[i] & (ooz[i] > zbuffer[xp[i], yp[i]])
        zbuffer[xp[i], yp[i]] = np.where(mask, ooz[i], zbuffer[xp[i], yp[i]])
        output[xp[i], yp[i]] = np.where(mask, chars[i], output[xp[i], yp[i]])
    
    return output

def pprint(array):
    print(*[" ".join(row) for row in array], sep="\n")

if __name__ == "__main__":
    for _ in range(screen_size * screen_size):
        A += theta_spacing
        B += phi_spacing
        print("\x1b[H")
        pprint(render_frame(A, B))
        sleep(0.01)
