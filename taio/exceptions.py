class InputDataException(Exception):
    pass


class FirstLineInputDataError(InputDataException):
    pass


class ProjectsInputDataError(InputDataException):
    pass


class WorkerInputDataError(InputDataException):
    pass


class ProjectsNumberInputDataError(InputDataException):
    pass


class InputDataFileNotExist(InputDataException):
    pass
