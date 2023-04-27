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

""" Module """

import sqlalchemy  # pylint: disable=E0401

from pylon.core.tools import log  # pylint: disable=E0401
from pylon.core.tools import module  # pylint: disable=E0401
from pylon.core.tools.context import Context as Holder  # pylint: disable=E0401

from tools import theme  # pylint: disable=E0401
from tools import db  # pylint: disable=E0401
from tools import db_migrations  # pylint: disable=E0401


class Module(module.ModuleModel):
    """ Pylon module """

    def __init__(self, context, descriptor):
        self.context = context
        self.descriptor = descriptor
        #
        self.db = Holder()  # pylint: disable=C0103
        self.db.tbl = Holder()

    def init(self):
        """ Init module """
        log.info("Initializing module")
        # Run DB migrations
        db_migrations.run_db_migrations(self, db.url)
        # DB
        module_name = self.descriptor.name
        self.db.metadata = sqlalchemy.MetaData()
        self.db.tbl.vmdr = sqlalchemy.Table(
            f"{module_name}__vmdr", self.db.metadata,
            autoload_with=db.engine,
        )
        self.db.tbl.meta = sqlalchemy.Table(
            f"{module_name}__meta", self.db.metadata,
            autoload_with=db.engine,
        )
        self.db.tbl.cv = sqlalchemy.Table(
            f"{module_name}__cv", self.db.metadata,
            autoload_with=db.engine,
        )
        # Theme registration
        theme.register_section(
            "kb", "KB",
            kind="holder",
            location="left",
            permissions={
                "permissions": ["kb"],
                "recommended_roles": {
                    "administration": {"admin": True, "viewer": True, "editor": True},
                    "default": {"admin": True, "viewer": True, "editor": True},
                    "developer": {"admin": True, "viewer": True, "editor": True},
                }
            },
            icon_class="fas fa-info-circle fa-fw",
        )
        theme.register_subsection(
            "kb",
            "vmdr", "VMDR",
            title="VMDR KB",
            kind="slot",
            prefix="kb_slot_vmdr_list_",
            permissions={
                "permissions": ["kb.vmdr"],
                "recommended_roles": {
                    "administration": {"admin": True, "viewer": True, "editor": True},
                    "default": {"admin": True, "viewer": True, "editor": True},
                    "developer": {"admin": True, "viewer": True, "editor": True},
                }
            },
            icon_class="fas fa-server fa-fw",
            weight=2,
        )
        theme.register_page(
            "kb", "vmdr", "view",
            title="VMDR KB",
            kind="slot",
            prefix="kb_slot_vmdr_view_",
            permissions={
                "permissions": ["kb.vmdr.view"],
                "recommended_roles": {
                    "administration": {"admin": True, "viewer": True, "editor": True},
                    "default": {"admin": True, "viewer": True, "editor": True},
                    "developer": {"admin": True, "viewer": True, "editor": True},
                }
            },
        )
        theme.register_subsection(
            "kb",
            "cv", "CloudView",
            title="CloudView KB",
            kind="slot",
            prefix="kb_slot_cv_list_",
            permissions={
                "permissions": ["kb.cv"],
                "recommended_roles": {
                    "administration": {"admin": True, "viewer": True, "editor": True},
                    "default": {"admin": True, "viewer": True, "editor": True},
                    "developer": {"admin": True, "viewer": True, "editor": True},
                }
            },
            icon_class="fas fa-cloud fa-fw",
        )
        theme.register_page(
            "kb", "cv", "view",
            title="CloudView KB",
            kind="slot",
            prefix="kb_slot_cv_view_",
            permissions={
                "permissions": ["kb.cv.view"],
                "recommended_roles": {
                    "administration": {"admin": True, "viewer": True, "editor": True},
                    "default": {"admin": True, "viewer": True, "editor": True},
                    "developer": {"admin": True, "viewer": True, "editor": True},
                }
            },
        )
        # Init RPCs
        self.descriptor.init_rpcs()
        # Init API
        self.descriptor.init_api()
        # Init SocketIO
        self.descriptor.init_sio()
        # Init blueprint
        self.descriptor.init_blueprint()
        # Init slots
        self.descriptor.init_slots()

    def deinit(self):  # pylint: disable=R0201
        """ De-init module """
        log.info("De-initializing module")
        # De-init slots
        # self.descriptor.deinit_slots()
        # De-init blueprint
        # self.descriptor.deinit_blueprint()
        # De-init SocketIO
        # self.descriptor.deinit_sio()
        # De-init API
        # self.descriptor.deinit_api()
        # De-init RPCs
        # self.descriptor.deinit_rpcs()
