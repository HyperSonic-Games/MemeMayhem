import math

# Helper function for LERP interpolation
def lerp(start, end, t):
    return (start[0] + t * (end[0] - start[0]), start[1] + t * (end[1] - start[1]))

# Helper function for Dead Reckoning prediction
def dead_reckon(last_position, velocity, time_delta):
    # Predict new position based on velocity and elapsed time
    new_x = last_position[0] + velocity[0] * time_delta
    new_y = last_position[1] + velocity[1] * time_delta
    return (new_x, new_y)

# Main function that applies both LERP and Dead Reckoning
def apply_lerp_and_dead_reckoning(current_position, last_position, velocity, target_position, time_delta, lerp_factor=0.1):
    """
    Interpolates player position with LERP and applies Dead Reckoning for predicting position.
    
    Args:
    - current_position: Current known position (x, y).
    - last_position: Last known position before the update (x, y).
    - velocity: The current velocity of the player (dx, dy).
    - target_position: The new position update from the server (x, y).
    - time_delta: Time elapsed since the last update.
    - lerp_factor: LERP factor (0.0 to 1.0).
    
    Returns:
    - new_position: The final interpolated or predicted position (x, y).
    """
    
    # Step 1: Apply Dead Reckoning prediction
    predicted_position = dead_reckon(last_position, velocity, time_delta)
    
    # Step 2: LERP between predicted position and target position
    new_position = lerp(predicted_position, target_position, lerp_factor)
    
    return new_position

# Example usage
if __name__ == "__main__":
    # Example data
    last_position = (5, 5)  # Last known position
    current_position = (5, 5)  # Current known position
    velocity = (1, 1)  # Player's velocity (dx, dy)
    target_position = (8, 8)  # New position update from the server
    time_delta = 0.1  # Time elapsed between updates (seconds)
    
    # Apply the LERP and Dead Reckoning
    new_position = apply_lerp_and_dead_reckoning(current_position, last_position, velocity, target_position, time_delta, lerp_factor=0.1)
    
    print(f"New position: {new_position}")
