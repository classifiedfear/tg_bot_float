from abc import ABC, abstractmethod

from fastapi import APIRouter


class AbstractRouterController(ABC):
    _router: APIRouter

    def __init__(self) -> None:
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    @abstractmethod
    def _init_routes(self):
        pass
