"""Testing module for query"""
from ebel_rest import connect
from ebel_rest.manager.core import Client
from ebel_rest.manager import query
from ..constants import USER, PASSWORD, DATABASE, SERVER


class TestQuery:
    connect(USER, PASSWORD, SERVER, DATABASE)

    def test_annotation(self):
        q = query.annotation('MeSHAnatomy', name='Lung')
        assert len(q.edges) > 1

    def test_last_author(self):
        q = query.last_author(['Hong W'])
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
        q = query.path("ACE2", "COVID-19", 1, 2)
        assert len(q.table.columns) >= 4
        assert len(q.table.index) > 0

    def test_belish(self):
        q = query.belish('p(HGNC:"ACE2") ? ?')
        assert len(q.table.columns) >= 4
        assert len(q.table.index) > 0

    def test_list_pmids(self):
        q = query.list_pmids()
        assert type(q) == list
        assert len(q) > 0

    # def test_find_contradictions(self):
    #     q = query.find_contradictions()
    #     assert type(q) == Client
    #     assert len(q.data) > 0
    #     assert len(q.table.columns) > 5


# TODO write tests for "subgraph"
