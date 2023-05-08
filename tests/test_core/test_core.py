"""Testing module for core"""
import pytest

import pandas as pd

from ebel_rest import connect
from ebel_rest import query
from ..constants import USER, PASSWORD, DATABASE, SERVER


err_msg = "Second element is not a graph"


class TestCore:
    connect(USER, PASSWORD, SERVER, DATABASE)

    def test_table_property(self):
        q = query.last_author('Hong W')
        assert len(q.table.columns) >= 4
        assert len(q.table.index) > 0

        assert isinstance(q.table, pd.DataFrame)
        expected_cols = ['subject_bel', 'relation', 'object_bel', 'pmid']
        actual_cols = q.table.columns.tolist()
        for excol in expected_cols:
            assert excol in actual_cols
        assert q.table.index.name == "edge_id"

    def test_graph_xor(self):
        """Tests the XOR overloaded operator."""
        # Get 2 Graph objects
        graph1 = query.causal_correlative_by_gene('CD33')
        graph2 = query.causal_correlative_by_gene('TREM2')

        # Check sum against xor
        xor = graph1 ^ graph2
        assert len(xor) == len(graph1) + len(graph2)

        # Check error is raised
        not_graph = query.list_pmids()  # Returns "Client" obj
        with pytest.raises(IOError) as e:
            graph1 ^ not_graph
        assert str(e.value) == err_msg

    def test_graph_add(self):
        """Tests the AND overloaded operator."""
        graph1 = query.causal_correlative_by_gene('CD33')
        graph2 = query.causal_correlative_by_gene('TREM2')

        # Check sum against xor
        summed_graphs = graph1 + graph2
        assert len(summed_graphs) == len(graph1) + len(graph2)

        # Check error is raised
        not_graph = query.list_pmids()  # Returns "Client" obj
        with pytest.raises(IOError) as e:
            graph1 + not_graph
        assert str(e.value) == err_msg

    def test_graph_sub(self):
        """Tests the subtraction overloaded operator."""
        graph1 = query.causal_correlative_by_gene('CD33')
        graph2 = query.causal_correlative_by_gene('CD33')  # Identical tables

        # Check sum against xor
        subbed_graphs = graph1 - graph2
        assert len(subbed_graphs) == 0
        assert subbed_graphs.table == "No results"

        # Check error is raised
        not_graph = query.list_pmids()  # Returns "Client" obj
        with pytest.raises(IOError) as e:
            graph1 + not_graph
        assert str(e.value) == err_msg
