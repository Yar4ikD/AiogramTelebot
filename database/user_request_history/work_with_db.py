"""Модуль работы с БД - history."""

import peewee
from loguru import logger
from .model import *
import datetime
from typing import Optional


class History:
    _user = None
    db.connect()
    logger.info('Connect | history.db')

    # def __int__(self):

    @classmethod
    def create(cls) -> None:
        """
        Метод класса создает таблицы БД.

        Returns: None

        """
        db.create_tables([User, Command])
        logger.success('Create Tables')

    @classmethod
    def add_user(cls, user_id: int, user_name: str) -> None:
        """
        Метод класса добавляет пользователя в таблицу users.
        Args:
            user_id: Передает id пользователя
            user_name: Передает имя аккаунта пользователя.

        Returns: None

        """
        try:
            id_, new_user = User.get_or_create(user_id=user_id, user_name=user_name, time_use=datetime.date.today())
            cls._user = id_

        except peewee.Expression as err:
            logger.exception(err)

        else:
            logger.success('history.db | func | add_user')

        finally:
            db.close()

    @classmethod
    def add_command(cls, command: str, query: str, response: str) -> None:
        """
        Метод класса добавляет команду бота и вернувшийся результат пользователю в таблицу commands.
        Args:
            command: Передает название команды ТГ-бота
            query: Передает данные указанные пользователем для получения результата
            response: Передает результат работы команды ТГ-бота

        Returns: None

        """
        try:
            Command.insert(select_command=command, query_data=query, response=response, user=cls._user).execute()

        except peewee.Expression as err:
            logger.exception(err)

        else:
            logger.success('history.db | func | add_command')

        finally:
            db.close()

    @classmethod
    def select_data(cls, user_id: str, count: int) -> Optional[str]:
        """
        Метод класса возвращает информацию с БД history - история запросов пользователя.
        Метод работы с БД - select
        Args:
            user_id: Передает id пользователя
            count: Передает ограничения по количеству записей.

        Returns: result

        """
        try:
            query = Command.select().join(User).where(User.user_id == user_id).limit(count)

            if len(query):
                logger.success('history.db | func | select_data')

                result = ''
                for data in query:

                    result += f'\n{data.select_command}\nДанные:\n{data.query_data}\nРезультат:\n{data.response}\n'

                return result

            return None
        except peewee.Expression as err:
            logger.exception(err)

        finally:
            db.close()
