import json

import requests
from flexmock import flexmock

from eduxator import io


class TestEduxIO():

    def good_data(self, filename):
        with open('test/files/' + filename) as data_file:
            data = json.load(data_file)
        return data

    def fake_response(self, filename):
        with open('test/files/' + filename) as f:
            text = f.read()
        return flexmock(text=text, cookies=flexmock(get_dict=lambda: {}))

    def test_parsing_form(self):
        flexmock(requests).should_receive("get").once().and_return(self.fake_response('form.html'))
        e = io.EduxIO(cookie_dict={})
        data = e.parse_form_edit_score(url='whatever_the_response_is_mocked')
        for key, value in self.good_data('form.json').items():
            assert data[key] == value
