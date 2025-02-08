import numpy as np
import matplotlib.pyplot as plt

def naca4_airfoil(m, p, t, c=1.0, n=100):
    # x-coordinates from 0 to c
    x = np.linspace(0, c, n)
    
    # Thickness distribution formula for NACA 4-digit airfoils
    yt = (t/0.2) * c * (0.2969 * np.sqrt(x/c) - 0.1260 * (x/c) 
                        - 0.3516 * (x/c)**2 + 0.2843 * (x/c)**3 
                        - 0.1015 * (x/c)**4)
    
    # Camber line and its slope
    yc = np.where(x < p*c, 
                  m/p**2 * (2*p*x/c - (x/c)**2), 
                  m/(1-p)**2 * ((1 - 2*p) + 2*p*x/c - (x/c)**2))
    dyc_dx = np.where(x < p*c, 
                      2*m/p**2 * (p - x/c), 
                      2*m/(1-p)**2 * (p - x/c))
    theta = np.arctan(dyc_dx)
    
    # Upper and lower surface coordinates
    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)

    return xu, yu, xl, yl

def rotate_airfoil(x, y, angle):
    # Rotate points around origin by angle (in degrees)
    theta = np.radians(angle)
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)], 
                                [np.sin(theta), np.cos(theta)]])
    coords = np.vstack((x, y))
    rotated_coords = rotation_matrix @ coords
    return rotated_coords[0], rotated_coords[1]

def plot_multiple_airfoils(angles_of_attack):
    plt.figure(figsize=(14, 7))
    
    for angle_of_attack in angles_of_attack:
        xu, yu, xl, yl = naca4_airfoil(m=0.02, p=0.4, t=0.12, c=2.0, n=200)  # Increased chord length
        
        # Rotate upper and lower surfaces
        xu_rot, yu_rot = rotate_airfoil(xu, yu, angle_of_attack)
        xl_rot, yl_rot = rotate_airfoil(xl, yl, angle_of_attack)
        
        # Plotting airfoil
        plt.plot(xu_rot, yu_rot, label=f'Upper Surface ({angle_of_attack}°)', linestyle='-')
        plt.plot(xl_rot, yl_rot, linestyle='-')

        # Indicating the chord line for each airfoil with dashed, unfilled arrows
        plt.annotate('', xy=(np.cos(np.radians(angle_of_attack)) * 2, 
                             np.sin(np.radians(angle_of_attack)) * 2), 
                     xytext=(0, 0), 
                     arrowprops=dict(arrowstyle='->', linestyle='--', fill=False), 
                     label=f'Chord Line ({angle_of_attack}°)')

    # Indicating the free-stream flow from -1 to 10 with dashed arrow
    plt.annotate('', xy=(10, 0), xytext=(-1, 0),
                 arrowprops=dict(arrowstyle='->', linestyle='--', fill=False), 
                 label='Free-stream flow')

    plt.title('Comparison of Airfoils with Angles of Attack: 10° and 60°')
    plt.gca().set_aspect('equal', adjustable='datalim')
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.xlim(-2, 4)
    plt.ylim(-2, 3)

    plt.show()

# Example usage with angles of attack 10° and 60°
plot_multiple_airfoils(angles_of_attack=[10, 60])
