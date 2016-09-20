# -*- coding: utf-8 -*-
"""Tests for cephlcm_common.models.playbook_configuration."""


import pytest

from cephlcm_common.models import playbook_configuration


def test_create(new_cluster, new_servers, public_playbook_name,
                pymongo_connection, freeze_time):
    name = pytest.faux.gen_alpha()
    pcmodel = playbook_configuration.PlaybookConfigurationModel.create(
        name=name,
        playbook=public_playbook_name,
        cluster=new_cluster,
        servers=new_servers,
        initiator_id=pytest.faux.gen_uuid()
    )

    db_pc = pymongo_connection.db.playbook_configuration.find_one(
        {"_id": pcmodel._id}
    )

    assert db_pc
    assert pcmodel.name == db_pc["name"]
    assert pcmodel.playbook == db_pc["playbook"]
    assert pcmodel.configuration == db_pc["configuration"]
    assert pcmodel.model_id == db_pc["model_id"]
    assert pcmodel.version == db_pc["version"]
    assert pcmodel.time_created == db_pc["time_created"]
    assert pcmodel.time_deleted == db_pc["time_deleted"]
    assert pcmodel.initiator_id == db_pc["initiator_id"]
    assert pcmodel.cluster_id == db_pc["cluster_id"]

    assert pcmodel.name == name
    assert pcmodel.playbook == public_playbook_name
    assert pcmodel.version == 1
    assert pcmodel.time_created == int(freeze_time.return_value)
    assert pcmodel.time_deleted == 0
    assert pcmodel.cluster_id == new_cluster.model_id


def test_update(new_cluster, new_servers, public_playbook_name,
                pymongo_connection, freeze_time):
    name = pytest.faux.gen_alpha()
    pcmodel = playbook_configuration.PlaybookConfigurationModel.create(
        name=name,
        playbook=public_playbook_name,
        cluster=new_cluster,
        servers=new_servers,
        initiator_id=pytest.faux.gen_uuid()
    )
    old_name = pcmodel.name

    pcmodel.name = pytest.faux.gen_alpha()
    pcmodel.save()

    assert pcmodel.version == 2
    assert pcmodel.name != old_name


def test_delete(new_cluster, new_servers, public_playbook_name,
                pymongo_connection, freeze_time):
    pcmodel = playbook_configuration.PlaybookConfigurationModel.create(
        name=pytest.faux.gen_alpha(),
        playbook=public_playbook_name,
        cluster=new_cluster,
        servers=new_servers,
        initiator_id=pytest.faux.gen_uuid()
    )
    pcmodel.delete()

    assert pcmodel.version == 2
    assert pcmodel.time_deleted == int(freeze_time.return_value)


def test_configuration_with_keys(new_cluster, new_servers,
                                 public_playbook_name, pymongo_connection,
                                 freeze_time):
    name = pytest.faux.gen_alpha()
    pcmodel = playbook_configuration.PlaybookConfigurationModel.create(
        name=name,
        playbook=public_playbook_name,
        cluster=new_cluster,
        servers=new_servers,
        initiator_id=pytest.faux.gen_uuid()
    )
    pcmodel.configuration = {
        "global_vars": {"127.0.0.1": "qqq"},
        "inventory": {}
    }
    pcmodel.save()

    db_model = pymongo_connection.db.playbook_configuration.find_one(
        {"_id": pcmodel._id})
    assert db_model
    assert "qqq" in db_model["configuration"]["global_vars"].values()

    new_pcmodel = playbook_configuration.PlaybookConfigurationModel()
    new_pcmodel.update_from_db_document(db_model)

    assert new_pcmodel.configuration == pcmodel.configuration
    assert new_pcmodel.configuration["global_vars"]["127.0.0.1"] == "qqq"
