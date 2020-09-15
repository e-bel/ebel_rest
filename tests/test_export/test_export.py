"""Export module tests."""
import os
import pytest

from ebel_rest import connect, export_graph
from ebel_rest.manager.export import Exporter
from ebel_rest.defaults import LIBRARY_PATH
from ..constants import USER, PASSWORD, DATABASE, SERVER

TEST_GRAPH_FILE = 'graph_test.txt'
TEST_MAP_FILE = 'map_test.txt'

TEST_GFP = os.path.join(LIBRARY_PATH, TEST_GRAPH_FILE)
TEST_MFP = os.path.join(LIBRARY_PATH, TEST_MAP_FILE)
TEST_MISSING_MFP = os.path.join(LIBRARY_PATH, "node_map.tsv")

connect(USER, PASSWORD, SERVER, DATABASE)

exp = Exporter(graph_path=TEST_GFP, output_file_format='lst', mapping_path=TEST_MFP)
data_check = exp.get_data()


class TestExport:

    def test_get_data(self):
        assert data_check is True

    def test_edge_list(self):
        gfp, mfp = exp.write_results()
        assert os.path.isfile(gfp)
        assert os.path.isfile(mfp)
        assert os.path.getsize(gfp) > 0  # Check file is not empty
        assert os.path.getsize(mfp) > 0

    def test_sif(self):
        gfp, mfp = exp.write_results(set_graph_file_format='sif', set_graph_file_delim='\t')
        assert os.path.isfile(gfp)
        assert os.path.isfile(mfp)
        assert os.path.getsize(gfp) > 0  # Check file is not empty
        assert os.path.getsize(mfp) > 0

    def test_csv(self):
        gfp, mfp = exp.write_results(set_graph_file_format='csv', set_graph_file_delim=',')
        assert os.path.isfile(gfp)
        assert os.path.isfile(mfp)
        assert os.path.getsize(gfp) > 0  # Check file is not empty
        assert os.path.getsize(mfp) > 0

    def test_json(self):
        gfp, mfp = export_graph(graph_path=TEST_GFP, output_file_format='lst', mapping_path=TEST_MFP)
        assert os.path.isfile(gfp)
        assert os.path.isfile(mfp)
        assert os.path.getsize(gfp) > 0  # Check file is not empty
        assert os.path.getsize(mfp) > 0

    def test_output_format_defense(self):
        with pytest.raises(ValueError) as e:
            export_graph(graph_path=TEST_GFP, output_file_format='foo', mapping_path=TEST_MFP)
        assert str(e.value) == "output_file_format must be either 'lst', 'sif', 'csv', or 'json'"

    def test_missing_map_path(self):
        export_graph(graph_path=TEST_GFP, output_file_format='sif', graph_delim='\t')

    def test_delim_defense(self):
        with pytest.raises(ValueError) as e:
            export_graph(graph_path=TEST_GFP,
                                    output_file_format='sif',
                                    mapping_path=TEST_MFP,
                                    graph_delim='^',)
        assert str(e.value) == "Delimiter for a SIF must be either tab-separated ('\t') or space-separated (' ')"

    def test_remove_test_files(self):
        if os.path.isfile(TEST_GFP):
            os.remove(TEST_GFP)

        if os.path.isfile(TEST_MFP):
            os.remove(TEST_MFP)

        if os.path.isfile(TEST_MISSING_MFP):
            os.remove(TEST_MISSING_MFP)

        assert not os.path.isfile(TEST_MFP)
        assert not os.path.isfile(TEST_MFP)
        assert not os.path.isfile(TEST_MISSING_MFP)
