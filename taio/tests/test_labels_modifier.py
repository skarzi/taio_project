import pytest

from taio.graph import LabelsModifier
from taio.data_loader import TaskInfo


@pytest.fixture()
def labels_modifier():
    return LabelsModifier(TaskInfo(3, 3, 2))


class TestLabelsModifier:
    @pytest.mark.parametrize('worker_no, expected', [('0', 1), (1, 2), (2, 3)])
    def test_modify_worker(self, labels_modifier, worker_no, expected):
        assert labels_modifier.modify_worker(worker_no) == expected

    @pytest.mark.parametrize('worker_label, expected', [
        ('1', 0),
        (2, 1),
        (3, 2)
    ])
    def test_unmodify_worker(self, labels_modifier, worker_label, expected):
        assert labels_modifier.unmodify_worker(worker_label) == expected

    @pytest.mark.parametrize('feature_no, expected', [
        ('0', 4),
        (1, 5),
        (2, 6),
    ])
    def test_modify_feature(self, labels_modifier, feature_no, expected):
        assert labels_modifier.modify_feature(feature_no) == expected

    @pytest.mark.parametrize('feature_label, expected', [
        ('4', 0),
        (5, 1),
        (6, 2)
    ])
    def test_unmodify_feature(self, labels_modifier, feature_label, expected):
        assert labels_modifier.unmodify_feature(feature_label) == expected

    @pytest.mark.parametrize('project_no, expected', [
        ('0', 7),
        (1, 8),
    ])
    def test_modify_project(self, labels_modifier, project_no, expected):
        assert labels_modifier.modify_project(project_no) == expected

    @pytest.mark.parametrize('project_label, expected', [
        ('7', 0),
        (8, 1),
    ])
    def test_unmodify_project(self, labels_modifier, project_label, expected):
        assert labels_modifier.unmodify_project(project_label) == expected

    @pytest.mark.parametrize('source_no, expected', [
        ('0', 0),
        (1, 0),
    ])
    def test_modify_source(self, labels_modifier, source_no, expected):
        assert labels_modifier.modify_source(source_no) == expected

    @pytest.mark.parametrize('target_no, expected', [
        ('0', 9),
        (9, 9),
    ])
    def test_modify_target(self, labels_modifier, target_no, expected):
        assert labels_modifier.modify_target(target_no) == expected

    def test_raises_exception_for_wrong_label_name(self, labels_modifier):
        with pytest.raises(ValueError):
            labels_modifier.modify('employee', 12)
