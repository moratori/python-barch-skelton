#!/usr/bin/env python

import ast
import os
import shelve
import threading
import configparser
import namedtupled
import sys
import traceback
import logging

from typing import Any, Union, Optional
from logging import getLogger
from abc import ABCMeta, abstractmethod

import common.framework.logger as logger
import common.framework.config as config


LOGGER = getLogger(__name__)


class BaseApplication(metaclass=ABCMeta):

    SCRIPT_EXT = ".py"
    CONF_EXT = ".ini"
    GENERAL_CONF_NAME = "common" + CONF_EXT

    RET_NORMAL_END = 0
    RET_KEY_INTERRUPTED_END = 1
    RET_ABNORMAL_END = 100

    def __init__(self, module_name: str, script_name: str) -> None:
        try:
            self.module_name: str = module_name
            self.script_name: str = script_name
            self.__toplevel_logger: Optional[logging.Logger] = None

            self._prepare_config_dir()
            self.load_config()
            self._prepare_appcache()
            self.validate_config()
            self.create_toplevel_logger()
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            sys.exit(BaseApplication.RET_ABNORMAL_END)

    @abstractmethod
    def validate_config(self) -> None:
        pass

    @abstractmethod
    def setup_resource(self) -> None:
        pass

    @abstractmethod
    def setup_application(self) -> None:
        pass

    @abstractmethod
    def run_application(self, **args: Any) -> Optional[int]:
        pass

    @abstractmethod
    def teardown_application(self) -> None:
        pass

    @abstractmethod
    def teardown_resource(self) -> None:
        pass

    def _prepare_appcache(self) -> None:
        dbname = os.path.join(config.APPCACHE,
                              os.path.basename(self.script_name))

        self.__appcache = shelve.open(dbname, flag="c", writeback=False)
        self.__appcache_mutex = threading.BoundedSemaphore(value=1)

    def set_cache(self, key: str, value: Any) -> None:
        with self.__appcache_mutex:
            self.__appcache[key] = value

    def del_cache(self, key: str) -> None:
        with self.__appcache_mutex:
            del self.__appcache[key]

    def get_cache(self, key: str) -> None:
        return self.__appcache[key]

    def get_cache_keys(self) -> Any:
        return self.__appcache.keys()

    def _convert_config_type(self, config: Union[str, dict]) -> Any:
        if isinstance(config, str):
            return ast.literal_eval(config)
        elif isinstance(config, dict):
            result = dict()
            for (key, value) in config.items():
                result[key] = self._convert_config_type(value)
            return result
        else:
            raise Exception("unknown config type: %s" % type(config))

    def load_config(self) -> None:
        specific_config_basename = \
            os.path.basename(self.script_name).\
            replace(BaseApplication.SCRIPT_EXT,
                    BaseApplication.CONF_EXT)

        common_conf = configparser.ConfigParser()
        self_conf = configparser.ConfigParser()

        common_conf.read(os.path.join(config.CONFIG_DIR,
                                      BaseApplication.GENERAL_CONF_NAME))

        self_conf.read(os.path.join(config.CONFIG_DIR,
                                    specific_config_basename))

        com = self._convert_config_type(common_conf._sections)  # type: ignore
        sel = self._convert_config_type(self_conf._sections)  # type: ignore
        self.conf = namedtupled.map(dict(common=com, self=sel))

    def _prepare_config_dir(self) -> None:
        for directory in config.DIRECTORIES:
            if not os.path.isdir(directory):
                os.mkdir(directory)

    def create_toplevel_logger(self) -> logging.Logger:
        if self.__toplevel_logger is None:
            self.__toplevel_logger = \
                logger.setup_logger(self.module_name,
                                    self.script_name,
                                    self.conf.common.logging.loglevel,
                                    self.conf.common.logging.rotation_timing,
                                    self.conf.common.logging.backupcount)
        return self.__toplevel_logger

    def start(self, **args: Any) -> None:
        retcode = BaseApplication.RET_NORMAL_END
        try:
            LOGGER.info("start application!")

            LOGGER.info("start setup resource")
            self.setup_resource()
            LOGGER.info("end setup resource")

            LOGGER.info("start application setup")
            self.setup_application()
            LOGGER.info("end application setup")

            LOGGER.info("start main routine")
            result = self.run_application(**args)
            LOGGER.info("end main routine")

            LOGGER.info("end application without unexpected error")
            if (result is not None) and (type(result) is int):
                retcode = result
        except KeyboardInterrupt:
            LOGGER.warn("keyboard interrupted")
            retcode = BaseApplication.RET_KEY_INTERRUPTED_END
        except Exception as ex:
            LOGGER.error("unexpected exception <%s> occurred" % (str(ex)))
            LOGGER.error(traceback.format_exc())
            retcode = BaseApplication.RET_ABNORMAL_END
        finally:
            LOGGER.info("start cleanup")
            try:
                LOGGER.info("start teardown application")
                self.teardown_application()
                LOGGER.info("end teardown application")
            except Exception as ex:
                LOGGER.warning("unexpected exception <%s> occurred" %
                               str(ex))
            try:
                LOGGER.info("start teardown resource")
                self.teardown_resource()
                LOGGER.info("end teardown resource")
            except Exception as ex:
                LOGGER.warning("unexpected exception <%s> occurred" %
                               str(ex))
            try:
                LOGGER.info("start persistent app cache")
                self.__appcache.close()
                LOGGER.info("end persistent app cache")
            except Exception as ex:
                LOGGER.warning("unexpected exception <%s> occurred" %
                               str(ex))
            LOGGER.info("end cleanup")

        sys.exit(retcode)
