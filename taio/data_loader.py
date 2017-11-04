import os

from collections import namedtuple

import taio.exceptions as dl_exc

TaskInfo = namedtuple('TaskInfo', [
    'workers_number',
    'features_number',
    'projects_number',
])
Task = namedtuple('Task', ['info', 'projects', 'workers'])


class DataLoader:
    def load(self, fname):
        if not os.path.exists(fname):
            raise dl_exc.InputDataFileNotExist()
        projects = list()
        workers = list()
        with open(fname) as f:
            task_info = self._task_info_from_first_line(f)
            line_no = 0
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                if line_no < task_info.workers_number:
                    workers.append(self._load_worker(task_info, line))
                else:
                    projects.append(self._load_project(task_info, line))
                line_no += 1
        if len(projects) != task_info.projects_number:
            raise dl_exc.ProjectsNumberInputDataError()
        return Task(task_info, projects, workers)

    def _load_worker(self, task_info, worker_line):
        worker = list()
        for x in worker_line.split(' '):
            if x == '1':
                worker.append(True)
            elif x == '0':
                worker.append(False)
            else:
                raise dl_exc.WorkerInputDataError()
        if len(worker) != task_info.features_number:
            raise dl_exc.WorkerInputDataError()
        return worker

    def _load_project(self, task_info, project_line):
        project = [int(x) for x in project_line.split(' ')]
        if (len(project) != task_info.features_number or
                not all(x >= 0 for x in project)):
            raise dl_exc.ProjectsInputDataError()
        return project

    def _task_info_from_first_line(self, file_handler):
        first_line = file_handler.readline().strip()
        while not first_line:
            first_line = file_handler.readline().strip()
        first_line = [int(x) for x in first_line.split()]
        if len(first_line) != 3 or not all(x > 0 for x in first_line):
            raise dl_exc.FirstLineInputDataError()
        return TaskInfo(first_line[1], first_line[0], first_line[-1])
