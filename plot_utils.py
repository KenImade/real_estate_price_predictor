import os
import matplotlib.pyplot as plt

def save_plot_to_png(plot_name, city_name):
    """
    Save the current plot to a PNG file.
    
    Parameters:
    - plot_name: The name to give the saved plot (without the .png extension).
    - city_name: The name of the city to save the pictures to.
    """
    
    directory = f'./Data/plots/{city_name}/'
    
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    # Save the plot
    fig = plt.gcf()
    plt.tight_layout()
    plt.savefig(f'{directory}{plot_name}.png', dpi=300)
