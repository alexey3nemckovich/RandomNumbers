import collections
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


PeriodInfo = collections.namedtuple('PeriodInfo', ['was_found', 'len'])
MinMaxInfo = collections.namedtuple('MinMaxInfo', ['min_el_index', 'max_el_index'])
SequencePeriodicProperties = collections.namedtuple('SequencePeriodicProperties', ['period_found', 'period_length', 'aperiodic_length'])


def calc_periodical_properties(sequence):
    period_info = find_period(sequence)

    if period_info.was_found:
        aperiodic_length = find_aperiodic_length(sequence, period_info.len)

        return SequencePeriodicProperties(
            period_found=True,
            period_length=period_info.len,
            aperiodic_length=aperiodic_length
        )
    else:
        return SequencePeriodicProperties(
            period_found=False,
            period_length=-1,
            aperiodic_length=-1
        )


def find_period(sequence):
    last_el = sequence[-1]
    n = len(sequence)

    match_elements_indexes = []

    i = 0
    count_matches = 0
    while count_matches < 2 and i < n:

        if last_el == sequence[i]:
            match_elements_indexes.append(i)
            count_matches += 1

        i += 1

    if len(match_elements_indexes) < 2:
        return PeriodInfo(
            was_found=False,
            len=-1
        )
    else:
        return PeriodInfo(
            was_found=True,
            len=match_elements_indexes[1] - match_elements_indexes[0]
        )


def find_aperiodic_length(sequene, period):
    i = 0
    n = len(sequene)
    while sequene[i] != sequene[i + period] and i < n:
        i += 1

    return period + i


def find_min_max_elements(sequence):
    n = len(sequence)

    min_ind = 0
    max_ind = 0
    for i in range(0, n):
        if sequence[i] > sequence[max_ind]:
            max_ind = i
            continue

        if sequence[i] < sequence[min_ind]:
            min_ind = i
            continue

    return MinMaxInfo(min_el_index=min_ind, max_el_index=max_ind)


def build_bar_chart(sequence, n_intervals):
    min_max_info = find_min_max_elements(sequence)

    interval_value = (sequence[min_max_info.max_el_index] - sequence[min_max_info.min_el_index]) / n_intervals

    intervals = []
    pair_min = sequence[min_max_info.min_el_index]
    for i in range(0, n_intervals):
        intervals.append(
            list((pair_min, pair_min + interval_value))
        )
        pair_min += interval_value

    for i in range(0, n_intervals):
        intervals[i].append(0)

    n = len(sequence)
    for el in sequence:
        for i in range(0, n_intervals):
            if intervals[i][0] <= el <= intervals[i][1]:
                intervals[i][2] += 1
                continue

    x = []
    y = []

    for i in range(0, n_intervals):
        x.append('{:03.2f} - {:03.2f}'.format(intervals[i][0], intervals[i][1]))
        y.append(intervals[i][2])

    y_pos = np.arange(len(x))

    plt.bar(y_pos, y, align='center', alpha=0.5)
    plt.xticks(y_pos, x)
    plt.ylabel('Count elements')
    plt.xlabel('Interval')
    plt.title('Distribution histogram')

    plt.show()
