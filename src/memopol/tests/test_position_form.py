import copy
import datetime

from .base import BaseTest, RepresentativeBaseTest, ThemeBaseTest

from representatives_positions.models import Position


class PositionFormTest(BaseTest):
    url = '/'
    create_url = RepresentativeBaseTest.base_url % 'none'
    position_fixture = {
        'position-representative': 1,
        'position-datetime': '2016-09-01',
        'position-link': 'http://example.com/test',
        'position-kind': 'other',
        'position-score': '0',
        'position-title': 'position test title',
        'position-text': 'position test text',
        'position-themes': '1'
    }

    def test_select_representative(self):
        self.selector_test(
            '#add-position-form #id_position-representative option[selected]',
            RepresentativeBaseTest.base_url % 'none'
        )

    def test_select_theme(self):
        self.selector_test(
            '#add-position-form #id_position-themes input[checked]',
            ThemeBaseTest.base_url % 'none'
        )

    def test_create_position(self):
        response = self.client.post(self.create_url, self.position_fixture)

        self.assertResponseDiffEmpty(response, '#add-position-success')
        position = Position.objects.get(text='position test text')

        assert position.datetime == datetime.date(2016, 9, 1)
        assert position.representative.pk == \
            self.position_fixture['position-representative']
        assert position.link == self.position_fixture['position-link']
        assert ''.join(['%s' % t.pk for t in position.themes.all()]) == '1'
        assert position.published is False

    def test_create_position_without_representative(self):
        fixture = copy.copy(self.position_fixture)
        fixture.pop('position-representative')

        response = self.client.post(self.create_url, fixture)
        self.assertResponseDiffEmpty(response,
            '#add-position-form .has-error .form-control')
        assert response.context['position_form'].is_valid() is False

    def test_create_position_without_datetime(self):
        fixture = copy.copy(self.position_fixture)
        fixture.pop('position-datetime')

        response = self.client.post(self.create_url, fixture)
        self.assertResponseDiffEmpty(response,
            '#add-position-form .has-error .form-control')
        assert response.context['position_form'].is_valid() is False

    def test_create_position_without_link(self):
        fixture = copy.copy(self.position_fixture)
        fixture.pop('position-link')

        response = self.client.post(self.create_url, fixture)
        self.assertResponseDiffEmpty(response,
            '#add-position-form .has-error .form-control')
        assert response.context['position_form'].is_valid() is False
