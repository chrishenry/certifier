# This file is part of Certifier.
# Copyright 2015, Behance Ops.

"""Tests for the the EC2 service class"""

import os
import sys
import time
import ConfigParser
from tests.unit import CertifierTestCase
import random
import sure
import mock
from mock import patch
from mock import Mock
from nose.plugins.attrib import attr

import boto.ec2.elb as elb


from moto import mock_elb

from certifier.elb import *

class ElbTestCase(CertifierTestCase):

    creds = {
        'aws_access_key_id': '',
        'aws_secret_access_key': ''
    }

    def setUp(self):
        super(ElbTestCase, self).setUp()

    @attr(elb=True)
    @mock_elb
    def test_get_empty_elbs(self):

        elbs = get_elbs(self.creds)
        elbs.should.be.empty

        elbs = get_elbs(self.creds, region='us-west-2')
        elbs.should.be.empty

    @attr(elb=True)
    @mock_elb
    def test_get_elbs(self):

        for x in range(1,51):
            self.create_elb()

        elbs = get_elbs(self.creds)
        len(elbs).should.equal(50)

    def create_elb(self):

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

        name = random.choice(left) + "_" + random.choice(right)

        conn = elb.connect_to_region('us-east-1')
        hc = elb.HealthCheck(
            interval=20,
            healthy_threshold=3,
            unhealthy_threshold=5,
            target='HTTP:8080/health'
        )

        zones = ['us-east-1a', 'us-east-1b']
        ports = [(80, 8080, 'http'), (443, 8443, 'tcp')]
        lb = conn.create_load_balancer(name, zones, ports)

        lb.configure_health_check(hc)

