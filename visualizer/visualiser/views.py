from django.shortcuts import render
import plotly.graph_objects as go
from plotly.offline import plot
import numpy as np


def index(request):
    # Define fixed random matrices for each season (5x4, 20 compartments)
    seasons_data = {
        'Winter': np.array([
            [1, 2, 2, 2],
            [1, 2, 1, 2],
            [2, 2, 1, 2],
            [2, 2, 2, 1],
            [2, 2, 2, 2]
        ]),
        'Spring': np.array([
            [2, 2, 1, 2],
            [2, 2, 2, 1],
            [2, 2, 2, 2],
            [2, 1, 2, 2],
            [2, 2, 1, 1]
        ]),
        'Summer': np.array([
            [2, 1, 2, 2],
            [1, 2, 2, 2],
            [2, 2, 2, 1],
            [2, 2, 1, 2],
            [1, 2, 2, 2]
        ]),
        'Fall': np.array([
            [2, 2, 2, 1],
            [2, 1, 2, 2],
            [2, 2, 1, 2],
            [1, 2, 2, 2],
            [2, 2, 2, 1]
        ]),
    }

    # Get the selected season from the request
    selected_season = request.GET.get('season', 'Winter')  # Default to 'Winter'
    matrix = seasons_data[selected_season]

    # Create figure with shape-based visualization
    fig = go.Figure()

    # Define grid size
    rows, cols = matrix.shape
    cell_size = 150  # Adjust the size of each block

    # Define colors
    colors = {1: 'blue', 2: 'grey'}

    # Add rectangle shapes for each matrix entry
    for i in range(rows):
        for j in range(cols):
            value = matrix[i, j]
            fig.add_shape(
                type="rect",
                x0=j * cell_size, y0=(rows - i - 1) * cell_size,  # Invert Y-axis to match grid orientation
                x1=(j + 1) * cell_size, y1=(rows - i) * cell_size,
                fillcolor=colors[value],
                line=dict(color="dark grey"),
            )
            # Add text label inside the cell

            fig.add_annotation(
                x=j * cell_size + cell_size / 2,
                y=(rows - i - 1) * cell_size + cell_size / 2,
                text="Coolant" if value == 1 else "Server",
                showarrow=False,
                font=dict(size=12, color="white" if value == 2 else "black"),
            )

    # Set figure layout
    fig.update_layout(
        title=f"Data Center Layout - {selected_season}",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        width=cols * cell_size + 100,  # Adjust figure size dynamically
        height=rows * cell_size + 100,
        showlegend=False
    )

    # Convert Plotly figure to HTML div
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    # Pass the plot div and selected season to the template
    context = {
        'plot_div': plot_div,
        'selected_season': selected_season,
        'seasons': list(seasons_data.keys()),  # For dropdown selection in HTML
    }

    return render(request, 'visualizer/index.html', context)
