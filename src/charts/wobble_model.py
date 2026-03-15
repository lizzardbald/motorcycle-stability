import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def simulate_wobble(v, trail, c_mech=5.0, I_steer=1.5, t_span=(0, 5), trigger_delta=0.1):
    """
    Simulates the motorcycle steering stability (wobble).
    
    Parameters:
    - v: Velocity (m/s)
    - trail: Mechanical trail (m)
    - c_mech: Mechanical damping (e.g., steering damper)
    - I_steer: Moment of inertia of the steering assembly
    - t_span: Time range for simulation (seconds)
    - trigger_delta: Initial displacement (radians) representing the 'trigger'
    """
    
    # Modeling the coefficients based on the physics discussed:
    # 1. Stiffness (Restoring Force): Increases with trail and v^2
    # Simplified approximation: k = C1 * v^2 * trail
    k_eff = (100.0 * (v**2) * trail) / 10.0 # Arbitrary scaling for visualization
    
    # 2. Effective Damping: Mechanical damping minus a velocity-dependent destabilization factor
    # Quadratic in v: gyroscopic destabilization grows with v^2
    sigma_v = 0.008 * v ** 2
    c_eff = c_mech - sigma_v
    
    # Define the ODE system: y' = f(t, y) where y = [delta, delta_dot]
    def ode_system(t, y):
        delta, delta_dot = y
        # delta_ddot = (1/I) * (-c_eff * delta_dot - k_eff * delta)
        delta_ddot = (-c_eff * delta_dot - k_eff * delta) / I_steer
        return [delta_dot, delta_ddot]

    # Initial conditions: [initial angle, initial angular velocity]
    y0 = [trigger_delta, 0.0]
    
    # Solve the ODE
    t_eval = np.linspace(t_span[0], t_span[1], 1000)
    sol = solve_ivp(ode_system, t_span, y0, t_eval=t_eval)
    
    return sol.t, sol.y[0]

