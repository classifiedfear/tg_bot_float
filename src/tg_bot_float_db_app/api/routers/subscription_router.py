from fastapi import APIRouter


class SubscriptionRouter:
    def __init__(self):
        self._router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self):
        pass