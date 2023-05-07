"""This file generates sequences of text based on other texts. It's not great but it's a toy to show a friend.
"""
from random import random, shuffle
data = open("norvig.txt", "r").read().lower()


def get_prob(text, num_chars):
    counts = {}
    for index in range(len(text) - num_chars - 1):
        if text[index:index+num_chars] in counts:
            if text[index+num_chars:index+num_chars+1] in counts[text[index:index+num_chars]]:
                counts[text[index:index+num_chars]
                       ][text[index+num_chars:index+num_chars+1]] += 1
            else:
                counts[text[index:index+num_chars]
                       ][text[index+num_chars:index+num_chars+1]] = 1
        else:
            counts[text[index:index+num_chars]] = {
                text[index+num_chars:index+num_chars+1]: 1
            }
    for key in counts:
        for char in counts[key]:
            counts[key][char] /= (len(text) - num_chars)
    return counts


def get_next_char(text_so_far, probs):
    num_chars = len(text_so_far)
    probs_index = 0
    expecteds = []
    while probs_index < num_chars and probs_index < len(probs):
        if text_so_far[-(probs_index+1):] in probs[probs_index]:
            expecteds.append(probs[probs_index][text_so_far[len(text_so_far)-probs_index-1:]])
        probs_index += 1
    char_predictions = {}
    for prob in expecteds:
        for char in prob:
            try:
                char_predictions[char] += prob[char]
            except:
                char_predictions[char] = prob[char]
    selection_list = []
    for char in char_predictions:
        selection_list.append([char_predictions[char], char])
    selection_list.sort()
    # here is a magic number: 5
    # it's used to limit the number of possibilities to be considered for the next character
    # the infintessimal possibilities are eliminated this way.
    selection_list = selection_list[-5:]
    total_prob = sum([s[0] for s in selection_list])
    for selection in selection_list:
        selection[0] /= total_prob
    shuffle(selection_list)
    char_chooser = random()
    accumulator = 0
    char_index = 0
    while accumulator < char_chooser:
        accumulator += selection_list[char_index][0]
        char_index += 1
    return selection_list[char_index-1][1]


window_size = input("How many characters do you want to use to predict the next? (16GB of RAM caps out at 16 chars)\n")
probs = []
# for char_length in range(1, len(data) - 1):
for char_length in range(1, int(window_size)+1):
    print("processing for length", char_length)
    probs.append(get_prob(data, char_length))


while True:
    prompt = input("what do you want to complete?\n").lower()
    num_words = int(input("how many words?\n"))
    words = 0
    while words < num_words:
        prompt += get_next_char(prompt, probs)
        if prompt[-1] == ' ':
            words += 1
    print(prompt)
