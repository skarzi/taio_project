import functools


def intigerify(func):
    @functools.wraps(func)
    def wrapper(self, number):
        return func(self, int(number))
    return wrapper


class LabelsModifier:

    def __init__(self, task_info):
        self._task_info = task_info

    def modify(self, label, number, modifier=True):
        modifier = self.get(label, modifier)
        if modifier:
            return modifier(number)
        raise ValueError(f'Wrong label "{label}"!')

    def get(self, label, modifier=True, fallback=None):
        method_name = f'{"modify" if modifier else "unmodify"}_{label}'
        return getattr(self, method_name, fallback)

    @intigerify
    def modify_worker(self, number):
        return number + 1

    @intigerify
    def unmodify_worker(self, number):
        return number - 1

    @intigerify
    def modify_feature(self, number):
        return number + 1 + self._task_info.workers_number

    @intigerify
    def unmodify_feature(self, number):
        return number - 1 - self._task_info.workers_number

    @intigerify
    def modify_project(self, number):
        return (number + 1 + self._task_info.workers_number +
                self._task_info.features_number)

    @intigerify
    def unmodify_project(self, number):
        return (number - 1 - self._task_info.workers_number -
                self._task_info.features_number)

    @intigerify
    def modify_source(self, number):
        return 0

    @intigerify
    def modify_target(self, number):
        return (1 + self._task_info.workers_number +
                self._task_info.features_number +
                self._task_info.projects_number)
