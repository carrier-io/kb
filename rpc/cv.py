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

import sqlalchemy  # pylint: disable=E0401
from sqlalchemy.dialects import postgresql  # pylint: disable=E0401
from sqlalchemy import select, func

# from pylon.core.tools import log  # pylint: disable=E0611,E0401
from pylon.core.tools import web  # pylint: disable=E0611,E0401

from tools import db  # pylint: disable=E0401
from tools import db_tools  # pylint: disable=E0401
from tools import rpc_tools  # pylint: disable=E0401


class RPC:  # pylint: disable=E1101,R0903
    """ RPC Resource """


    @web.rpc("kb_add_cv_cid", "add_cv_cid")
    @rpc_tools.wrap_exceptions(RuntimeError)
    def _add_cv_cid(self, cid, data):
        values = {
            "cid": cid,
            "data": data,
        }
        #
        with db.engine.connect() as connection:
            stmt = postgresql.insert(
                self.db.tbl.cv
            ).values(
                **values
            )
            return connection.execute(
                stmt.on_conflict_do_update(
                    index_elements=["cid"],
                    set_=dict(data=stmt.excluded.data)
                )
            ).inserted_primary_key[0]


    @web.rpc("kb_get_cv_cid", "get_cv_cid")
    @rpc_tools.wrap_exceptions(RuntimeError)
    def _get_cv_cid(self, cid):
        with db.engine.connect() as connection:
            item = connection.execute(
                self.db.tbl.cv.select().where(
                    self.db.tbl.cv.c.cid == cid,
                )
            ).mappings().one()
        return db_tools.sqlalchemy_mapping_to_dict(item)


    @web.rpc("kb_list_cv_cids", "list_cv_cids")
    @rpc_tools.wrap_exceptions(RuntimeError)
    def _list_cv_cids(self, limit=None, offset=None, search=None):
        stmt = self.db.tbl.cv.select()
        count_stmt = select([func.count()]).select_from(self.db.tbl.cv)
        #
        if search is not None:
            condition = sqlalchemy.or_(
                sqlalchemy.cast(
                    self.db.tbl.cv.c.cid, sqlalchemy.Text
                ).ilike(
                    f'%{search}%'
                ),
                self.db.tbl.cv.c.data["controlName"].astext.ilike(
                    f'%{search}%'
                )
            )
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)
        #
        with db.engine.connect() as connection:
            total = connection.execute(count_stmt).scalar()
        #
        stmt = stmt.order_by(
            self.db.tbl.cv.c.cid
        )
        #
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        #
        with db.engine.connect() as connection:
            items = connection.execute(stmt).mappings().all()
        #
        return total, [db_tools.sqlalchemy_mapping_to_dict(item) for item in items]
