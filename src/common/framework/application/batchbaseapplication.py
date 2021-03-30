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
import timeout_decorator

from typing import Any, Union, Optional, Tuple
from logging import getLogger
from abc import ABCMeta, abstractmethod

import common.framework.logger as logger
import common.framework.config as config


LOGGER = getLogger(__name__)


class BatchBaseApplication(metaclass=ABCMeta):

    SCRIPT_EXT = ".py"
    CONF_EXT = ".ini"
    GENERAL_CONF_NAME = "common" + CONF_EXT

    RET_NORMAL_END = 0
    RET_KEY_INTERRUPTED_END = 1
    RET_ABNORMAL_END = 100
    RET_TIMEOUT_END = 200

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
            sys.exit(BatchBaseApplication.RET_ABNORMAL_END)

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
            replace(BatchBaseApplication.SCRIPT_EXT,
                    BatchBaseApplication.CONF_EXT)

        common_conf = configparser.ConfigParser()
        self_conf = configparser.ConfigParser()

        common_conf.read(os.path.join(config.CONFIG_DIR,
                                      BatchBaseApplication.GENERAL_CONF_NAME))

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

    def _get_timeout_duration(self) -> Tuple[bool, int]:
        multithreaded = False
        timeout_duration = -1

        try:
            multithreaded = self.conf.self.application.multithread_app
        except Exception:
            pass

        try:
            timeout_duration = self.conf.self.application.timeout_duration
        except Exception:
            try:
                timeout_duration = \
                    self.conf.common.application.timeout_duration
            except Exception:
                pass

        return multithreaded, timeout_duration

    def start(self, **args: Any) -> None:
        retcode = BatchBaseApplication.RET_NORMAL_END
        multithread, timeout_duration = self._get_timeout_duration()

        if timeout_duration > -1:
            func = timeout_decorator.\
                timeout(timeout_duration,
                        use_signals=not multithread)(self.run_application)
        else:
            func = self.run_application

        try:
            LOGGER.info("start application!")

            LOGGER.info("start setup resource")
            self.setup_resource()
            LOGGER.info("end setup resource")

            LOGGER.info("start application setup")
            self.setup_application()
            LOGGER.info("end application setup")

            LOGGER.info("start main routine")
            result = func(**args)
            LOGGER.info("end main routine")

            LOGGER.info("end application without unexpected error")
            if (result is not None) and (type(result) is int):
                retcode = result
        except KeyboardInterrupt:
            LOGGER.warn("keyboard interrupted")
            retcode = BatchBaseApplication.RET_KEY_INTERRUPTED_END
        except timeout_decorator.TimeoutError:
            LOGGER.warn("timeout exception occurred: %dsec" %
                        (timeout_duration))
            retcode = BatchBaseApplication.RET_TIMEOUT_END
        except Exception as ex:
            LOGGER.error("unexpected exception <%s> occurred" % (str(ex)))
            LOGGER.error(traceback.format_exc())
            retcode = BatchBaseApplication.RET_ABNORMAL_END
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
