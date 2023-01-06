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

""" API """

import datetime

import flask  # pylint: disable=E0401
import flask_restful  # pylint: disable=E0401
from flask import request

# from pylon.core.tools import log  # pylint: disable=E0611,E0401

from tools import auth  # pylint: disable=E0401


class API(flask_restful.Resource):  # pylint: disable=R0903
    """ API Resource """

    def __init__(self, module):
        self.module = module


    @auth.decorators.check_api(['global_admin'])
    def get(self):
        """ Get all cloud vulnerabilities"""

        search_text = request.args.get("search", None, type=str)
        offset = request.args.get('offset', 0, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        total, data = self.module.list_cv_cids(
            limit=limit, 
            offset=offset, 
            search=search_text,
        )

        return {"ok": True, "total": total, "rows":data}

    @auth.decorators.check_api(["global_admin"])
    def post(self):
        """ Add CIDs from POST JSON """
        added = 0
        data = flask.request.json
        #
        self.module.set_meta(
            "cv", {
                "updated": data.get(
                    "updated",
                    datetime.datetime.now(
                        datetime.timezone.utc
                    ).isoformat(
                        timespec="seconds"
                    ).replace("+00:00", "Z")
                ),
                "signatures": data.get("signatures", "unknown"),
            }
        )
        #
        for item in data.get("items", list()):
            cid = item.pop("cid")
            self.module.add_cv_cid(cid, item)
            added += 1
        #
        return {"ok": True, "added": added}
