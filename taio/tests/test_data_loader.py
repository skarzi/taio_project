import os

import pytest

from taio.data_loader import DataLoader


TEST_DATA_DIRECTORY = os.path.join(
    os.path.dirname(__file__),
    '..', '..', 'data',
)


@pytest.fixture()
def data_loader():
    return DataLoader()


def path_to_test(fname):
    return os.path.join(TEST_DATA_DIRECTORY, fname)


class TestDataLoader:
    @pytest.mark.parametrize('test_filepath, expected', [
        (
            'test_data_0.txt',
            {
                'info': (3, 3, 3),
                'workers': [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                'projects': [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            },
        ),
        (
            'test_data_3.txt',
            {
                'info': (3, 3, 2),
                'workers': [[1, 1, 0], [0, 1, 0], [0, 1, 1]],
                'projects': [[1, 3, 0], [1, 0, 1]],
            },
        ),
        (
            'test_data_4.txt',
            {
                'info': (4, 3, 2),
                'workers': [[1, 0, 0], [1, 1, 0], [0, 1, 1], [0, 0, 1]],
                'projects': [[2, 2, 0], [0, 2, 2]],
            },
        ),
    ])
    def test_data_loader_successfully_load_valid_data(
        self,
        data_loader,
        test_filepath,
        expected,
    ):
        task = data_loader.load(path_to_test(test_filepath))
        assert tuple(task.info) == expected['info']
        assert task.workers == expected['workers']
        assert task.projects == expected['projects']
