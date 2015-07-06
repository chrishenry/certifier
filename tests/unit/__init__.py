# This file is part of Certifier.
# Copyright 2014, Behance Ops.

"""Some common testing functionality."""

# Use unittest2 on Python < 2.7.
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os
import sys
import random

sys.path.append("../../certifier")

class CertifierTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def random_name(self):

        # A shameless ripoff of the docker names generator
        # https://github.com/docker/docker/blob/master/pkg/namesgenerator/names-generator.go
        left = [
            "admiring",
            "adoring",
            "agitated",
            "angry",
            "backstabbing",
            "berserk",
            "boring",
            "clever",
            "cocky",
            "compassionate",
            "condescending",
            "cranky",
            "desperate",
            "determined",
            "distracted",
            "dreamy",
            "drunk",
            "ecstatic",
            "elated",
            "elegant",
            "evil",
            "fervent",
            "focused",
            "furious",
            "gloomy",
            "goofy",
            "grave",
            "happy",
            "high",
            "hopeful",
            "hungry",
            "insane",
            "jolly",
            "jovial",
            "kickass",
            "lonely",
            "loving",
            "mad",
            "modest",
            "naughty",
            "nostalgic",
            "pensive",
            "prickly",
            "reverent",
            "romantic",
            "sad",
            "serene",
            "sharp",
            "sick",
            "silly",
            "sleepy",
            "stoic",
            "stupefied",
            "suspicious",
            "tender",
            "thirsty",
            "trusting",
        ]

        right = [
            "albattani",
            "almeida",
            "archimedes",
            "ardinghelli",
            "babbage",
            "banach",
            "bardeen",
            "brattain",
            "shockley",
            "bartik",
            "bell",
            "blackwell",
            "bohr",
            "bose",
            "brown",
            "carson",
            "chandrasekhar",
            "colden",
            "cori",
            "cray",
            "curie",
            "darwin",
            "davinci",
            "einstein",
            "elion",
            "engelbart",
            "euclid",
            "fermat",
            "fermi",
            "feynman",
            "franklin",
            "galileo",
            "goldstine",
            "goodall",
            "hawking",
            "heisenberg",
            "hodgkin",
            "hoover",
            "hopper",
            "hypatia",
            "jang",
            "jones",
            "kilby",
            "noyce",
            "khorana",
            "kirch",
            "kowalevski",
            "lalande",
            "leakey",
            "lovelace",
            "lumiere",
            "mayer",
            "mccarthy",
            "mcclintock",
            "mclean",
            "meitner",
            "mestorf",
            "morse",
            "newton",
            "nobel",
            "payne",
            "pare",
            "pasteur",
            "perlman",
            "pike",
            "poincare",
            "poitras",
            "ptolemy",
            "raman",
            "ramanujan",
            "ritchie",
            "thompson",
            "rosalind",
            "saha",
            "sammet",
            "sinoussi",
            "stallman",
            "swartz",
            "tesla",
            "torvalds",
            "turing",
            "wilson",
            "wozniak",
            "wright",
            "yalow",
            "yonath",
        ]

        return random.choice(left) + "_" + random.choice(right) + "_" + str(random.randrange(0, 100000000))
