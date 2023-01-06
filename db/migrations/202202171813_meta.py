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

""" DB migration """

revision = "202202171813"
down_revision = "202202161207"
branch_labels = None


from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql


def upgrade(module, payload):
    module_name = module.descriptor.name
    #
    op.create_table(
        f"{module_name}__meta",
        sa.Column("key", sa.Text, primary_key=True, index=True),
        sa.Column("data", psql.JSONB),
    )


def downgrade(module, payload):
    module_name = module.descriptor.name
    #
    op.drop_table(f"{module_name}__meta")
