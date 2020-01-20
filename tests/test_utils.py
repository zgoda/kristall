from kristall.utils import endpoint


class TestResource:
    pass


def test_endpoint_for_simple_instance():
    item = object()
    rv = endpoint(item)
    assert rv == 'builtins.object'


def test_endpoint_for_class_instance():
    item = TestResource()
    rv = endpoint(item)
    assert rv == 'tests.test_utils.TestResource'


def test_endpoint_for_class_object():
    rv = endpoint(TestResource)
    assert rv == 'tests.test_utils.TestResource'
