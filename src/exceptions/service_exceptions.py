class ProjectServiceError(Exception):
    """Base exception for project service errors."""
    pass


class TaskServiceError(Exception):
    """Base exception for task service errors."""
    pass


class ProjectLimitReachedError(ProjectServiceError):
    """Raised when maximum number of projects is reached."""
    pass


class ProjectNameExistsError(ProjectServiceError):
    """Raised when a project with the same name already exists."""
    pass


class ProjectNotFoundError(ProjectServiceError):
    """Raised when a project is not found."""
    pass


class TaskLimitReachedError(TaskServiceError):
    """Raised when maximum number of tasks in a project is reached."""
    pass


class TaskNotFoundError(TaskServiceError):
    """Raised when a task is not found."""
    pass


class InvalidTaskStatusError(TaskServiceError):
    """Raised when an invalid task status is provided."""
    pass


class InvalidDeadlineFormatError(TaskServiceError):
    """Raised when an invalid deadline format is provided."""
    pass


class EmptyTitleError(TaskServiceError):
    """Raised when a title is empty or blank."""
    pass


class TitleTooLongError(TaskServiceError):
    """Raised when a title exceeds the maximum length."""
    pass


class DescriptionTooLongError(TaskServiceError):
    """Raised when a description exceeds the maximum length."""
    pass