"""Day 14: Restroom Redoubt

https://adventofcode.com/2024/day/14

"""


def parse_input(data):
    result = []
    for line in data.strip().split('\n'):
        line = line.replace('p=', '').replace('v=', '')
        p, v = line.split()
        px, py = p.split(',')
        vx, vy = v.split(',')
        result.append(
            ((int(px), int(py)), (int(vx), int(vy)))
        )
    return result


def move(p, v, p_max=(10, 6)):
    x, y = p
    dx, dy = v
    x_max, y_max = p_max

    nx, ny = x + dx, y + dy
    if dx < 0 and nx < 0:
        nx = x_max + nx + 1
    elif dx > 0 and nx > x_max:
        nx = nx - x_max - 1

    if dy < 0 and ny < 0:
        ny = y_max + ny + 1
    elif dy > 0 and ny > y_max:
        ny = ny - y_max - 1

    return nx, ny


def move_multiple(p, v, n, p_max=(10, 6)):
    while n:
        p = move(p, v, p_max)
        n -= 1
    return p


def calculate_is_in_quadrant(p, p_min, p_max):
    x, y = p
    x_min, y_min = p_min
    x_max, y_max = p_max
    return (
        x_min <= x <= x_max and
        y_min <= y <= y_max
    )


def count_positions_in_quadrant(positions, p_min, p_max):
    return sum([calculate_is_in_quadrant(p, p_min, p_max) for p in positions])


def get_quadrants(p_max):
    x_max, y_max = p_max
    return [
        ((0, 0), (x_max // 2 - 1, y_max // 2 - 1)),
        ((0, y_max // 2 + 1), (x_max // 2 - 1, y_max)),
        ((x_max // 2 + 1, 0), (x_max, y_max // 2 - 1)),
        ((x_max // 2 + 1, y_max // 2 + 1), (x_max, y_max)),
    ]


def solve(data, n=100, p_max=(10, 6)):
    result = 1
    data = parse_input(data)
    final_positions = []
    for i in data:
        new_p = move_multiple(i[0], i[1], n, p_max)
        final_positions.append(new_p)
    for qp_min, qp_max in get_quadrants(p_max):
        result *= count_positions_in_quadrant(final_positions, qp_min, qp_max)

    return result


def print_picture(points, p_max):
    x_max, y_max = p_max
    picture = ''
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            picture += '#' if (x, y) in points else '.'
        picture += '\n'
    print(picture)
    return picture


def solve2(data, n=100, p_max=(10, 6)):
    counter = 1
    data = parse_input(data)

    print_picture([x[0] for x in data], p_max)
    while counter < n:
        final_positions = []
        new_data = []
        for i in data:
            new_p = move(i[0], i[1], p_max)
            final_positions.append(new_p)
            new_data.append((new_p, i[1]))
        if (
            ((counter - 13) % 101 == 0) or
            ((counter - 65) % 103 == 0)
        ):
            print('-' * 100)
            print(counter)
            print('-' * 100)
            print_picture(final_positions, p_max)
            print('-' * 100)
        data = new_data
        counter += 1


if __name__ == '__main__':
    input_data = open('input_data.txt').read()

    result = solve(input_data, 100, (100, 102))
    print(f'Example1: {result}')

    result = solve2(input_data, 10_000, (100, 102))
    print(f'Example2: {result}')
