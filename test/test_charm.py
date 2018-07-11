# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=invalid-name, too-few-public-methods, bad-continuation

"""Test cases for the charm module"""

from __future__ import unicode_literals
from __future__ import print_function

import logging # pylint: disable=unused-import
import unittest

from helpers import centos, docker, ubuntu

from hpccm.charm import charm

class Test_charm(unittest.TestCase):
    def setUp(self):
        """Disable logging output messages"""
        logging.disable(logging.ERROR)

    @ubuntu
    @docker
    def test_defaults(self):
        """Default charm building block"""
        c = charm()
        self.assertEqual(str(c),
r'''# Charm++ version 6.8.2
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        git \
        make \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp http://charm.cs.illinois.edu/distrib/charm-6.8.2.tar.gz && \
    mkdir -p /usr/local && tar -x -f /var/tmp/charm-6.8.2.tar.gz -C /usr/local -z && \
    cd /usr/local/charm-v6.8.2 && ./build charm++ multicore-linux-x86_64 --build-shared --with-production -j4 && \
    rm -rf /var/tmp/charm-6.8.2.tar.gz
ENV CHARMBASE=/usr/local/charm-v6.8.2 \
    LD_LIBRARY_PATH=/usr/local/charm-v6.8.2/lib_so:$LD_LIBRARY_PATH \
    PATH=/usr/local/charm-v6.8.2/bin:$PATH''')

    @ubuntu
    @docker
    def test_runtime(self):
        """Runtime"""
        c = charm()
        r = c.runtime()
        s = '\n'.join(str(x) for x in r)
        self.assertEqual(s,
r'''# Charm++
COPY --from=0 /usr/local/charm-v6.8.2 /usr/local/charm-v6.8.2
ENV CHARMBASE=/usr/local/charm-v6.8.2 \
    LD_LIBRARY_PATH=/usr/local/charm-v6.8.2/lib_so:$LD_LIBRARY_PATH \
    PATH=/usr/local/charm-v6.8.2/bin:$PATH''')