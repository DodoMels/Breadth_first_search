import h5py
import numpy as np
import matplotlib.pyplot as plt


def get_neighbours(position, grid, traversed):
    result = set()
    x, y = position
    # find the neighbours
    for x_offset in [-1, 1]:
        for y_offset in [-1, 1]:
            new_x = x - x_offset
            new_y = y - y_offset
            try:
                wall = grid[new_x][new_y]
                # check if the new neighbours hits the wall
                if not wall and (new_x, new_y) not in traversed:
                    result.add((new_x, new_y))
            except IndexError:
                continue
    return list(result)


def breadth_first_search(from_coord, to_coord, blocked):
    # initialisation
    traversed = set()
    traversed.add(from_coord)
    # get the first neighbours
    hood = {from_coord: get_neighbours(from_coord, blocked, traversed)}
    trip = {from_coord: []}
    step_counter = 0
    found = False
    rounds = 0
    # loop until endpoint found
    while not found:
        circle = []
        endpoints = set()
        for position in list(hood.keys()):
            # count the calculation steps for new neigbours around one coordinate
            rounds += 1
            if rounds % 100:
                print(f"\rRound {rounds}", end="")
            step_counter += 1
            # get the neighbour around one coordinate
            for neighbour in hood[position]:
                # when neighbour already found ignore
                if neighbour in traversed:
                    continue
                circle.append(neighbour)
                trip[neighbour] = []
                # trip of the search method
                trip[neighbour].append(position)
                # show the new neighbours from the next coordinate
                if trip[position]:
                    trip[neighbour] += trip[position]
                new_neighbours = get_neighbours(neighbour, blocked, traversed)
                # save the the new neighbours
                if new_neighbours:
                    hood[neighbour] = new_neighbours
                endpoints = endpoints.union(set(new_neighbours))
                traversed = traversed.union(set(hood))
                # cancel of the search loop
                if neighbour == to_coord:
                    found = True

    return trip[to_coord]


if __name__ == '__main__':
    # Load recorded data
    with h5py.File('data/map.hdf5', 'r') as hf:
        center = np.asarray(hf.attrs['center'])
        blocksize = np.asarray(hf.attrs['blocksize'])
        grid = np.asarray(hf['grid'])

    # Unknown fields are considered as blocked, too
    blocked = grid >= 0
    from_coord = (53, 16)
    to_coord = (43, 102)


    path = breadth_first_search(from_coord, to_coord, blocked)

    _, ax = plt.subplots()
    ax.set_title('Obstacle map')
    ax.imshow(blocked)
    for step in path:
        ax.plot(step[1], step[0], 'bo--',)
    ax.plot(from_coord[1], from_coord[0], 'ro')
    ax.plot(to_coord[1], to_coord[0], 'go')
    plt.show()


