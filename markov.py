"""A Markov chain generator that can tweet random messages."""

import sys
from random import choice
import os
import discord

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    text = open(file_path).read()

    return text
    


def make_chains(text_string, chains=None):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains('hi there mary hi there juanita')

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    if not chains:
        chains = {}

    words = text_string.split(" ")

    for i in range(len(words)-2):
        key_tuple = (words[i], words[i+1])
        next_word = words[i+2]
        # https://stackoverflow.com/questions/12905999/python-dict-how-to-create-key-or-append-an-element-to-key
        chains.setdefault(key_tuple,[next_word]).append(next_word)
    return chains


def make_text(chains, seed_word):
    """Return text from chains."""

    possible_seed_tuples = []
    for each_key in chains:
        if each_key[0] == seed_word:
            possible_seed_tuples.append(each_key)
    try:
        seed_tuple = choice(possible_seed_tuples)
    except IndexError:
        return f"Uh oh; '{seed_word}' is not a good seed_word for this text."
    words = [f"{seed_tuple[0]} {seed_tuple[1]}"]

    while True:
        
        possible_values = chains.get(seed_tuple)

        try:
            seed_tuple = (seed_tuple[1], choice(possible_values))
            words.append(seed_tuple[1])
        except TypeError:
            break

    return ' '.join(words)

def text_blender(input_path_or_paths):
    """ Blend a single file, or a list of files.

    'gettysburg.txt', 'green-eggs.txt', 'the_boy_who_lived.txt'"""

    input_paths = input_path_or_paths
    if isinstance(input_path_or_paths, str):
        input_paths = [input_path_or_paths]

    seed_words = []
    chains = {}
    for input_path in input_paths:
        # Open the file and turn it into one long string
        try:
            input_text = open_and_read_file(input_path)
        except FileNotFoundError:
            print(f"Uh oh; '{input_path}' is not a good input_path.\n")
            continue

        # Just make the seed word the first word of the text. Makes text natural-sounding.
        seed_words.append(input_text.split(" ")[0])

        # Get a Markov chain
        chains = make_chains(input_text, chains)

    # Produce random text
    random_text = make_text(chains, choice(seed_words))

    return random_text




client = discord.Client()


@client.event
async def on_ready():
    print(f'Successfully connected! Logged in as {client.user}.')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    a_presidential_message = text_blender(['biden_on_covid19.txt', 'clinton_impeachment.txt', 'reagan_sold_weapons.txt', 'nixon_resignation.txt'])
    await message.channel.send(a_presidential_message[:1000])

client.run(os.environ['DISCORD_TOKEN'])
