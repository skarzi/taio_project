from collections import namedtuple

TaskInfo = namedtuple('TaskInfo', [
    'workers_number',
    'features_number',
    'projects_number',
])
Task = namedtuple('Task', ['info', 'projects', 'workers'])


class DataLoader:
    def load(self, fname):
        projects = list()
        workers = list()
        with open(fname) as f:
            task_info = TaskInfo(*self._info_from_first_line(f))
            line_no = 0
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                if line_no < task_info.projects_number:
                    projects.append([int(x) for x in line.split(' ')])
                else:
                    workers.append([True if x == '1' else False
                                    for x in line.split(' ')])
                line_no += 1
        return Task(task_info, projects, workers)

    def _info_from_first_line(self, file_handler):
        first_line = file_handler.readline().strip()
        while not first_line:
            first_line = file_handler.readline().strip()
        return [int(x) for x in first_line.split(' ')]