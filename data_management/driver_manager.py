
# This is a bit nasty, since imports aren't dynamic, but it
# really isn't that critical since we're only going to have 2.
from data_management.drivers.mongo_driver import MongoDriver
from data_management.drivers.filesystem_driver import FilesystemDriver
from data_management.base_driver import BaseDriver
from exceptions import *

DRIVERS: dict[str, type[BaseDriver]] = {
    "MONGO": MongoDriver,
    "FILESYSTEM": FilesystemDriver
}


class DriverManager:
    def __init__(self, driver_type: str):
        # TODO add section that explains which driver type name corresponds to which driver
        if driver_type not in DRIVERS.keys():
            raise DriverNotFound(f"No such driver: '{driver_type}', check documentation")
        self.driver_cls: type[BaseDriver] = DRIVERS[driver_type]

    def get_driver(self):
        # TODO implement per driver
        return self.driver_cls()

    def get_default_driver(self) -> BaseDriver:
        return self.driver_cls.get_default_driver()


