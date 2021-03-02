import argparse
import sys

WRONG_SEPARATOR_ERROR_MESSAGE = '''
!!! Error !!!
Not every line in file is formatted this way: '[number] [chars]'
     OR
Separator %r is not used in file %r!
Please change the separator through the --separator parameter to the separator in the file used.
!!! Please notice that both files must use the same separator !!!'''


def parse_content(content, separator):
    try:
        return {line.split(separator, 1)[0]: line.split(separator, 1)[1] for line in content.splitlines()}
    except IndexError:
        raise ValueError('Separator is not used')


def process_data(base_file, sub_file, out_file, separator):
    print('Processing data ...')
    try:
        with open(base_file) as larger:
            larger = parse_content(larger.read(), separator)
    except ValueError:
        print(WRONG_SEPARATOR_ERROR_MESSAGE % (separator, base_file), file=sys.stderr)
        exit(1)

    try:
        with open(sub_file) as smaller:
            smaller = parse_content(smaller.read(), separator)
    except ValueError:
        print(WRONG_SEPARATOR_ERROR_MESSAGE % (separator, sub_file), file=sys.stderr)
        exit(1)

    difference = set(larger.keys()) - set(smaller.keys())
    output_dict = {k: v for k, v in larger.items() if k in difference}

    with open(out_file, "w") as output_file:
        print(*(separator.join(x) for x in output_dict.items()), sep='\n', end='', file=output_file)
    print('Data processed successfully!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base-file', required=True)
    parser.add_argument('-s', '--sub-file', required=True)
    parser.add_argument('-o', '--out-file', required=True)
    parser.add_argument('--separator', required=False, default='\t')
    process_data(**vars(parser.parse_args()))
