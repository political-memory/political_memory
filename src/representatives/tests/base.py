import copy
import logging
import re

from django import test
from django.core.serializers.json import Deserializer


class TestBase(test.TestCase):
    logger = logging.getLogger('representatives')

    _exclude = ('id', '_state', 'created', 'updated', 'fingerprint')
    _exclude_re = (re.compile(r'^_.*_cache$'),)

    def assertObjectsFromFixture(self, fixture):
        missing = []

        with open(fixture, 'r') as f:
            for obj in Deserializer(f.read()):
                compare = copy.copy(obj.object.__dict__)

                for field in self._exclude:
                    if field in compare:
                        compare.pop(field)

                for re in self._exclude_re:
                    for field in compare.keys():
                        if re.match(field):
                            compare.pop(field)

                try:
                    type(obj.object).objects.get(**compare)
                except:
                    self.logger.warn(
                        'MISSING %s\n   %s' % (type(obj.object), compare))
                    missing.append(compare)

        assert len(missing) is 0
