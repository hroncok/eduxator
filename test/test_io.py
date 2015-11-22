import json

import pytest
import requests
from flexmock import flexmock

from eduxator import io


class TestEduxIO():

    def good_data(self, filename):
        with open('test/files/' + filename + '.json') as data_file:
            data = json.load(data_file)
        return data

    def fake_response(self, filename, url=''):
        with open('test/files/' + filename + '.html') as f:
            text = f.read()
        return flexmock(text=text, cookies=flexmock(get_dict=lambda: {}), url=url)

    def test_parsing_form(self):
        url = 'https://edux.fit.cvut.cz/courses/BI-3DT/' + \
              'classification/view/fulltime/tutorials/3?do=edit'
        flexmock(io.EduxIO).should_receive('get').with_args(url).once().and_return(
            self.fake_response('form', url=url))
        e = io.EduxIO(cookie_dict={})
        e.course = 'BI-3DT'
        e.classpath = ('fulltime', 'tutorials', '3')
        data = e.parse_form_edit_score()
        for key, value in self.good_data('form').items():
            assert data[key] == value

    def test_sending_form(self):
        url = 'https://edux.fit.cvut.cz/courses/BI-3DT/classification/view/fulltime/tutorials/3'
        flexmock(io.EduxIO).should_receive('post').with_args(url, {}).once()
        e = io.EduxIO(cookie_dict={})
        e.course = 'BI-3DT'
        e.classpath = ('fulltime', 'tutorials', '3')
        e.submit_form_edit_score({})

    def test_parsing_courses(self):
        flexmock(requests).should_receive('get').once().and_return(self.fake_response('courses'))
        e = io.EduxIO(cookie_dict={})
        assert sorted(self.good_data('courses')) == sorted(e.parse_courses_list())

    @pytest.mark.parametrize('course', ('BI-3DT', 'BI-3DT.1'))
    def test_parsing_calssification(self, course):
        url = 'https://edux.fit.cvut.cz/courses/{}/classification/view/start'
        url1 = url.format(course)
        url2 = url.format('BI-3DT')
        flexmock(io.EduxIO).should_receive('get').with_args(url1).once().and_return(
            self.fake_response('classification', url=url2))
        e = io.EduxIO(cookie_dict={})
        e.course = course
        tree = e.parse_classification_tree()
        assert e.course == 'BI-3DT'
