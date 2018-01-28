from unittest import TestCase
import requests
from mock import Mock

from configurations import RequestParameters
from services import RequesterService


class TestRequesterService(TestCase):
    def setUp(self):
        self.request_parameters = RequestParameters()
        self.request_parameters.key = "paramkey"
        self.request_parameters.locale = "testLocale"
        self.request_parameters.application = "application"
        self.request_parameters.secret = "super-secret"
        self.requester_service = RequesterService(request_parameters=self.request_parameters, base_url="http://127.0.0.1")
        response = requests.Response()
        response.status_code = 200
        self.get_mock = Mock(return_value=response)
        self.json_mock = Mock(return_value={"result": "OK"})
        response.json = self.json_mock
        requests.get = self.get_mock

    def test_request(self):
        response = self.requester_service.request("test/resource", {"key": "value"})
        self.assertDictEqual({"result": "OK"}, response)
        self.get_mock.assert_called_once_with(params={'key': 'value', 'locale': 'testLocale', 'apikey': 'paramkey'}, url='http://127.0.0.1/test/resource')

    def test_request_no_params(self):
        response = self.requester_service.request("test/resource", None)
        self.assertDictEqual({"result": "OK"}, response)
        self.get_mock.assert_called_once_with(params={'locale': 'testLocale', 'apikey': 'paramkey'}, url='http://127.0.0.1/test/resource')

