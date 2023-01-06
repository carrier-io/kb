#!/usr/bin/python3
# coding=utf-8

#   Copyright 2022 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" RPC """

from sqlalchemy.dialects import postgresql  # pylint: disable=E0401

# from pylon.core.tools import log  # pylint: disable=E0611,E0401
from pylon.core.tools import web  # pylint: disable=E0611,E0401

from tools import db  # pylint: disable=E0401
from tools import db_tools  # pylint: disable=E0401
from tools import rpc_tools  # pylint: disable=E0401


class RPC:  # pylint: disable=E1101,R0903
    """ RPC Resource """


    @web.rpc("kb_set_meta", "set_meta")
    @rpc_tools.wrap_exceptions(RuntimeError)
    def _set_meta(self, key, data):
        values = {
            "key": key,
            "data": data,
        }
        #
        with db.engine.connect() as connection:
            stmt = postgresql.insert(
                self.db.tbl.meta
            ).values(
                **values
            )
            return connection.execute(
                stmt.on_conflict_do_update(
                    index_elements=["key"],
                    set_=dict(data=stmt.excluded.data)
                )
            ).inserted_primary_key[0]


    @web.rpc("kb_get_meta", "get_meta")
    @rpc_tools.wrap_exceptions(RuntimeError)
    def _get_meta(self, key, default=...):
        try:
            with db.engine.connect() as connection:
                item = connection.execute(
                    self.db.tbl.meta.select().where(
                        self.db.tbl.meta.c.key == key,
                    )
                ).mappings().one()
            return db_tools.sqlalchemy_mapping_to_dict(item)["data"]
        except:  # pylint: disable=W0702
            if default is ...:
                default = dict()
            return default
