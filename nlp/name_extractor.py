#
#  name_extractor.py
#  ATOM
#
#  Created by Karthik V.
#  Updated copyright on 16/1/19 5:54 PM.
#
#  Copyright © 2019 Karthik Venkatesh. All rights reserved.
#

# Reference
# Question link: https://stackoverflow.com/questions/20290870/improving-the-extraction-of-human-names-with-nltk
# Answer link: https://stackoverflow.com/a/49500219/5019015

import nltk
from nltk.corpus import wordnet


class NameExtractor:

    @staticmethod
    def download_required_packages():
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
        nltk.download('wordnet')

    @staticmethod
    def get_human_names(text):
        tokens = nltk.tokenize.word_tokenize(text)
        pos = nltk.pos_tag(tokens)
        sent = nltk.ne_chunk(pos, binary=False)

        person_list = []
        person = []
        name = ""

        for subtree in sent.subtrees(filter=lambda t: t.label() == 'PERSON'):
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 0:
                for part in person:
                    name += part + ' '
                if name[:-1] not in person_list:
                    person_list.append(name[:-1])
                name = ''
            person = []

        person_names = person_list
        for person in person_list:
            person_split = person.split(" ")
            for name in person_split:
                if wordnet.synsets(name):
                    if name in person:
                        person_names.remove(person)
                        break

        return person_names

    @staticmethod
    def extract_names(text: str):
        names = NameExtractor.get_human_names(text)
        return names
