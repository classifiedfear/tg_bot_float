from fastapi import APIRouter


class UserRouter:
    def __init__(self):
        self._router = APIRouter(prefix="/users", tags=["users"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        pass
