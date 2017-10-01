import sys
import argparse
import collections
import math
from enum import Enum
from LemerNumbersGenerator import LemerNumbersGenerator
from SequenceAlanization import SequencePeriodicProperties
from SequenceAlanization import calc_periodical_properties
from SequenceAlanization import build_bar_chart


def create_args_parser():
    parser = argparse.ArgumentParser(
        description='Lemer numbers geneator'
    )
    required_args = parser.add_argument_group('required named arguments')
    required_args.add_argument('--r0', type=int, help='Initial generator number', required=False)
    required_args.add_argument('--a', type=int, help='Number to multiply prev generator value', required=False)
    required_args.add_argument('--m', type=int, help='Generated numbers up limit', required=False)
    required_args.add_argument('--n', '--count', type=int, help='Count numbers to generate', required=False)
    return parser


GenerationParameters = collections.namedtuple('GenerationParameters', ['r0', 'a', 'm', 'n', 'mode'])


class WorkMode(Enum):
    SEARCHING_GOOD_PERIOD = 1
    OBTAIN_STATISTICS = 2


def prepare_generation_parameters():
    if len(sys.argv) > 1:
        # parse args
        parser = create_args_parser()
        namespace = parser.parse_known_args(sys.argv[1:])

        return GenerationParameters(
            r0=namespace[0].r0,
            a=namespace[0].a,
            m=namespace[0].m,
            n=namespace[0].n,
            mode=WorkMode.OBTAIN_STATISTICS
        )
    else:
        return GenerationParameters(0, 0, 0, 0, mode=WorkMode.SEARCHING_GOOD_PERIOD)


def search_big_period():
    expected_period = 50000

    degree = round(math.log(expected_period, 2))
    if 2 ** degree < expected_period:
        expected_period += 1

    n = 2 ** (degree + 1)

    m = 2 ** 32 - 1
    a = 16807

    r0 = 1

    generated_numbers = []
    periodic_properties = SequencePeriodicProperties(0, 0, 0)

    lemer_generator = LemerNumbersGenerator()
    while periodic_properties.period_length < expected_period:
        #init generator
        lemer_generator.set_generator_parameters(r0, a, m)
        lemer_generator.reset()

        #generate numbers
        generated_numbers.clear()
        for i in range(0, n):
            generated_numbers.append(lemer_generator.next_number())

        #get results
        periodic_properties = calc_periodical_properties(generated_numbers)

        #correct parameters if not success
        if periodic_properties.period_found and periodic_properties.period_length < expected_period:
            a -= 1

    print_period_info(periodic_properties, expected_period)

    print("r0 = ", r0)
    print("a = ", a)
    print("m = ", m)


def obtain_statistics(params):
    # init generator
    lemer_generator = LemerNumbersGenerator(
        params.r0,
        params.a,
        params.m
    )

    # generating n numbers
    m = 0
    d = 0
    generated_numbers = []
    for i in range(0, params.n):
        new_number = lemer_generator.next_number()

        if i > 0:
            d = d * ((i - 1) / i) + ((new_number - m) ** 2) / (i + 1)

        if i == 0:
            m = new_number
        else:
            m = m * (i / (i + 1)) + new_number / (i + 1)

        generated_numbers.append(new_number)

    build_bar_chart(generated_numbers, 20)
    count_els_in_quadrant = find_count_elements_located_in_quadrant(generated_numbers)
    periodic_properties = calc_periodical_properties(generated_numbers)

    v = count_els_in_quadrant / int(params.n / 2)

    print("M = ", m)
    print("D = ", d)
    print("Pi/4 = ", math.pi / 4)
    print("Count pairs located in quadrant to all pairs = ", v)
    print_period_info(periodic_properties, params.n)


def find_count_elements_located_in_quadrant(sequence):
    count = 0

    i = 0
    n = len(sequence)
    while i < n:
        if i != n - 1:
            if (sequence[i] ** 2 + sequence[i+1] ** 2) < 1:
                count += 1
        i += 2

    return count


def print_period_info(info, n):
    if info.period_found:
        print("Result period = ", info.period_length)
        print("Result aperiodic length = ", info.aperiodic_length)
    else:
        print("Period is larger than ", n)


if __name__ == '__main__':
    params = prepare_generation_parameters()

    if WorkMode.SEARCHING_GOOD_PERIOD == params.mode:
        search_big_period()
    else:
        obtain_statistics(params)
