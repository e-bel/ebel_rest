"""Testing module for query"""
import pytest

from ebel_rest import connect
from ebel_rest import query
from ..constants import USER, PASSWORD, DATABASE, SERVER


class TestQuery:
    connect(USER, PASSWORD, SERVER, DATABASE)

    def test_annotation(self):
        q = query.annotation('MeSHAnatomy', name='Lung')
        assert len(q.edges) > 1

    def test_last_author(self):
        q = query.last_author('Hong W')
        assert len(q.table.columns) >= 4
        assert len(q.table.index) > 0

    def test_pmid(self):
        q = query.pmid(30310104)
        assert len(q.table.columns) >= 4
        assert len(q.table.index) > 0

    def test_causal_correlative_by_gene(self):
        q = query.causal_correlative_by_gene('IL6')
        assert len(q.table.columns) >= 4
        assert len(q.table.index) > 0

    def test_path(self):
        q = query.path("ACE2", "AGTR1", 1, 1)
        assert len(q.table.columns) >= 4
        assert len(q.table.index) > 0

    def test_path_max_greater_min_error(self):
        with pytest.raises(ValueError) as e:
            query.path("ACE2", "AGTR1", 4, 1)
        assert str(e.value) == "min_edges must be a smaller value than max_edges!"

    def test_path_min_greater_0_error(self):
        with pytest.raises(ValueError) as e:
            query.path("ACE2", "AGTR1", 0, 1)
        assert str(e.value) == "min_edges must a value greater than 1!"

    def test_belish(self):
        q = query.belish('p(HGNC:"ACE2") ? ?')
        assert len(q.table.columns) >= 4
        assert len(q.table.index) > 0

    def test_sql(self):
        csql = "SELECT name as bel_name FROM bel LIMIT 1"
        q = query.sql(csql)
        assert 'bel_name' in list(q.table.columns)
        assert len(q.table.columns) == 1
        assert len(q.table.index) == 1

    def test_list_pmids(self):
        q = query.list_pmids()
        assert type(q) == list
        assert len(q) > 0

    # TODO Current version of test KG (COVID) too large. Need to make smaller test DB
    # def test_find_contradictions(self):
    #     q = query.find_contradictions()
    #     assert type(q) == Client
    #     assert len(q.data) > 0
    #     assert len(q.table.columns) > 5


# TODO write tests for "subgraph"
