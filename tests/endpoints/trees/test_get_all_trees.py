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
    def test_happypath_get_all_trees(self):
        response = self.client.get(
            f'/api/v1/trees'
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type_value(self, data, 'count', int, 25)
        assert_payload_field_type(self, data, 'trees', list)

        results = data['trees']

        next_result = results[0]
        assert_payload_field_type_value(
            self, next_result, 'name', str,
            'Ellcrys, "The Shannara Chronicles"'
        )
        assert_payload_field_type_value(
            self, next_result, 'description', str,
            'Telepathic, magical elf trees are always pretty rad, but poor '
            'Ellcrys tends to get completely overshadowed by all the other '
            'white trees in fantasy pop culture, of which there are many.'
        )
        assert_payload_field_type_value(
            self, next_result, 'image_url', str,
            'https://ugc.reveliststatic.com/gen/full/2016/04/27/14/9j/7l/'
            'pogmddl0ws39.gif'
        )


