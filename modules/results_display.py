import matplotlib.pyplot as plt
import seaborn as sns


def visualize_cutting(pipes, available_pipe_length, cutting_loss, sizes_quantities):
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 8))
    bar_height = 0.5

    global size_to_color
    total_used_length = 0
    total_waste = 0
    sizes = set(size for size, _ in sizes_quantities)
    colors = sns.color_palette("tab20", len(sizes))
    size_to_color = {size: colors[i] for i, size in enumerate(sizes)}

    for i, pipe in enumerate(pipes):
        cuts = pipe['lengths']
        used_length = sum(cuts) + cutting_loss * (len(cuts) - 1)
        unused_length = available_pipe_length - used_length
        total_used_length += used_length
        total_waste += unused_length

        bottom = 0
        for cut in cuts:
            color = size_to_color[cut]
            # Draw the bar
            ax.barh(i, cut, bar_height, left=bottom, color=color, edgecolor='black')
            # Add text label for the size
            ax.text(bottom + cut / 2, i, str(cut), ha='center', va='center', fontsize=10, color='white', weight='bold')
            bottom += cut + cutting_loss

        # Draw the unused length in red
        ax.barh(i, unused_length, bar_height, left=used_length, color='red', edgecolor='black')
        # Add text label for the unused length
        if unused_length > 0:
            ax.text(used_length + unused_length / 2, i, f"{unused_length}", ha='center', va='center', fontsize=10, color='white', weight='bold')

    # Adding labels and legend
    ax.set_xlabel('Length (mm)', fontsize=12)
    ax.set_ylabel('Pipe Index', fontsize=12)
    ax.set_title('Pipe Cutting Visualization', fontsize=16)
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color, edgecolor='black') for color in colors]
    legend_labels = [f'Cut Size: {size}' for size in sizes]
    #ax.legend(legend_handles, legend_labels, title="Cut Sizes", bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    img_path = 'static/cutting_visualization.png'
    plt.savefig(img_path)
    plt.close()

    # Generate the pie chart for waste vs used material
    labels = ['Used Material', 'Waste Material']
    sizes = [total_used_length, total_waste]
    colors = ['#2ca02c', '#d62728']  # Green for used, red for waste

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Pipe Usage (Used Material vs Waste)', fontsize=16)
    pie_chart_path = 'static/pipe_usage_pie_chart.png'
    plt.savefig(pie_chart_path)
    plt.close()

    return img_path, total_used_length, total_waste, pie_chart_path


def cut_distribution_histogram(sizes_quantities):
    global size_to_color  # Use the global size_to_color mapping

    # Extract sizes and quantities from the list of tuples
    sizes = [size for size, _ in sizes_quantities]
    quantities = [quantity for _, quantity in sizes_quantities]

    # Dynamically calculate bar width
    num_bars = len(sizes_quantities)
    plot_width = 12  # Width of the figure in inches
    bar_width = plot_width / (num_bars * 2.5)  # Adjust divisor to control spacing

    # Create the bar chart
    plt.figure(figsize=(12, 8))

    # Plot bars with the same color mapping as in visualize_cutting
    for i, (size, quantity) in enumerate(sizes_quantities):
        color = size_to_color.get(size, 'grey')  # Default to grey if the size is not in the mapping
        plt.bar(size, quantity, color=color, edgecolor='black', width=25)

    # Add titles and labels
    plt.title('Sizes vs Quantities', fontsize=16)
    plt.xlabel('Size', fontsize=14,)
    plt.ylabel('Quantity', fontsize=14 )
    plt.xticks(rotation=45, fontsize=12)  # Rotate and style x-axis labels
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the chart
    cut_dist_img = "static/cut_distribution_histogram.png"
    plt.savefig(cut_dist_img)
    plt.close()  # Close the plot to prevent display in an interactive session

    return cut_dist_img

def cutting_efficiency(total_used_length, total_waste, total_length):
    return (total_used_length / total_length) * 100