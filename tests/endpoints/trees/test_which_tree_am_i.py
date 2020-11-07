import json
import unittest

from api import create_app
from tests import assert_payload_field_type_value, \
    assert_payload_field_type


class GetTreesTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()


class GetAllTreesTest(GetTreesTest):
    def test_happypath_which_tree_am_i(self):
        payload = {
            'name': 'dione'
        }
        response = self.client.post(
            '/api/v1/trees/which-am-i', json=payload,
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type(self, data, 'result', dict)

        next_result = data['result']
        assert_payload_field_type_value(
            self, next_result, 'name', str,
            'The Keebler Elf Tree'
        )
        assert_payload_field_type_value(
            self, next_result, 'description', str,
            'Can any of these other trees give you cookies? Definitely not.'
        )
        assert_payload_field_type_value(
            self, next_result, 'image_url', str,
            'https://ugc.reveliststatic.com/gen/constrain/800/800/80/2016/'
            '04/27/14/72/x3/po5rzeca8s39.jpg'
        )

    def test_happypath_which_tree_am_i_whitespace_mixed_case(self):
        payload = {
            'name': " D i O \t  n E  \n"
        }
        response = self.client.post(
            '/api/v1/trees/which-am-i', json=payload,
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(
            self, data['result'], 'name', str,
            'The Keebler Elf Tree'
        )

    def test_sadpath_missing_name(self):
        payload = {
        }
        response = self.client.post(
            '/api/v1/trees/which-am-i', json=payload,
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(
            self, data, 'error', str,
            'missing or empty "name" parameter'
        )

    def test_sadpath_blank_name(self):
        payload = {
            'name': ''
        }
        response = self.client.post(
            '/api/v1/trees/which-am-i', json=payload,
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(
            self, data, 'error', str,
            'missing or empty "name" parameter'
        )



