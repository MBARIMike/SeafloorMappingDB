from re import L, T
from tabnanny import verbose
from django_tables2 import Table, Column, ManyToManyColumn

from smdb.models import Compilation, Expedition, Mission


class MissionTable(Table):
    name = Column(linkify=True)
    expedition = Column(linkify=True)

    class Meta:
        model = Mission
        fields = (
            "name",
            "track_length",
            "start_depth",
        )


class ExpeditionTable(Table):
    name = Column(linkify=True)
    mission_set = ManyToManyColumn(
        linkify_item=True,
        verbose_name="Missions",
    )

    class Meta:
        model = Expedition
        fields = ("name", "expd_db_id")
        sequence = ("name", "expd_db_id", "mission_set")


class CompilationTable(Table):
    name = Column(linkify=True)
    missions = ManyToManyColumn(linkify_item=True, verbose_name="Missions")

    class Meta:
        model = Compilation
        fields = ("name",)
        sequence = ("name", "missions")
