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

    def fake_response(self, filename):
        with open('test/files/' + filename + '.html') as f:
            text = f.read()
        return flexmock(text=text, cookies=flexmock(get_dict=lambda: {}))

    @pytest.mark.parametrize('argument', (True, False))
    def test_parsing_form(self, argument):
        url = 'https://edux.fit.cvut.cz/courses/BI-3DT/' + \
              'classification/view/fulltime/tutorials/3?do=edit'
        flexmock(io.EduxIO).should_receive('get').with_args(url).once().and_return(
            self.fake_response('form'))
        e = io.EduxIO(cookie_dict={})
        if argument:
            data = e.parse_form_edit_score(course='BI-3DT',
                                           classpath=('fulltime', 'tutorials', '3'))
        else:
            e.course = 'BI-3DT'
            e.classpath = ('fulltime', 'tutorials', '3')
            data = e.parse_form_edit_score()
        for key, value in self.good_data('form').items():
            assert data[key] == value
        assert e.course == 'BI-3DT'
        assert e.classpath == ('fulltime', 'tutorials', '3')

    @pytest.mark.parametrize('argument', (True, False))
    def test_sending_form(self, argument):
        url = 'https://edux.fit.cvut.cz/courses/BI-3DT/classification/view/fulltime/tutorials/3'
        flexmock(io.EduxIO).should_receive('post').with_args(url, {}).once()
        e = io.EduxIO(cookie_dict={})
        if argument:
            e.submit_form_edit_score({}, course='BI-3DT',
                                     classpath=('fulltime', 'tutorials', '3'))
        else:
            e.course = 'BI-3DT'
            e.classpath = ('fulltime', 'tutorials', '3')
            e.submit_form_edit_score({})
        assert e.course == 'BI-3DT'
        assert e.classpath == ('fulltime', 'tutorials', '3')

    def test_parsing_courses(self):
        flexmock(requests).should_receive('get').once().and_return(self.fake_response('courses'))
        e = io.EduxIO(cookie_dict={})
        assert sorted(self.good_data('courses')) == sorted(e.parse_courses_list())

    @pytest.mark.parametrize('argument', (True, False))
    def test_parsing_calssification(self, argument):
        url = 'https://edux.fit.cvut.cz/courses/BI-3DT/classification/view/start'
        flexmock(io.EduxIO).should_receive('get').with_args(url).once().and_return(
            self.fake_response('classification'))
        e = io.EduxIO(cookie_dict={})
        if argument:
            tree = e.parse_classification_tree('BI-3DT')
        else:
            e.course = 'BI-3DT'
            tree = e.parse_classification_tree()
        assert e.course == 'BI-3DT'
        assert tree == self.good_data('classification')
