# Snapshot testing referenced here: https://docs.graphene-python.org/en/latest/testing/
# https://github.com/syrusakbary/snapshottest/#reasons-to-use-this-package
import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from graphene.test import Client
from jinja2 import Template

from smdb.models import (
    Expedition,
    MissionType,
    Person,
    Platform,
    PlatformType,
    Sensor,
    SensorType,
)
from smdb.schema import schema
from smdb.users.models import User

pytestmark = pytest.mark.django_db()


def user_authenticated():
    rf = RequestFactory()
    user, _ = User.objects.get_or_create(username="tester")
    request = rf.post("/graphql/")
    request.user = user

    return request


# ===== MissionType Tests =====
create_missiontype_mutation = """mutation {
        create_missiontype(missiontype_name: "Initial") {
            missiontype {
            missiontype_name
            }
        }
    }"""


def test_all_missiontypes_empty(snapshot):
    client = Client(schema)
    snapshot.assert_match(
        client.execute(
            """{
                all_missiontypes {
                    missiontype_name
                    uuid
                  }
                }"""
        )
    )


def test_create_missiontype(snapshot):
    client = Client(schema)
    snapshot.assert_match(
        client.execute(create_missiontype_mutation, context=user_authenticated())
    )
    assert MissionType.objects.all()[0].missiontype_name == "Initial"


def test_all_sensortypes(snapshot):
    client = Client(schema)
    client.execute(create_sensortype_mutation, context=user_authenticated())
    response = client.execute(
        """{
                all_sensortypes {
                    sensortype_name
                  }
                }"""
    )
    assert response["data"]["all_sensortypes"][0]["sensortype_name"] == "Initial"
    snapshot.assert_match(response)


def test_update_missiontype(snapshot):
    client = Client(schema)
    client.execute(create_missiontype_mutation, context=user_authenticated())
    assert MissionType.objects.all()[0].missiontype_name == "Initial"

    update_missiontype_mutation = """mutation {
                update_missiontype(missiontype_name: "Initial", new_missiontype_name: "Updated") {
                    missiontype {
                        missiontype_name
                    }
                }
            }"""
    ##breakpoint()
    ##result = client.execute(update_missiontype_mutation, context=user_authenticated())
    ##breakpoint()
    snapshot.assert_match(
        client.execute(
            """mutation {
                update_missiontype(missiontype_name: "Initial", new_missiontype_name: "Updated") {
                    missiontype {
                        missiontype_name
                    }
                }
            }""",
            context=user_authenticated(),
        )
    )
    assert MissionType.objects.all()[0].missiontype_name == "Updated"


def test_delete_missiontype(snapshot):
    client = Client(schema)
    client.execute(create_missiontype_mutation, context=user_authenticated())
    snapshot.assert_match(
        client.execute(
            """mutation {
                delete_missiontype(missiontype_name: "Initial") {
                    missiontype {
                        missiontype_name
                    }
                }
            }""",
            context=user_authenticated(),
        )
    )
    assert MissionType.objects.all().count() == 0


# ===== Person Tests =====
create_person_template = Template(
    """mutation {
        create_person(input: {
            first_name: "Jane",
            last_name: "Doe",
            institution_name: "MBARI"
        }) {
            person {
                {{ uuid }}
                first_name
                last_name
                institution_name
            }
        }
    }"""
)


def test_all_persons_empty(snapshot):
    client = Client(schema)
    snapshot.assert_match(
        client.execute(
            """{
                all_persons {
                    uuid
                    first_name
                    last_name
                    institution_name
                  }
                }"""
        )
    )


def test_create_person(snapshot):
    client = Client(schema)
    create_person_mutation = create_person_template.render(uuid="")
    snapshot.assert_match(
        client.execute(create_person_mutation, context=user_authenticated())
    )
    assert Person.objects.all()[0].first_name == "Jane"
    assert Person.objects.all()[0].last_name == "Doe"
    assert Person.objects.all()[0].institution_name == "MBARI"


def test_all_persons(snapshot):
    client = Client(schema)
    create_person_mutation = create_person_template.render(uuid="")
    client.execute(create_person_mutation, context=user_authenticated())
    response = client.execute(
        """{
                all_persons {
                    first_name
                    last_name
                    institution_name
                  }
                }"""
    )
    assert response["data"]["all_persons"][0]["first_name"] == "Jane"
    assert response["data"]["all_persons"][0]["last_name"] == "Doe"
    assert response["data"]["all_persons"][0]["institution_name"] == "MBARI"
    snapshot.assert_match(response)


# https://medium.com/@jamesvaresamuel/mutation-and-query-in-graphql-using-python-django-part-2-79d9852a1092
def test_update_person(snapshot):
    client = Client(schema)
    create_person_mutation = create_person_template.render(uuid="uuid")
    response = client.execute(create_person_mutation, context=user_authenticated())
    uuid = response["data"]["create_person"]["person"]["uuid"]
    snapshot.assert_match(
        client.execute(
            """mutation UpdatePerson($uuid: ID!) {
            update_person(uuid: $uuid, input: {
                first_name: "Jim",
                last_name: "Roe",
                institution_name: "SIO"
            }) {
                person {
                    first_name
                    last_name
                    institution_name
                }
            }
        }""",
            variables={"uuid": uuid},
            context=user_authenticated(),
        )
    )
    assert Person.objects.all()[0].first_name == "Jim"
    assert Person.objects.all()[0].last_name == "Roe"
    assert Person.objects.all()[0].institution_name == "SIO"


def test_delete_person(snapshot):
    client = Client(schema)
    create_person_mutation = create_person_template.render(uuid="uuid")
    response = client.execute(create_person_mutation, context=user_authenticated())
    uuid = response["data"]["create_person"]["person"]["uuid"]
    snapshot.assert_match(
        client.execute(
            """mutation DeletePerson($uuid: ID!) {
            delete_person(uuid: $uuid) {
                person {
                    first_name
                    last_name
                    institution_name
                }
            }
        }""",
            variables={"uuid": uuid},
            context=user_authenticated(),
        )
    )
    assert Person.objects.all().count() == 0


# ===== PlatformType Tests =====
create_platformtype_mutation = """mutation {
        create_platformtype(platformtype_name: "Initial") {
            platformtype {
                platformtype_name
            }
        }
    }"""


def test_all_platformtypes_empty(snapshot):
    client = Client(schema)
    snapshot.assert_match(
        client.execute(
            """{
                all_platformtypes {
                    platformtype_name
                    uuid
                  }
                }"""
        )
    )


def test_create_platformtype(snapshot):
    client = Client(schema)
    snapshot.assert_match(
        client.execute(create_platformtype_mutation, context=user_authenticated())
    )
    assert PlatformType.objects.all()[0].platformtype_name == "Initial"


def test_all_platformtypes(snapshot):
    client = Client(schema)
    client.execute(create_platformtype_mutation, context=user_authenticated())
    response = client.execute(
        """{
                all_platformtypes {
                    platformtype_name
                  }
                }"""
    )
    assert response["data"]["all_platformtypes"][0]["platformtype_name"] == "Initial"
    snapshot.assert_match(response)


def test_update_platformtype(snapshot):
    client = Client(schema)
    client.execute(create_platformtype_mutation, context=user_authenticated())
    assert PlatformType.objects.all()[0].platformtype_name == "Initial"

    snapshot.assert_match(
        client.execute(
            """mutation {
                update_platformtype(platformtype_name: "Initial", new_platformtype_name: "Updated") {
                    platformtype {
                        platformtype_name
                    }
                }
            }""",
            context=user_authenticated(),
        )
    )
    assert PlatformType.objects.all()[0].platformtype_name == "Updated"


def test_delete_platformtype(snapshot):
    client = Client(schema)
    client.execute(create_platformtype_mutation, context=user_authenticated())
    snapshot.assert_match(
        client.execute(
            """mutation {
                delete_platformtype(platformtype_name: "Initial") {
                    platformtype {
                        platformtype_name
                    }
                }
            }""",
            context=user_authenticated(),
        )
    )
    assert PlatformType.objects.all().count() == 0


# ===== Platform Tests =====
create_platform_template = Template(
    """mutation {
        create_platform(input: {
            platform_name: "Dorado",
            platformtypes: [
                {
                    platformtype_name: "AUV"
                }
            ]
            operator_org_name: "MBARI"
        }) {
            platform {
                {{ uuid }}
                platform_name
                operator_org_name
                platform_type {
                    platformtype_name
                }
            }
        }
    }"""
)


def test_all_platforms_empty(snapshot):
    client = Client(schema)
    snapshot.assert_match(
        client.execute(
            """{
                all_platforms {
                    platform_name
                    uuid
                  }
                }"""
        )
    )


def test_create_platform(snapshot):
    client = Client(schema)
    create_platform_mutation = create_platform_template.render(uuid="")
    snapshot.assert_match(
        client.execute(create_platform_mutation, context=user_authenticated())
    )
    assert Platform.objects.all()[0].platform_name == "Dorado"
    assert Platform.objects.all()[0].operator_org_name == "MBARI"


def test_update_platform(snapshot):
    client = Client(schema)
    create_platform_mutation = create_platform_template.render(uuid="uuid")
    response = client.execute(create_platform_mutation, context=user_authenticated())
    uuid = response["data"]["create_platform"]["platform"]["uuid"]
    assert Platform.objects.all()[0].platform_name == "Dorado"

    snapshot.assert_match(
        client.execute(
            """mutation UpdatePlatform($uuid: ID!) {
                update_platform(uuid: $uuid, input: {
                    platform_name: "Updated",
                    platformtypes: [
                        {
                            platformtype_name: "LRAUV"
                        }
                    ]
                    operator_org_name: "SIO"
                }) {
                    platform {
                        platform_name
                        platform_type {
                            platformtype_name
                        }
                        operator_org_name
                    }
                }
            }""",
            variables={"uuid": uuid},
            context=user_authenticated(),
        )
    )
    assert Platform.objects.all()[0].platform_name == "Updated"
    assert Platform.objects.all()[0].platform_type.platformtype_name == "LRAUV"
    assert Platform.objects.all()[0].operator_org_name == "SIO"


def test_delete_platform(snapshot):
    client = Client(schema)
    create_platform_mutation = create_platform_template.render(uuid="uuid")
    response = client.execute(create_platform_mutation, context=user_authenticated())
    uuid = response["data"]["create_platform"]["platform"]["uuid"]
    snapshot.assert_match(
        client.execute(
            """mutation DeletePlatform($uuid: ID!) {
                delete_platform(uuid: $uuid) {
                    platform {
                        platform_name
                    }
                }
            }""",
            variables={"uuid": uuid},
            context=user_authenticated(),
        )
    )
    assert Platform.objects.all().count() == 0


# ===== SensorType Tests =====
create_sensortype_mutation = """mutation {
        create_sensortype(sensortype_name: "Initial") {
            sensortype {
                sensortype_name
            }
        }
    }"""


def test_all_sensortypes_empty(snapshot):
    client = Client(schema)
    snapshot.assert_match(
        client.execute(
            """{
                all_sensortypes {
                    sensortype_name
                    uuid
                  }
                }"""
        )
    )


def test_create_sensortype(snapshot):
    client = Client(schema)
    snapshot.assert_match(
        client.execute(create_sensortype_mutation, context=user_authenticated())
    )
    assert SensorType.objects.all()[0].sensortype_name == "Initial"


def test_all_sensortypes(snapshot):
    client = Client(schema)
    client.execute(create_sensortype_mutation, context=user_authenticated())
    response = client.execute(
        """{
                all_sensortypes {
                    sensortype_name
                  }
                }"""
    )
    assert response["data"]["all_sensortypes"][0]["sensortype_name"] == "Initial"
    snapshot.assert_match(response)


def test_update_sensortype(snapshot):
    client = Client(schema)
    client.execute(create_sensortype_mutation, context=user_authenticated())
    assert SensorType.objects.all()[0].sensortype_name == "Initial"

    snapshot.assert_match(
        client.execute(
            """mutation {
                update_sensortype(sensortype_name: "Initial", new_sensortype_name: "Updated") {
                    sensortype {
                        sensortype_name
                    }
                }
            }""",
            context=user_authenticated(),
        )
    )
    assert SensorType.objects.all()[0].sensortype_name == "Updated"


def test_delete_sensortype(snapshot):
    client = Client(schema)
    client.execute(create_sensortype_mutation, context=user_authenticated())
    snapshot.assert_match(
        client.execute(
            """mutation {
                delete_sensortype(sensortype_name: "Initial") {
                    sensortype {
                        sensortype_name
                    }
                }
            }""",
            context=user_authenticated(),
        )
    )
    assert SensorType.objects.all().count() == 0


# ===== Sensor Tests =====
create_sensor_template = Template(
    """mutation {
        create_sensor(input: {
            sensortypes: [
                {
                    sensortype_name: "Sonar"
                }
            ],
            model_name: "Initial",
            comment: "Initial comment"
        }) {
            sensor {
                {{ uuid }}
                model_name
                comment
                sensor_type {
                    sensortype_name
                }
            }
        }
    }"""
)


def test_all_sensors_empty(snapshot):
    client = Client(schema)
    snapshot.assert_match(
        client.execute(
            """{
                all_sensors {
                    uuid
                    model_name
                    comment
                  }
                }"""
        )
    )


def test_create_sensor(snapshot):
    client = Client(schema)
    create_sensor_mutation = create_sensor_template.render(uuid="")
    snapshot.assert_match(
        client.execute(create_sensor_mutation, context=user_authenticated())
    )
    assert Sensor.objects.all()[0].model_name == "Initial"


def test_all_sensors(snapshot):
    client = Client(schema)
    create_sensor_mutation = create_sensor_template.render(uuid="")
    client.execute(create_sensor_mutation, context=user_authenticated())
    response = client.execute(
        """{
                all_sensors {
                    model_name
                    comment
                  }
                }"""
    )
    assert response["data"]["all_sensors"][0]["model_name"] == "Initial"
    snapshot.assert_match(response)


def test_update_sensor(snapshot):
    client = Client(schema)
    create_sensor_mutation = create_sensor_template.render(uuid="uuid")
    response = client.execute(create_sensor_mutation, context=user_authenticated())
    uuid = response["data"]["create_sensor"]["sensor"]["uuid"]
    assert Sensor.objects.all()[0].model_name == "Initial"

    snapshot.assert_match(
        client.execute(
            """mutation UpdateSensor($uuid: ID) {
                update_sensor(uuid: $uuid, input: {
                    model_name: "Updated",
                    comment: "New comment"
                }) {
                    sensor {
                        model_name
                        comment
                    }
                }
            }""",
            variables={"uuid": uuid},
            context=user_authenticated(),
        )
    )
    assert Sensor.objects.all()[0].model_name == "Updated"
    assert Sensor.objects.all()[0].comment == "New comment"


def test_delete_sensor(snapshot):
    client = Client(schema)
    create_sensor_mutation = create_sensor_template.render(uuid="uuid")
    response = client.execute(create_sensor_mutation, context=user_authenticated())
    uuid = response["data"]["create_sensor"]["sensor"]["uuid"]
    snapshot.assert_match(
        client.execute(
            """mutation DeleteSensor($uuid: ID) {
                delete_sensor(uuid: $uuid) {
                    sensor {
                        model_name
                        comment
                    }
                }
            }""",
            variables={"uuid": uuid},
            context=user_authenticated(),
        )
    )
    assert Sensor.objects.all().count() == 0


# ===== Expedition Tests =====

create_expedition_template = Template(
    """mutation {
        create_expedition(input: {
            chiefscientist: {first_name: "Walter", last_name: "Munk", institution_name: "SIO"},
            expd_path_name: "/mbari/SeafloorMapping/2019/20190308m1",
            investigator: {first_name: "Henry", last_name: "Stommel", institution_name: "SIO"},
            start_date_iso: "1998-07-01",
            end_date_iso: "1998-07-20",
            expd_name: "Initial"}) {
            expedition {
                expd_name
                start_date
                end_date
                investigator {
                    first_name
                    last_name
                }
                chiefscientist {
                    first_name
                    last_name
                }
                expd_path_name
            }
        }
    }"""
)


def test_all_expeditions_empty(snapshot):
    client = Client(schema)
    snapshot.assert_match(
        client.execute(
            """{
                all_expeditions {
                    expd_name
                    start_date
                    end_date
                    expd_path_name
                  }
                }"""
        )
    )


def test_create_expedition(snapshot):
    client = Client(schema)
    create_expedition_mutation = create_expedition_template.render(uuid="")
    snapshot.assert_match(
        client.execute(create_expedition_mutation, context=user_authenticated())
    )
    assert Expedition.objects.filter(expd_name="Initial")[0].expd_name == "Initial"


def test_all_expeditions(snapshot):
    client = Client(schema)
    create_expedition_mutation = create_expedition_template.render(uuid="")
    client.execute(create_expedition_mutation, context=user_authenticated())
    response = client.execute(
        """{
                all_expeditions {
                    expd_name
                    start_date
                    end_date
                    expd_path_name
                  }
                }"""
    )
    assert response["data"]["all_expeditions"][-1]["expd_name"] == "Initial"
    snapshot.assert_match(response)


def test_update_expedition(snapshot):
    client = Client(schema)
    create_expedition_mutation = create_expedition_template.render(uuid="uuid")
    response = client.execute(create_expedition_mutation, context=user_authenticated())
    uuid = response["data"]["create_expedition"]["expedition"]["uuid"]
    assert Expedition.objects.all()[0].model_name == "Initial"

    snapshot.assert_match(
        client.execute(
            """mutation UpdateExpedition($uuid: ID) {
                update_expedition(uuid: $uuid, input: {
                    model_name: "Updated",
                    comment: "New comment"
                }) {
                    expedition {
                        model_name
                        comment
                    }
                }
            }""",
            variables={"uuid": uuid},
            context=user_authenticated(),
        )
    )
    assert Expedition.objects.all()[0].model_name == "Updated"
    assert Expedition.objects.all()[0].comment == "New comment"


def test_delete_expedition(snapshot):
    client = Client(schema)
    create_expedition_mutation = create_expedition_template.render(uuid="uuid")
    response = client.execute(create_expedition_mutation, context=user_authenticated())
    uuid = response["data"]["create_expedition"]["expedition"]["uuid"]
    snapshot.assert_match(
        client.execute(
            """mutation DeleteExpedition($uuid: ID) {
                delete_expedition(uuid: $uuid) {
                    expedition {
                        model_name
                        comment
                    }
                }
            }""",
            variables={"uuid": uuid},
            context=user_authenticated(),
        )
    )
    assert Expedition.objects.all().count() == 0
