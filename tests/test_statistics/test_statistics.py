"""Testing module for statistics"""
from ebel_rest import statistics, connect
from ..constants import USER, PASSWORD, DATABASE, SERVER


class TestStatistics:

    def test_summarize(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        stats = statistics.summarize()
        assert stats.data is not None
        assert stats.table.shape == (5, 2)

    def test_publication_by_year(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        stats = statistics.publication_by_year()
        assert stats.data is not None
        assert len(stats.table.columns) == 2
        assert len(stats.table.index) > 0

    def test_publication_by_number_of_statements(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        stats = statistics.publication_by_number_of_statements()
        assert stats.data is not None
        assert len(stats.table.columns) == 6
        assert len(stats.table.index) > 0

    def test_last_author_by_number_of_publications(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        stats = statistics.last_author_by_number_of_publications()
        assert stats.data is not None
        assert len(stats.table.columns) == 2
        assert len(stats.table.index) > 0

    def test_last_author_by_number_of_statements(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
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
        connect(USER, PASSWORD, SERVER, DATABASE)
        stats = statistics.edges()
        assert stats.data is not None
        assert len(stats.table.columns) == 2
        assert len(stats.table.index) > 0

    def test_nodes(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        stats = statistics.nodes()
        assert stats.data is not None
        assert len(stats.table.columns) == 2
        assert len(stats.table.index) > 0

    def test_total_bel_nodes(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        stats = statistics.total_bel_nodes()
        assert stats.data is not None
        assert stats.table.shape == (1, 1)

    def test_total_bel_edges(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        stats = statistics.total_bel_edges()
        assert stats.data is not None
        assert stats.table.shape == (1, 1)

    def test_total_publications(self):
        connect(USER, PASSWORD, SERVER, DATABASE)
        stats = statistics.total_publications()
        assert stats.data is not None
        assert stats.table.shape == (1, 1)
