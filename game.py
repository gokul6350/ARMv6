import matplotlib.pyplot as plt
import numpy as np
from inverse_k import inverse_k2dof as ik
from matplotlib.widgets import Slider
import math
from datetime import datetime



# Arm lengths
L1 = 11
L2 = 16

# Initial end effector position
end_effector_x = -21
end_effector_y = 0




# Function to update the plot based on slider values"""
"""
def update(val):
    global theta1, theta2
    theta1 = slider_theta1.val
    theta2 = slider_theta2.val
    update_simulation()
"""
# Function to update the simulation based on joint angles
def update_simulation():
    joint2_x = L1 * np.cos(theta1)
    joint2_y = L1 * np.sin(theta1)
    end_effector_x_sim = joint2_x + L2 * np.cos(theta1 + theta2)
    end_effector_y_sim = joint2_y + L2 * np.sin(theta1 + theta2)

    # Clear previous plot and plot the updated simulation
    ax.clear()
    ax.plot([0, joint2_x], [0, joint2_y], 'r-')
    ax.plot([joint2_x, end_effector_x_sim], [joint2_y, end_effector_y_sim], 'b-')
    ax.plot(0, 0, 'ro')  # Joint 1
    ax.plot(joint2_x, joint2_y, 'ro')  # Joint 2
    ax.plot(end_effector_x_sim, end_effector_y_sim, 'bo')  # End effector
    ax.set_xlim([-30, 30])
    ax.set_ylim([-30, 30])
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('2-DOF Robotic Arm Simulation')
    ax.grid(True)
    plt.draw()
def sim_inverse_k(end_effector_x,end_effector_y):
# Initial joint angles
    p,initial_theta1, initial_theta2 = ik(end_effector_x, end_effector_y, L1, L2)
    global theta1,theta2,ax
    theta1 =  math.radians(initial_theta1*-1)
    theta2 =  math.radians(initial_theta2*-1)
    print(f"{theta1} and {theta2}")
# Create the initial plot
    fig, ax = plt.subplots()
    update_simulation()

# Create slider axes and sliders for joint angles
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    axcolor = 'lightgoldenrodyellow'
    plt.savefig(f'logs/sim-{formatted_time}.png')
"""
ax_theta1 = plt.axes([0.1, 0.01, 0.65, 0.03], facecolor=axcolor)
ax_theta2 = plt.axes([0.1, 0.06, 0.65, 0.03], facecolor=axcolor)

slider_theta1 = Slider(ax_theta1, 'Theta1', -np.pi, np.pi, valinit=initial_theta1, valfmt='%1.2f rad')
slider_theta2 = Slider(ax_theta2, 'Theta2', -np.pi, np.pi, valinit=initial_theta2, valfmt='%1.2f rad')

# Attach the update function to the slider change event
slider_theta1.on_changed(update)
slider_theta2.on_changed(update)
"""
    
