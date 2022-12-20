"""Export module tests."""
import os
import pytest
import pathlib

from ebel_rest import connect, export_graph
from ebel_rest import Exporter
from ..constants import USER, PASSWORD, DATABASE, SERVER

EXPORT_DIR = pathlib.Path(__file__).parent.absolute()

TEST_GFP = os.path.join(EXPORT_DIR, 'graph_test.txt')
TEST_MFP = os.path.join(EXPORT_DIR, 'map_test.txt')
TEST_MISSING_MFP = os.path.join(EXPORT_DIR, "node_map.tsv")

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
            exp.write_results(set_graph_file_format='foo')
        assert str(e.value) == "output_file_format must be either 'lst', 'sif', 'csv', or 'json'"

    def test_delim_defense(self):
        with pytest.raises(ValueError) as e:
            exp.write_results(set_graph_file_format='sif', set_graph_file_delim='^')
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
