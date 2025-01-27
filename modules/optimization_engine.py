def best_fit_decreasing(available_pipe_length, sizes_quantities, cutting_loss):
    sizes_quantities.sort(key=lambda x: -x[0])  # Sort by size descending
    pipes = []  # This will hold the detailed pipe data
    cutting_plan = []  # This will hold the formatted cutting plan for user display
    total_remaining_length = 0  # To track total remaining length across all pipes

    for size, quantity in sizes_quantities:
        for _ in range(quantity):
            best_fit_index = -1
            min_space_left = available_pipe_length + 1

            # Try to fit the current cut in an existing pipe
            for i in range(len(pipes)):
                if pipes[i]['remaining'] >= size + cutting_loss and pipes[i]['remaining'] - (size + cutting_loss) < min_space_left:
                    best_fit_index = i
                    min_space_left = pipes[i]['remaining'] - (size + cutting_loss)

            if best_fit_index == -1:
                # No suitable pipe found, add a new one
                new_pipe = {'lengths': [size], 'remaining': available_pipe_length - (size + cutting_loss)}
                pipes.append(new_pipe)
            else:
                # Add the current size to an existing pipe
                pipes[best_fit_index]['lengths'].append(size)
                pipes[best_fit_index]['remaining'] -= (size + cutting_loss)

    # Prepare the cutting plan for user-friendly display
    for i, pipe in enumerate(pipes):
        cutting_plan.append({
            'stock_pipe': f'Pipe {i + 1}',  # Identify the pipe number
            'used_lengths': pipe['lengths'],  # List of cut sizes from this pipe
            'remaining_length': pipe['remaining']  # Remaining length in this pipe
        })
        total_remaining_length += pipe['remaining']  # Add the remaining length of each pipe

    total_pipes_used = len(pipes)
    return pipes, cutting_plan, total_pipes_used, total_remaining_length
