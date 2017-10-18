import sys
import argparse
import math
import Generators
from AttribtutedObject import AttributedObject
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
    method_name = 'add_' + distribution_name + '_distribution_args'
    globals()[method_name](required_args)
    required_args.add_argument('--n', '--count', type=int, help='Count numbers to generate', required=True)
    return parser


def add_even_distribution_args(required_args):
    required_args.add_argument('--a', type=float, help='Left generated numbers bound including', required=True)
    required_args.add_argument('--b', type=float, help='Right generated numbers bound not including', required=True)


def add_gaussian_distribution_args(required_args):
    required_args.add_argument('--m', type=float, help='Math expectation', required=True)
    required_args.add_argument('--s', type=float, help='Standard deviation', required=True)


def add_exponent_distribution_args(required_args):
    required_args.add_argument('--h', type=float, help='Generator parameter', required=False)


def add_hamma_distribution_args(required_args):
    required_args.add_argument('--h', type=float, help='Exponent generator parameter', required=False)
    required_args.add_argument('--c', type=int, help='Count random numbers to multiply', required=False)


def add_triangle_distribution_args(required_args):
    required_args.add_argument('--a', type=float, help='Left generated numbers bound including', required=True)
    required_args.add_argument('--b', type=float, help='Right generated numbers bound not including', required=True)
    required_args.add_argument('--alg', help='Algorithm of selection between random numbers(min/max)', required=True)


def add_simpson_distribution_args(required_args):
    required_args.add_argument('--a', type=float, help='Left generated numbers bound including', required=True)
    required_args.add_argument('--b', type=float, help='Right generated numbers bound not including', required=True)


def prepare_data():
    parser = distribution_type_parser()
    type_args = parser.parse_args(sys.argv[1:])
    distribution_name = type_args.name
    distribution_args_parser = create_distribution_args_parser(distribution_name)
    while True:
        try:
            distribution_args_parser.print_help()
            args_string = input("Enter parameters: ")
            args = distribution_args_parser.parse_args(args_string.split())
            break
        except:
            pass

    res = AttributedObject()
    generator_class_name = "Generators." + distribution_name.title() + "NumbersGenerator"
    res.generator = eval(generator_class_name)(args)
    res.n = args.n
    return res


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
    print("Standard deviation = ", math.sqrt(d))
    build_bar_chart(generated_numbers, 20)


if __name__ == '__main__':
    data = prepare_data()
    obtain_statistics(data.generator, data.n)
