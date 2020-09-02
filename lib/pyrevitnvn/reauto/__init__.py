
def plot_design_cordninates(list_values):
    """
    :param list_values: a list of grid spacings, i.e. [1,3,5], the spacing is 1, 3, 5
    :return: A list of where the ith grid spacing is, i.e [1,4,9] (first line is at 1, second at 4, etc)
    """
    new_list_cor = []
    sum_val = 0
    for i in list_values:
        sum_val += i
        new_list_cor.append(sum_val)
    return new_list_cor

# Helper function to make points
def make_point_from_coords(x, y, z=None):
    if z is None:
        return [x, y]
    return [x, y, z]

def get_corr_lines(far_pos, grid_line_spacing):
    """
    Gets the corner_lines position
    :param far_pos: The position that is the farthest, either front to back or left to right
    :param grid_line_spacing: The list that contains the grid line spacing of the of the dimension not stated above
            (i.e. far_pos is back to front and list is left to right)
    :return: corrlines_x, corr_lines_y
    """

    corr_lines_x = []
    corr_lines_y = []
    corr_x = [0, 0]
    corr_y = [0, far_pos]
    corr_lines_x.append(corr_x)
    corr_lines_y.append(corr_y)
    for x in plot_design_cordninates(grid_line_spacing):
        corr_x = [x, x]
        corr_y = [0, far_pos]
        corr_lines_x.append(corr_x)
        corr_lines_y.append(corr_y)
    return corr_lines_x, corr_lines_y

def get_edges_lines_corners_single_iteration(corr_linesA_x, corr_linesA_y, do_3d=False):
    """
    Helper function do remove duplication
    :param corr_linesA_x: corner lines along x dimension
    :param corr_linesA_y: corner lines along y dimension
    :param do_3d: boolean, should add 3d points (z=0) or not
    :return: plot_edges, plot_lines, corner_points
    """
    if do_3d:
        z = 0
    else:
        z = None
    plot_edges = []
    corner_points = []
    plot_lines = []
    i = 0
    for x, y in zip(corr_linesA_x, corr_linesA_y):
        point_a = make_point_from_coords(x[0], y[0], z)
        point_b = make_point_from_coords(x[1], y[1], z)

        if i == 0 or i == len(corr_linesA_x) - 1:
            # Corners
            plot_edges.append([point_a, point_b])
            corner_points.append(point_a)
            corner_points.append(point_b)
        else:
            plot_lines.append([point_a, point_b])
        i += 1
    return plot_edges, plot_lines, corner_points


# This is the main function - it returns the edges, lines, corners 
def get_edges_lines_corners_main(grid_spacing_front_to_back, grid_spacing_left_to_right, do_3d=False):
    """
    :param grid_spacing_front_to_back:
    :param grid_spacing_left_to_right:
    :param do_3d: boolean, should add 3d points (z=0) or not
    :return: plot_edges, plot_lines, corners
    """
    corr_linesX_x, corr_linesX_y = get_corr_lines(sum(grid_spacing_left_to_right), grid_spacing_front_to_back)

    corr_linesY_y, corr_linesY_x = get_corr_lines(sum(grid_spacing_front_to_back), grid_spacing_left_to_right)

    plot_edges, plot_lines, corner_points = get_edges_lines_corners_single_iteration(corr_linesX_x,
                                                                                     corr_linesX_y, do_3d)

    plot_edges_y, plot_lines_y, corner_points_y = get_edges_lines_corners_single_iteration(corr_linesY_x,
                                                                                           corr_linesY_y, do_3d)
    # Concatenate two lists
    plot_edges = plot_edges + plot_edges_y
    plot_lines = plot_lines + plot_lines_y
    corner_points = corner_points + corner_points_y
    corners = []
    for m in corner_points:
        if m not in corners:
            corners.append(m)
    return plot_edges, plot_lines, corners