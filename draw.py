import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import logging
from operator import itemgetter

# [243, 362, 457, 915, 1048576]
capY = 362

x, y = [], []
y1, y2, y3, y4, tb = [], [], [], [], []


def validate_parameter(argv):
    log_file = ""
    if len(sys.argv) < 2:
         print("must specify filename")
         sys.exit(1)
    else:
        log_file = sys.argv[1]

     # create output directory if not exist
    if not os.path.exists(log_file):
        print('')
        os.exit(-1)

    return log_file


def read_log_file(log_file):
    global x, y, y1, y2, y3, y4, tb
    with open(log_file) as f:
        for i, line in enumerate(f):
            x.append(i)
            y.append(round(int(line.split()[1]) / 1048576, 2))
            y1.append(round(int(line.split()[2]) / 1048576, 2))
            y2.append(round(int(line.split()[3]) / 1048576, 2))
            y3.append(round(int(line.split()[4]) / 1048576, 2))
            y4.append(round(int(line.split()[5]) / 1048576, 2))
            tb.append(round(int(line.split()[6]) / 1048576, 2))


# trying to find a starting x point that we can start a new job, 
# and this job will not cause the disk usage exceed its capacity
def find_early_start_point(x_delta):
    x_tmp = [x_val + x_delta for x_val in x]
    starting_x = x_tmp[0]
    for i, v in enumerate(x[starting_x:]):
        yc = y[starting_x + i] + y[i]
        if yc > capY:
            return False
    return True


def get_try_x_points(starting_i):
    try_x_list = []
    for v in range(starting_i, len(x)):
        if find_early_start_point(v):
            try_x_list.append(v)

    logging.info(f"x len: {len(x)}, try_x_list len: {len(try_x_list)}")
    return try_x_list


def get_y_combined_from_try_x(try_x_list):
    try_x = 1
    try:
        try_x = try_x_list[0]
    except Exception as e:
        logging.error(f'Caught exception when dereferencing try_x_list: {e}')

    y_combined = [v[0] + v[1] for v in zip(y[try_x:], y)]

    # for every try_x, we start a new task from it
    # by calculating all combined y values, we pick the max y from them
    # compare all max y we collect from new tasks, we get a task with minimum max y

    max_y0, max_y_combined = [], []
    for tx in try_x_list:
        y_combined_try = [v[0] + v[1] for v in zip(y[tx:], y)]
        max_y0.append((tx, max(y_combined_try))) # {index, maxY_in_y_combined} pair
        max_y_combined.append(max(y_combined_try))

    logging.info(f"max y0 is {max_y0}")

    # resMin, resMax = min(max_y0, key=itemgetter(1))[0], max(max_y0, key=itemgetter(1))[0]
    # logging.info(f"resMin:{resMin}, resMax:{resMax}")

    return y_combined, max_y0, max_y_combined


# Green Line: Draw all possible max_y_combined
def draw_max_y_combined(try_x_list, max_y_combined):
    plt.plot(try_x_list, max_y_combined, '-', color='green', label='max_total')

# Black line:
def draw_y_combined(x0, y_combined):
    # draw peak point in y combined line
    y_combined_max = max(y_combined)
    x0_pos = y_combined.index(y_combined_max)
    x0_max = x0[x0_pos]
    plt.annotate('({}, {})'.format(x0_max, y_combined_max), xy=(x0_max, y_combined_max), xytext=(x0_max-25, y_combined_max+20),
        arrowprops=dict(arrowstyle='->', color='black',connectionstyle="arc,angleA=-90,angleB=180"))

    # draw starting point of y combined line (annotate)
    try_x = x0[0]
    plt.annotate('({}, {})'.format(try_x, y[try_x]), xy=(try_x, y[try_x]), xytext=(try_x-30, y[try_x]+10),
            arrowprops=dict(arrowstyle='->', color='black', connectionstyle="arc,angleA=-90,angleB=180"),)

    # draw vertical for starting point of y combined line
    plt.axvline(try_x, c='black', ls='--')

    plt.annotate('{}'.format(try_x), xy=(try_x, 0), xytext=(try_x-6, -9),color='red')

    # draw starting point of y combined line (circle)
    plt.plot(try_x, y[try_x], 'ow-', mec='r')
    plt.plot(x0, y_combined, 'k-', linewidth=2, label='combined')


def draw_y_range(capY):
    plt.ylim([0, capY])

def draw_task1():
    plt.plot(x, y, 'r-', label='task1')
    plt.axvline(x[-1], c='black', ls='--')

    # draw peak point in task1 (annotate)
    y_max = max(y)
    x_pos = y.index(y_max)
    x_max = x[x_pos]
    plt.annotate('({}, {})'.format(x_max, y_max), xy=(x_max, y_max), xytext=(x_max, y_max+20),
                arrowprops=dict(arrowstyle='->', color='red'),)

        # draw end point
    plt.annotate('({}, {})'.format(x[-1], y[-1]), xy=(x[-1], y[-1]), xytext=(x[-1]+3, y[-1]))
    plt.stem(x[-1], y[-1], 'ok--')
    plt.plot(x[-1], y[-1], 'ow-', mec='r')

def draw_task2(x0, y0):
    plt.plot(x0, y0, 'r-', label='task2')


def draw_p1():
    # move down a little bit so that it does not overlap task1's line
    global y1
    y_ = [v for v in y1]
    y1 = list(map(lambda v: v - 1,  y_))

    # draw max_xy in p1
    y1_max = max(y1)
    x1_pos = y1.index(y1_max)
    x1_max = x[x1_pos]
    plt.annotate('({}, {})'.format(x1_max, y1_max), xy=(x1_max, y1_max), xytext=(x1_max, y1_max+10),
                arrowprops=dict(arrowstyle='->', color='blue'),)

    # draw max_xy of task1 in p1
    y_max_p1 = max(y[:len(y1)])
    x_pos_p1 = y.index(y_max_p1)
    x_max_p1 = x[x_pos_p1]
    plt.annotate('({}, {})'.format(x_max_p1, y_max_p1), xy=(x_max_p1, y_max_p1), xytext=(x_max_p1, y_max_p1+20),
            arrowprops=dict(arrowstyle='->', color='red'),)

    # draw p1 line
    plt.plot(x, y1, '-', color='blue', label='p1')

def draw_p2():
    y2max = max(y2)
    x2pos = y2.index(y2max)
    x2max = x[x2pos]

    plt.annotate('({}, {})'.format(x2max, y2max), xy=(x2max, y2max), xytext=(x2max, y2max+10),
            arrowprops=dict(arrowstyle='->', color='blue'),)

    # draw p2 line
    plt.plot(x, y2, '-', color='tab:orange', label='p2')

def draw_p3():
    plt.plot(x, y3, '-', color='tab:brown', label='p3')

def draw_p4():
    plt.plot(x, y4, 'm-', label='p4')

def draw_table():
    plt.plot(x, tb, 'y-', label='tb')


# plt.stem(try_x, y[try_x], 'ok--')
# plt.setp(markerline, marker='o', color='black')

# plt.annotate('{}'.format(try_x), xy=(try_x, 0), xytext=(try_x-6, -9),color='red')

def draw_legend():
    plt.legend(frameon=False, loc='upper left', ncol=2)


def main(argv):
    read_log_file(validate_parameter(argv))
    draw_y_range(capY + 50)
    draw_task1()
    draw_p1()
    draw_p2()
    draw_p3()
    draw_p4()
    draw_table()

    try_x_list = get_try_x_points(1)
    if len(try_x_list) == 0:
        logging.warning(f"No valid starting point was found")
    else:
        y_combined, max_y0, max_y_combined = get_y_combined_from_try_x(try_x_list)
        draw_y_combined(x[try_x_list[0]:], y_combined)
        draw_max_y_combined(try_x_list, max_y_combined)

    draw_legend()
    plt.show()


if __name__ == "__main__":
    main(sys.argv)
