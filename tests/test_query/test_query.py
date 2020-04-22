"""Testing module for query"""
from ebel_rest import query, connect
from ..constants import USER, PASSWORD, DATABASE, SERVER


class TestQuery:

    def test_annotation(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        q = query.annotation('MeSHAnatomy', name='Lung')
        assert len(q.edges) > 1

    def test_last_author(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        q = query.last_author(['Hong W'])
        assert len(q.table.columns) >= 4
        assert len(q.table.index) > 0

    def test_pmid(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        q = query.pmid(30310104)
        assert len(q.table.columns) >= 4
        assert len(q.table.index) > 0

    def test_causal_correlative_by_gene(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        q = query.causal_correlative_by_gene('IL6')
        assert len(q.table.columns) >= 4
        assert len(q.table.index) > 0

    def test_path(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        q = query.path("ACE2", "COVID-19", 1, 2)
        assert len(q.table.columns) >= 4
        assert len(q.table.index) > 0

    def test_belish(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        q = query.belish('p(HGNC:"ACE2") ? ?')
        assert len(q.table.columns) >= 4
        assert len(q.table.index) > 0

# TODO write tests for "subgraph"
