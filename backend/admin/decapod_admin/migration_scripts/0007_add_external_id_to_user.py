#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2016 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This migration adds external_id field to all user models.
"""


from decapod_api import wsgi
from decapod_common.models import db
from decapod_common.models import generic
from decapod_common.models import user


with wsgi.application.app_context():
    generic.configure_models(db.MongoDB())
    user.UserModel.collection().update_many(
        {"external_id": {"$exists": False}},
        {"$set": {"external_id": None}}
    )
