from .base import BaseTest, RepresentativeBaseTest, ThemeBaseTest


class PositionFormTest(BaseTest):
    url = '/'

    def test_position_form(self):
        self.client.cookies['csrftoken'] = 'csrftoken'
        self.selector_test('#add-position-form form')

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
