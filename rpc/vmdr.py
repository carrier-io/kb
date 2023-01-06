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


    @web.rpc("kb_add_vmdr_qid", "add_vmdr_qid")
    @rpc_tools.wrap_exceptions(RuntimeError)
    def _add_vmdr_qid(self, qid, data):
        values = {
            "qid": qid,
            "data": data,
        }
        #
        with db.engine.connect() as connection:
            stmt = postgresql.insert(
                self.db.tbl.vmdr
            ).values(
                **values
            )
            return connection.execute(
                stmt.on_conflict_do_update(
                    index_elements=["qid"],
                    set_=dict(data=stmt.excluded.data)
                )
            ).inserted_primary_key[0]


    @web.rpc("kb_get_vmdr_qid", "get_vmdr_qid")
    @rpc_tools.wrap_exceptions(RuntimeError)
    def _get_vmdr_qid(self, qid):
        with db.engine.connect() as connection:
            item = connection.execute(
                self.db.tbl.vmdr.select().where(
                    self.db.tbl.vmdr.c.qid == qid,
                )
            ).mappings().one()
        return db_tools.sqlalchemy_mapping_to_dict(item)


    @web.rpc("kb_list_vmdr_qids", "list_vmdr_qids")
    @rpc_tools.wrap_exceptions(RuntimeError)
    def _list_vmdr_qids(self, limit=None, offset=None, search=None):
        stmt = self.db.tbl.vmdr.select()
        count_stmt = select([func.count()]).select_from(self.db.tbl.vmdr)
        #
        if search is not None:
            condition = sqlalchemy.or_(
                sqlalchemy.cast(
                    self.db.tbl.vmdr.c.qid, sqlalchemy.Text
                ).ilike(
                    f'%{search}%'
                ),
                self.db.tbl.vmdr.c.data["title"].astext.ilike(
                    f'%{search}%'
                )
            )
            count_stmt = count_stmt.where(condition)
            stmt = stmt.where(condition)
        
        #
        with db.engine.connect() as connection:
            total = connection.execute(count_stmt).scalar()
        #
        stmt = stmt.order_by(
            self.db.tbl.vmdr.c.qid
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
