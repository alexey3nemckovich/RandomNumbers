import sys
import argparse
import collections
import LemerNumbersGenerator


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


GenerationParameters = collections.namedtuple('GenerationParameters', ['r0', 'a', 'm', 'n'])


def prepare_generation_parameters():
    if len(sys.argv) > 1:
        # parse args
        parser = create_args_parser()
        namespace = parser.parse_known_args(sys.argv[1:])

        return GenerationParameters(
            r0=namespace.r0,
            a=namespace.a,
            m=namespace.m,
            n=namespace.n
        )
    else:
        n = 2 ** 21  # 2097152
        m = n - 1
        a = n - 2
        r0 = m - 1
        return GenerationParameters(r0=r0, a=a, m=m, n=n)


if __name__ == '__main__':
    params = prepare_generation_parameters()

    # init generator
    lemerGenerator = LemerNumbersGenerator.LemerNumbersGenerator(
        params.r0,
        params.a,
        params.m
    )

    # generating n numbers
    for i in (0, params.n - 1):
        print(lemerGenerator.next_number())
