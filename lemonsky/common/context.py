from collections.abc import Mapping
from typing import Any, Dict, List, Optional

from ..data.hrm.models import (
    EmployeeModel,
)
from lemonsky.data.dashboard.controllers import (
    Project,
)
from lemonsky.data.dashboard.models import (
    ProjectModel,
    TaskModel,
    VersionModel,
)


from abc import ABC, abstractmethod
from typing import Any, List

from lemonsky.common.singleton import Singleton
from lemonsky.data.dashboard.controllers import (
    Project,
)


class BaseContext(ABC, Singleton):
    """
    Applies Observer pattern. Subject interface that declares a ser of methods to manage subscribers
    """
    @abstractmethod
    def attach():
        """
        Attach an observer to subject
        """
        pass

    @abstractmethod
    def dettach():
        """
        dettach an observer to subject
        """
        pass

    @abstractmethod
    def notify():
        """
        Notify all observers about an event
        """
        pass


class BaseObserver(ABC, Singleton):
    def __init__(self):
        super().__init__()
        self._all: List[Any] = []
        self._current: Any = None
    
    @abstractmethod
    def update():
        pass
    
    @property
    def all(self):
        return self._all

    @all.setter
    def all(self, value: List[Any]):
        self._all = value

    @property
    def current(self):
        return self._all

    @current.setter
    def current(self, value: List[Any]):
        self._current = value


class ProjectContext(BaseContext):
    """
    Holds project state that'll affect observing contexts
    """
    def __init__(self):
        self._observers: List[Mapping[BaseObserver]] = []
    
    def attach(self, observer: Mapping[BaseObserver]):
        self._observers.append(observer)

    def dettach(self, observer: Mapping[BaseObserver]):
        self._observers.remove(observer)

    def notify(self, observer: Mapping[BaseObserver]):
        for observer in self._observers:
            observer.update(self)


class GroupContext(BaseContext):
    """
    Holds ContentGroup state. Content Group is a special class made for categorizing contents for display in the Skyline hierarchy tree
    """
    def __int__(self):
        # self._current: ProjectModel = None
        self._observers: List[Mapping[BaseObserver]] = []
    
    def attach(self, observer: Mapping[BaseObserver]):
        self._observers.append(observer)

    def dettach(self, observer: Mapping[BaseObserver]):
        self._observers.remove(observer)

    def notify(self, observer: Mapping[BaseObserver]):
        for observer in self._observers:
            observer.update(self)


class UserContext(BaseContext):
    _observers: List[BaseObserver] = []
    
    def attach(self, observer: Mapping[BaseObserver]):
        self._observers.append(observer)

    def dettach(self, observer: Mapping[BaseObserver]):
        self._observers.remove(observer)

    def notify(self, observer: Mapping[BaseObserver]):
        for observer in self._observers:
            observer.update(self)


class ToolContext(Singleton):
    """
    A Singleton collection of contexts (concrete subjects that holds a list of observers) that are useful for pipeline
    Stores values that'll be used tool-wide, this can be passed around everywhere
    """
    def __init__(self):
        super().__init__()
        self.projects: ProjectContext = ProjectContext()
        # self.tasks: TaskContext()
        self.users: UserContext = UserContext()
        self.init_context()

    def init_context(self) -> None:
        
        return

    def fetch_task_context():
        return

    def fetch_current_user():
        return

    def fetch_machine_name():
        return


class Publisher(object):
    """
    Publisher object that controls the registering of versions and files
    Args:
        object (_type_): _description_
    """
    def __init__(self):
        super().__init__()
        self.versions = List[VersionModel]

    def add_files(self):
        print("add_files")

    def publish(self):
        return
