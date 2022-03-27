#!/usr/bin/env python

import ast
import configparser
import logging
import os
import shelve
import sys
import threading
import traceback
from abc import ABCMeta, abstractmethod
from enum import IntEnum
from logging import getLogger
from typing import Any, Optional, Tuple, Union

import common.framework.config as config
import common.framework.logger as logger
import namedtupled
import timeout_decorator

LOGGER = getLogger(__name__)


class ExitCode(IntEnum):
    NORMAL = 0
    KEY_INTERRUPTED = 1
    TIMEOUT = 2
    ABEND = 127


class BatchBaseApplication(metaclass=ABCMeta):

    SCRIPT_EXT = ".py"
    CONF_EXT = ".ini"
    GENERAL_CONF_NAME = "common" + CONF_EXT

    def __init__(self, module_name: str, script_name: str) -> None:
        try:
            self.module_name: str = module_name
            self.script_name: str = script_name
            self.__toplevel_logger: Optional[logging.Logger] = None
            self.set_exit_code(ExitCode.NORMAL)

            self._prepare_config_dir()
            self.load_config()
            self._prepare_appcache()
            self.validate_config()
            self.create_toplevel_logger()
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            sys.exit(ExitCode.ABEND.value)

    def set_exit_code(self, code: ExitCode) -> None:
        """終了コードを設定します

        Args:
            code (ExitCode): 終了コードを示すenum
        """
        self.__return_code = code

    def validate_config(self) -> None:
        """コンフィグの内容を検証します
        """
        pass

    def setup_resource(self) -> None:
        """リソースの設定を行います
        """
        pass

    def setup_application(self) -> None:
        """アプリケーションロジックの実行に必要な前準備を行います
        """
        pass

    @abstractmethod
    def run_application(self) -> None:
        """アプリケーションロジックのエントリポイントです
        """
        pass

    def teardown_application(self) -> None:
        """アプリケーションロジックの終了に必要な処理を行います
        """
        pass

    def teardown_resource(self) -> None:
        """リソースの解放を行います
        """
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

    def start(self) -> None:
        multithread, timeout_duration = self._get_timeout_duration()

        if timeout_duration > -1:
            func = timeout_decorator.\
                timeout(timeout_duration,
                        use_signals=not multithread)(self.run_application)
        else:
            func = self.run_application

        try:
            LOGGER.info("start application")

            LOGGER.debug("start setup resource")
            self.setup_resource()
            LOGGER.debug("end setup resource")

            LOGGER.debug("start application setup")
            self.setup_application()
            LOGGER.debug("end application setup")

            LOGGER.info("start main routine")
            func()
            LOGGER.info("end main routine")

            LOGGER.info("end application successfully")
        except KeyboardInterrupt:
            LOGGER.warn("keyboard interrupted")
            self.set_exit_code(ExitCode.KEY_INTERRUPTED)
        except timeout_decorator.TimeoutError:
            LOGGER.warn("timeout exception occurred: %dsec" %
                        (timeout_duration))
            self.set_exit_code(ExitCode.TIMEOUT)
        except Exception as ex:
            LOGGER.error("unexpected exception <%s> occurred" % (str(ex)))
            LOGGER.error(traceback.format_exc())
            self.set_exit_code(ExitCode.ABEND)
        finally:
            LOGGER.debug("start cleanup")
            try:
                LOGGER.debug("start teardown application")
                self.teardown_application()
                LOGGER.debug("end teardown application")
            except Exception as ex:
                LOGGER.warning(
                    "exception <%s> occurred while teardown application" %
                    str(ex))
            try:
                LOGGER.debug("start teardown resource")
                self.teardown_resource()
                LOGGER.debug("end teardown resource")
            except Exception as ex:
                LOGGER.warning(
                    "exception <%s> occurred while teardown resource" %
                    str(ex))
            try:
                LOGGER.debug("start persistent app cache")
                self.__appcache.close()
                LOGGER.debug("end persistent app cache")
            except Exception as ex:
                LOGGER.warning(
                    "exception <%s> occurred while persistent app cache" %
                    str(ex))
            LOGGER.debug("end cleanup")

        sys.exit(self.__return_code.value)
