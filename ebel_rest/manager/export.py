"""Module for exporting the knowledge graph in different formats."""
import os
import csv
import json
from typing import Tuple

from ebel_rest.manager.core import Client
from ebel_rest.constants import BEL, INDEX


def export_graph(graph_path: str,
                 output_file_format: str,
                 graph_delim: str = ',',
                 mapping_path: str = None,
                 map_delim: str = ',',
                 ) -> Tuple[str, str]:
    """Exports the Knowledge Graph to an output file.

    Parameters
    ----------
    graph_path: str
        Write file path.
    output_file_format: {'lst', 'sif', 'json', 'csv'}
        Graph export format. Can be on of the following:
            * Edge list (.lst)
            * SIF (Simple Interaction Format): tsv, txt
            * CSV
            * JSON
    mapping_path: str
        File path for generate mapping file of node identifiers to index. If None, defaults to same directory as given
        for graph_path.
    map_delim: {'\t', ',', ' '}
        A one-character string used to separate fields in the mapping file. It defaults to ','
    graph_delim: {'\t', ',', ' '}
        A one-character string used to separate fields in the graph file. It defaults to ','

    Raises
    ------
    ValueError
        If output_file_format is not one of the following formats: 'lst', 'csv', 'tsv', 'txt', 'json'.
        If 'sif' is the output_file_format and delimiter is not one of the following formats: '\t', ',', ' '.

    Returns
    -------
    path: str
        The path to which the file was written to.
    """
    exp = Exporter(graph_path, output_file_format, graph_delim, mapping_path, map_delim)
    return exp.export()


class Exporter:
    """Class for handling export requests."""

    def __init__(self,
                 graph_path: str,
                 output_file_format: str,
                 graph_delim: str = ',',
                 mapping_path: str = None,
                 map_delim: str = ',',):
        self.graph_path = graph_path
        self.output_file_format = output_file_format
        self.graph_delim = graph_delim
        self.mapping_path = mapping_path
        self.map_delim = map_delim
        self.odb_results = None
        self.mapping_dict = None

    def export(self):
        """Export the data using the initialized parameters."""
        odb_results = self.get_data()

        if odb_results:
            return self.write_results()

        else:
            return None

    def write_results(self, set_graph_file_format: str = None, set_graph_file_delim: str = None) -> Tuple[str, str]:
        """Write the retrieved data to file.

        Parameters
        ----------
        set_graph_file_format: str
            Allows one to change output file format.
        set_graph_file_delim: str
            Allows one to change graph file delimiter.

        Returns
        -------
        Tuple[str, str]
            The path to the graph results and the mapping file.
        """
        if set_graph_file_format is not None:
            self.output_file_format = set_graph_file_format

        if set_graph_file_delim is not None:
            self.graph_delim = set_graph_file_delim

        self._check_params()

        if self.output_file_format in ['sif', 'csv']:
            prepared_sif_data = self._prepare_sif_csv()
            graph_file = self._write_sif_csv_file(graph_data=prepared_sif_data)

        elif self.output_file_format == 'lst':
            prepared_list_data = self._prepare_edge_list()
            graph_file = self._write_edge_list_file(graph_data=prepared_list_data)

        else:
            graph_file = self._write_json()

        map_file = self._write_mapping()

        return graph_file, map_file

    def get_data(self) -> bool:
        """Retrieve the requested data from the OrientDB database."""
        # Set which API function to call
        api_func = "export_full" if self.output_file_format == 'json' else 'export_slim'

        self.odb_results = Client().apply_api_function(api_func).data  # raw data
        self.mapping_dict = self._create_mapping()  # Integer mappings

        if not self.odb_results or not self.mapping_dict:
            return False

        return True

    def _check_params(self):
        """Checks the passed parameters."""
        if self.output_file_format not in ['lst', 'sif', 'json', 'csv']:
            raise ValueError("output_file_format must be either 'lst', 'sif', 'csv', or 'json'")

        if self.output_file_format == 'sif' and self.graph_delim not in ['\t', ' ']:
            raise ValueError("Delimiter for a SIF must be either tab-separated ('\t') or space-separated (' ')")

    def _prepare_edge_list(self) -> list:
        """Prepares edge list data for export."""
        edges = []
        for rel in self.odb_results:
            out_node = self.mapping_dict[rel['out_rid']][INDEX]
            in_node = self.mapping_dict[rel['in_rid']][INDEX]
            edges.append((out_node, in_node))

        return edges

    def _write_edge_list_file(self, graph_data: list) -> str:
        """Method for writing edge list graph data to file."""
        with open(self.graph_path, 'w') as graph_file:
            graph_writer = csv.writer(graph_file, delimiter=" ")
            graph_writer.writerows(graph_data)

        return self.graph_path

    def _write_json(self) -> str:
        with open(self.graph_path, 'w') as graph_file:
            json.dump(self.odb_results, fp=graph_file)
        return self.graph_path

    def _write_mapping(self) -> str:
        """Method for writing mapping file."""
        if self.mapping_path is None:  # If no provided path for map file, create one...
            directory = os.path.dirname(self.graph_path)
            self.mapping_path = os.path.join(directory, "node_map.tsv")

        with open(self.mapping_path, 'w', encoding='utf-8') as map_file:
            map_writer = csv.writer(map_file, delimiter=self.map_delim or '\t')
            for rid, values in self.mapping_dict.items():
                index = values[INDEX]
                bel = values[BEL]
                map_writer.writerow((index, rid, bel))

        return self.mapping_path

    def _prepare_sif_csv(self) -> dict:
        """Method for preparing relation tuples and mappings for CSV and SIF files."""
        # Create a set of nodes and generate a mapping of RIDs to integers

        triples = dict()
        for rel in self.odb_results:
            out_node = self.mapping_dict[rel['out_rid']][INDEX]
            relation = rel['relation']
            in_node = self.mapping_dict[rel['in_rid']][INDEX]

            if out_node not in triples:
                triples[out_node] = {relation: [in_node]}

            elif relation not in triples[out_node]:
                triples[out_node][relation] = [in_node]

            else:
                triples[out_node][relation].append(in_node)

        return triples

    def _write_sif_csv_file(self, graph_data: dict) -> str:
        """Method for writing SIF or CSV graph data to file."""
        with open(self.graph_path, 'w') as graph_file:
            graph_writer = csv.writer(graph_file, delimiter=self.graph_delim or ',')
            for out_node in graph_data:
                for rel_type in graph_data[out_node]:
                    in_nodes = graph_data[out_node][rel_type]
                    values = [out_node, rel_type] + in_nodes
                    graph_writer.writerow(values)

        return self.graph_path

    def _create_mapping(self) -> dict:
        """Generates a mapping dict of rids to integers"""
        nodes = dict()

        # Map rids to their BEL statements
        for rel in self.odb_results:
            nodes[rel['out_rid']] = {BEL: rel['out_bel']}
            nodes[rel['in_rid']] = {BEL: rel['in_bel']}

        for index, rid in enumerate(set(nodes.keys())):
            nodes[rid][INDEX] = index

        return nodes
