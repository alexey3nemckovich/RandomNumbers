import sys
import argparse
import collections
import math
from enum import Enum
from LemerNumbersGenerator import LemerNumbersGenerator
from SequenceAlanization import SequencePeriodicProperties
from SequenceAlanization import calc_periodical_properties
from SequenceAlanization import build_bar_chart


def distribution_type_parser():
    parser = argparse.ArgumentParser(
        description='Distribution simulator'
    )
    required_args = parser.add_argument_group('required named arguments')
    required_args.add_argument('--name', help='Distribution name', required=True)
    return parser


def create_distribution_args_parser(distribution_name):
    parser = argparse.ArgumentParser(
        description=distribution_name + ' distribution'
    )
    required_args = parser.add_argument_group('required named arguments')
    locals()['add_' + distribution_name + '_distribution_args'](required_args)
    required_args.add_argument('--n', '--count', type=int, help='Count numbers to generate', required=True)
    return parser


def add_even_distribution_args(required_args):
    required_args.add_argument('--a', type=float, help='Left generated numbers bound including', required=True)
    required_args.add_argument('--b', type=float, help='Right generated numbers bound not including', required=True)


def add_gauss_distribution_args(required_args):
    required_args.add_argument('--m', type=float, help='Math expectation', required=True)
    required_args.add_argument('--s', type=float, help='Standard deviation', required=True)


def add_exponent_distribution_args(required_args):
    required_args.add_argument('--h', type=float, help='Generator parameter', required=False)


def add_hamma_distribution_args(required_args):
    required_args.add_argument('--h', type=float, help='Exponent generator parameter', required=False)
    required_args.add_argument('--c', type=int, help='Count random numbers to sum', required=False)


def add_triangle_distribution_args(required_args):
    required_args.add_argument('--a', type=float, help='Left generated numbers bound including', required=True)
    required_args.add_argument('--b', type=float, help='Right generated numbers bound not including', required=True)
    required_args.add_argument('--m', type=int, help='Number of distribution density(0/1)', required=True)


def add_simpson_distribution_args(required_args):
    required_args.add_argument('--a', type=float, help='Left generated numbers bound including', required=True)
    required_args.add_argument('--b', type=float, help='Right generated numbers bound not including', required=True)


def prepare_data():
    parser = distribution_type_parser()
    namespace = parser.parse_known_args(sys.argv[1:])
    distribution_args_parser = create_distribution_args_parser(namespace[0].name)


def obtain_statistics(generator, n):
    m = 0
    d = 0
    generated_numbers = []

    for i in range(n):
        new_number = generator.next_number()

        if i > 0:
            d = d * ((i - 1) / i) + ((new_number - m) ** 2) / (i + 1)

        if i == 0:
            m = new_number
        else:
            m = m * (i / (i + 1)) + new_number / (i + 1)

        generated_numbers.append(new_number)

    print("M = ", m)
    print("D = ", d)
    build_bar_chart(generated_numbers, 20)


if __name__ == '__main__':
    data = prepare_data()
    obtain_statistics(data.generator, data.n)
