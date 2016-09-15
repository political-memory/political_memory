from datetime import date, timedelta

from django import test
from django.db import connection

from memopol_settings.models import Setting


class DecayFunctionTest(test.TestCase):
    def decay_score(self, score, date, num, denom, exponent, decimals):
        with connection.cursor() as cursor:
            cursor.execute('SELECT decay_score(%s, %s, %s, %s, %s, %s);',
                           [score, date, num, denom, exponent, decimals])
            return float([row[0] for row in cursor.fetchall()][0])

    def do_decay_test(self, num, denom, exp, decs, days, scores):
        def decayed(score, date):
            return self.decay_score(score, date, num, denom, exp, decs)

        for d, s in zip(days, scores):
            assert decayed(100, date.today() - timedelta(d)) == s

    def test_no_decay(self):
        self.do_decay_test(
            0, 1, 1, 0,
            (0, 31, 355, 375, 730, 3650),
            (100, 100, 100, 100, 100, 100)
        )

    def test_normal_decay(self):
        self.do_decay_test(
            1, 365, 1, 0,
            (0, 31, 355, 375, 730, 3650),
            (100, 99, 39, 35, 2, 0)
        )

    def test_decimals(self):
        self.do_decay_test(
            1, 365, 1, 2,
            (0, 31, 355, 375, 730, 3650),
            (100, 99.28, 38.83, 34.8, 1.83, 0)
        )

    def test_extreme_decay(self):
        self.do_decay_test(
            1, 365, 100, 0,
            (0, 31, 355, 375, 730, 3650),
            (100, 100, 100, 0, 0, 0)
        )
