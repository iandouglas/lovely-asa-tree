import json
import unittest
from unittest.mock import patch
from tests import assert_payload_field_type_value
from api import create_app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_cors(self):
        response = self.client.head('/')

        assert_payload_field_type_value(
            self,
            response.headers,
            'Access-Control-Allow-Origin',
            str,
            '*'
        )
        assert_payload_field_type_value(
            self,
            response.headers,
            'Access-Control-Allow-Headers',
            str,
            'Content-Type'
        )
        assert_payload_field_type_value(
            self,
            response.headers,
            'Access-Control-Allow-Methods',
            str,
            'GET, PATCH, POST, DELETE, OPTIONS'
        )
