# Copyright 2012 Nextdoor.com, Inc.
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

"""nd_service_registry Zookeeper Client Library

Copyright 2012 Nextdoor Inc."""

__author__ = 'matt@nextdoor.com (Matt Wise)'

import logging
from kazoo.client import KazooClient
from nd_service_registry.funcs import rate_limiter

# Our default variables
from version import __version__ as VERSION


class ZookeeperClient(KazooClient):
    """Shim-layer that provides some safety controls"""

    @rate_limiter(targetAvgTimeBetweenCalls=1, numCallsToAverage=50)
    def retry(self, *args, **kwargs):
        return super(ZookeeperClient, self).retry(*args, **kwargs)

    @rate_limiter(targetAvgTimeBetweenCalls=1, numCallsToAverage=50)
    def get(self, *args, **kwargs):
        return super(ZookeeperClient, self).get(*args, **kwargs)

    @rate_limiter(targetAvgTimeBetweenCalls=10, numCallsToAverage=50)
    def set(self, *args, **kwargs):
        return super(ZookeeperClient, self).set(*args, **kwargs)

    @rate_limiter(targetAvgTimeBetweenCalls=10, numCallsToAverage=50)
    def create(self, *args, **kwargs):
        return super(ZookeeperClient, self).create(*args, **kwargs)

    @rate_limiter(targetAvgTimeBetweenCalls=10, numCallsToAverage=50)
    def delete(self, *args, **kwargs):
        return super(ZookeeperClient, self).delete(*args, **kwargs)


class KazooFilter(logging.Filter):
    """Filters out certain Kazoo messages that we do not want to see."""
    def filter(self, record):
        retval = True

        # Filter out the PING messages
        if record.getMessage().find('PING') > -1:
            retval = False

        return retval
