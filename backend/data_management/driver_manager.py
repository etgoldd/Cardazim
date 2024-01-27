
# This is a bit nasty, since imports aren't dynamic, but it
# really isn't that critical since we're only going to have 2.
from backend.data_management.drivers.mongo_driver import MongoDriver
from backend.data_management.drivers.filesystem_driver import FilesystemDriver
from backend.data_management.base_driver import BaseDriver
from exceptions import *

DRIVERS: dict[str, type[BaseDriver]] = {
    "MONGO": MongoDriver,
    "FILESYSTEM": FilesystemDriver
}


class DriverManager:
    def __init__(self, driver_type: str):
        """
        This class is responsible for managing the drivers.
        :param driver_type: The type of driver to use, currently only "MONGO" and "FILESYSTEM" are supported.
        """
        if driver_type not in DRIVERS.keys():
            raise DriverNotFound(f"No such driver: '{driver_type}', check documentation")
        self.driver_cls: type[BaseDriver] = DRIVERS[driver_type]

    def get_driver(self):
        # TODO implement per driver
        raise NotImplementedError()

    def get_default_driver(self) -> BaseDriver:
        return self.driver_cls.get_default_driver()
