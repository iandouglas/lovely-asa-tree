from sqlalchemy import MetaData, ForeignKeyConstraint, Table
from sqlalchemy.engine import reflection
from sqlalchemy.sql.ddl import DropConstraint, DropTable


def assert_payload_field_type_value(obj, payload, field, data_type, value):  # pragma: no cover
    obj.assertIn(field, payload)
    obj.assertIsInstance(payload[field], data_type)
    obj.assertEqual(value, payload[field])


def assert_payload_field_type(obj, payload, field, data_type):  # pragma: no cover
    obj.assertIn(field, payload)
    obj.assertIsInstance(payload[field], data_type)
