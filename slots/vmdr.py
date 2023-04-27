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

""" Slot """

# from pylon.core.tools import log  # pylint: disable=E0611,E0401
from pylon.core.tools import web  # pylint: disable=E0611,E0401

from tools import auth  # pylint: disable=E0401
from tools import theme  # pylint: disable=E0401


class Slot:  # pylint: disable=E1101,R0903
    """ Slot Resource """


    @web.slot("kb_slot_vmdr_content")
    @auth.decorators.check_slot(["kb.vmdr"], access_denied_reply=theme.access_denied_part)
    def _vmdr_kb_content(self, context, slot, payload):
        _ = slot
        #
        try:
            page = int(payload.request.args.get("page", "1"))
        except:  # pylint: disable=W0702
            page = 1
        #
        search = payload.request.args.get("search", None)
        #
        _, data = self.list_vmdr_qids(limit=30, offset=(page-1)*30, search=search)
        meta = self.get_meta("vmdr")
        #
        with context.app.app_context():
            return self.descriptor.render_template(
                "vmdr/kb.html",
                data=data, page=page, search=search,
                updated=meta.get("updated"), signatures=meta.get("signatures"),
            )


    @web.slot("kb_slot_vmdr_styles")
    @auth.decorators.check_slot(["kb.vmdr"])
    def _vmdr_kb_styles(self, context, slot, payload):
        _ = slot, payload
        #
        with context.app.app_context():
            return self.descriptor.render_template("vmdr/kb_styles.html")


    @web.slot("kb_slot_vmdr_view_content")
    @auth.decorators.check_slot(["kb.vmdr.view"], access_denied_reply=theme.access_denied_part)
    def _vmdr_kb_view_content(self, context, slot, payload):
        _ = slot
        #
        try:
            qid = int(payload.request.args.get("qid", None))
            data = self.get_vmdr_qid(qid)
        except:  # pylint: disable=W0702
            return theme.access_denied_part
        #
        with context.app.app_context():
            return self.descriptor.render_template("vmdr/kb_view.html", data=data)
