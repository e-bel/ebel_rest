"""Testing module for statistics"""
import pandas as pd
from ebel_rest import connect
from ebel_rest.manager import statistics
from ..constants import USER, PASSWORD, DATABASE, SERVER


class TestStatistics:
    connect(USER, PASSWORD, SERVER, DATABASE)

    def test_summarize(self):
        stats = statistics.summarize()
        assert stats.data is not None
        assert stats.table.shape == (5, 2)

    def test_publication_by_year(self):
        stats = statistics.publication_by_year()
        assert stats.data is not None
        assert len(stats.table.columns) == 2
        assert len(stats.table.index) > 0

    def test_publication_by_number_of_statements(self):
        stats = statistics.publication_by_number_of_statements()
        assert stats.data is not None
        assert len(stats.table.columns) == 6
        assert len(stats.table.index) > 0

    def test_last_author_by_number_of_publications(self):
        stats = statistics.last_author_by_number_of_publications()
        assert stats.data is not None
        assert len(stats.table.columns) == 2
        assert len(stats.table.index) > 0

    def test_node_namespace_order_by_namespace(self):
        stats = statistics.node_namespace_order_by_namespace()
        assert stats.data is not None
        assert len(stats.table.columns) == 3
        assert len(stats.table.index) > 0

    def test_namespace_by_count(self):
        stats = statistics.namespace_by_count()
        assert type(stats.table) == pd.DataFrame
        assert len(stats.table.columns) == 2
        assert 'HGNC' in stats.table['namespace'].values

    def test_last_author_by_number_of_statements(self):
        stats = statistics.last_author_by_number_of_statements()
        assert stats.data is not None
        assert len(stats.table.columns) == 2
        assert len(stats.table.index) > 0

    def test_node_namespace_order_by_count(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        stats = statistics.node_namespace_order_by_count()
        assert stats.data is not None
        assert len(stats.table.columns) == 3
        assert len(stats.table.index) > 0

    def test_edges(self):
        stats = statistics.edges()
        assert stats.data is not None
        assert len(stats.table.columns) == 2
        assert len(stats.table.index) > 0

    def test_nodes(self):
        stats = statistics.nodes()
        assert stats.data is not None
        assert len(stats.table.columns) == 2
        assert len(stats.table.index) > 0

    def test_total_bel_nodes(self):
        stats = statistics.total_bel_nodes()
        assert stats.data is not None
        assert stats.table.shape == (1, 1)

    def test_total_bel_edges(self):
        stats = statistics.total_bel_edges()
        assert stats.data is not None
        assert stats.table.shape == (1, 1)

    def test_total_publications(self):
        stats = statistics.total_publications()
        assert stats.data is not None
        assert stats.table.shape == (1, 1)

    # def test_edges_by_pmid(self):
    #     no_pivot = statistics.edges_by_pmid(pivot=False)
    #     assert no_pivot.data is not None
    #     assert len(no_pivot.table.columns) == 3
    #     assert len(no_pivot.table.index) > 0
    #
    #     pivot = statistics.edges_by_pmid(pivot=True)
    #     assert isinstance(pivot, pd.DataFrame)
    #     assert len(pivot.columns) >= 0
    #     assert len(pivot.index) > 0

    # def test_nodes_by_pmid(self):
    #     no_pivot = statistics.nodes_by_pmid(pivot=False)
    #     assert no_pivot.data is not None
    #     assert len(no_pivot.table.columns) == 2
    #     assert len(no_pivot.table.index) > 0
    #
    #     pivot = statistics.nodes_by_pmid(pivot=True)
    #     assert isinstance(pivot, pd.DataFrame)
    #     assert len(pivot.columns) >= 0
    #     assert len(pivot.index) > 0
