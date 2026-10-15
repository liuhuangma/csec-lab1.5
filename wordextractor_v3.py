#!/usr/bin/env python3
import click
import requests
import re
from bs4 import BeautifulSoup


def get_html_of(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')
        exit(1)
    return resp.content.decode()


def get_all_words_from(url):
    html = get_html_of(url)
    soup = BeautifulSoup(html, 'html.parser')
    raw_text = soup.get_text()
    return re.findall(r'\w+', raw_text)


def count_occurrences_in(word_list, min_length=0):
    word_count = {}
    for word in word_list:
        if len(word) < min_length:
            continue
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] = word_count.get(word) + 1
    return word_count


def get_top_words_from(all_words, min_length=0):
    occurrences = count_occurrences_in(all_words, min_length)
    return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)


def mutate_word(word):
    mutations = set()
    mutations.add(word.lower())
    mutations.add(word.upper())
    mutations.add(word.capitalize())
    suffixes = ['2019', '1!', '2!', '3!', '01', '123']
    for suffix in suffixes:
        mutations.add(word + suffix)
        mutations.add(word.capitalize() + suffix)
        mutations.add(word.upper() + suffix)
    return mutations


@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.')
@click.option('--length', '-l', default=0, help='Minimum word length (default: 0, no limit).')
@click.option('--output', '-o', default=None, help='Output file path (default: print to console).')
def main(url, length, output):
    the_words = get_all_words_from(url)
    top_words = get_top_words_from(the_words, length)

    result_lines = []
    for word, count in top_words[:10]:
        for mutated in sorted(mutate_word(word)):
            result_lines.append(mutated)

    if output:
        with open(output, 'w') as f:
            for line in result_lines:
                f.write(line + '\n')
        print(f'Results written to {output}')
    else:
        for line in result_lines:
            print(line)


if __name__ == '__main__':
    main()