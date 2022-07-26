from pydantic import BaseModel

from sdk.healthchecks import SUCCESS_STATUS


class HealthCheckStatuses(BaseModel):
    DatabaseBackend: str
    DefaultFileStorageHealthCheck: str
    DiskUsage: str
    MemoryUsage: str
    RabbitMQHealthCheck: str

    def is_all_success(self) -> bool:
        return all(value == SUCCESS_STATUS for _, value in self.__iter__())


class Msg(BaseModel):
    msg: str
