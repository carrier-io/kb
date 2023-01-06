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


    @web.slot("kb_slot_vmdr_list_content")
    @auth.decorators.check_slot([], access_denied_reply=theme.access_denied_part)
    def _vmdr_kb_content(self, context, slot, payload):
        with context.app.app_context():
            return self.descriptor.render_template("vmdr/kb_list.html",)


    @web.slot("kb_slot_vmdr_list_styles")
    @auth.decorators.check_slot([])
    def _vmdr_kb_styles(self, context, slot, payload):
        with context.app.app_context():
            return self.descriptor.render_template("vmdr/kb_styles.html")


    @web.slot("kb_slot_vmdr_list_scripts")
    @auth.decorators.check_slot([], access_denied_reply=theme.access_denied_part)
    def _vmdr_kb_view_content(self, context, slot, payload):
        with context.app.app_context():
            return self.descriptor.render_template("vmdr/kb_scripts.html")
