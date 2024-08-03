from abc import abstractmethod, ABC

from aiogram import Router


class AbstractRouterController(ABC):
    def __init__(self) -> None:
        self._router = Router()

    @abstractmethod
    def _init_routes(self) -> None:
        pass

    @property
    def router(self) -> Router:
        return self._router
