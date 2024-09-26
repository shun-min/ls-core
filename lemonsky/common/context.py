from collections.abc import Callable, Mapping
from typing import Any, Dict, List, Optional, Type, Union

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

from skyline.models import (
    SkylineProjectCrew,
)


class BaseContext(ABC):
    def __init__(self):
        super().__init__()
        self._all: List[Any] = []
        self._current: Any = None
    
    @property
    def all(self):
        return self._all

    @all.setter
    def all(self, value: List[Any]):
        self._all = value
    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value: Any):
        self._current = value
        self.notify()
    
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
    def detach():
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


class BaseObserver(ABC):    
    def __init__(
        self,
        func: Optional[Callable] = None,
    ):
        self._func = func

    @abstractmethod
    def update():
        pass


class UserContext(BaseContext, Singleton):
    _observers: List[Mapping[BaseObserver]] = []
    def __init__(self):
        self._crew_data: Optional[SkylineProjectCrew] = None
    
    def attach(
        self, 
        observers: List[Any] | Any,
    ) -> None:
        if isinstance(observers, list):
            self._observers.extend(observers)
        else:
            self._observers.append(observers)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    @property
    def crew_data(self):
        return self._crew_data

    @crew_data.setter
    def crew_data(self, value: SkylineProjectCrew):
        self._crew_data= value


class ProjectContext(BaseContext, Singleton):
    """
    Holds project state that'll affect observing contexts
    """
    def __init__(self):
        self._observers: List[Any] = []
    
    def attach(
        self,
        observers: List[Any] | Any,
    ) -> None:
        if isinstance(observers, list):
            self._observers.extend(observers)
        else:
            self._observers.append(observers)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)


class GroupContext(BaseContext):
    """
    Holds ContentGroup state. Content Group is a special class made for categorizing contents for display in the Skyline hierarchy tree
    """
    def __int__(self):
        # self._current: ProjectModel = None
        self._observers: List[Mapping[BaseObserver]] = []
    
    def attach(self, observer: Any):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, observer):
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
        self.users: UserContext = UserContext()

    def init_context(self) -> None:
        
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
