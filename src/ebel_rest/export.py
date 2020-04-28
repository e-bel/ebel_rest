"""Module for exporting the knowledge graph in different formats."""
import os
import csv
import json
from typing import Tuple, List

from .core import Client
from .constants import BEL, INDEX


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
    if output_file_format not in ['lst', 'sif', 'json', 'csv']:
        raise ValueError("output_file_format must be either 'lst', 'sif', 'csv', or 'json'")

    if output_file_format == 'sif' and graph_delim not in ['\t', ' ']:
        raise ValueError("delimiter for a SIF must be either tab-separated ('\t') or space-separated (' ')")

    # Set which API function to call
    api_func = "export_full" if output_file_format == 'json' else 'export_slim'

    odb_results = Client().apply_api_function(api_func).data  # raw data
    mapping_dict = _create_mapping(relations=odb_results)  # Integer mappings

    if output_file_format in ['sif', 'csv']:
        prepared_sif_data = _prepare_sif_csv(odb_relations=odb_results, mapping=mapping_dict)
        graph_file = _write_sif_csv_file(graph_path=graph_path,
                                         graph_data=prepared_sif_data,
                                         delimiter=graph_delim)

    elif output_file_format == 'lst':
        prepared_list_data = _prepare_edge_list(odb_relations=odb_results, mapping=mapping_dict)
        graph_file = _write_edge_list_file(graph_path=graph_path, graph_data=prepared_list_data)

    else:
        graph_file = _write_json(graph_path=graph_path, graph_data=odb_results)

    map_file = _write_mapping(mapping_data=mapping_dict,
                              graph_path=graph_path,
                              delimiter=map_delim,
                              mapping_path=mapping_path)

    return graph_file, map_file


def _prepare_edge_list(odb_relations: List[dict], mapping: dict) -> list:
    """Prepares edge list data for export."""
    edges = []
    for rel in odb_relations:
        out_node = mapping[rel.pop('out_rid')][INDEX]
        in_node = mapping[rel.pop('in_rid')][INDEX]
        edges.append((out_node, in_node))

    return edges


def _write_edge_list_file(graph_path: str, graph_data: list) -> str:
    """Method for writing edge list graph data to file."""
    with open(graph_path, 'w') as graph_file:
        graph_writer = csv.writer(graph_file, delimiter=" ")
        graph_writer.writerows(graph_data)

    return graph_path


def _write_json(graph_path: str, graph_data: dict) -> str:
    with open(graph_path, 'w') as graph_file:
        json.dump(graph_data, fp=graph_file)

    return graph_path


def _write_mapping(mapping_data: dict, graph_path: str, delimiter: str, mapping_path: str = None) -> str:
    """Method for writing mapping file."""
    if mapping_path is None:  # If no provided path for map file, create one...
        directory = os.path.dirname(graph_path)
        mapping_path = os.path.join(directory, "node_map.tsv")

    with open(mapping_path, 'w') as map_file:
        map_writer = csv.writer(map_file, delimiter=delimiter or '\t')
        for rid, values in mapping_data.items():
            index = values[INDEX]
            bel = values[BEL]
            map_writer.writerow((index, rid, bel))

    return mapping_path


def _prepare_sif_csv(odb_relations: List[dict], mapping: dict) -> dict:
    """Method for preparing relation tuples and mappings for CSV and SIF files."""
    # Create a set of nodes and generate a mapping of RIDs to integers

    triples = dict()
    for rel in odb_relations:
        out_node = mapping[rel.pop('out_rid')][INDEX]
        relation = rel.pop('relation')
        in_node = mapping[rel.pop('in_rid')][INDEX]

        if out_node not in triples:
            triples[out_node] = {relation: [in_node]}

        elif relation not in triples[out_node]:
            triples[out_node][relation] = [in_node]

        else:
            triples[out_node][relation].append(in_node)

    return triples


def _write_sif_csv_file(graph_path: str, graph_data: dict, delimiter: str = None) -> str:
    """Method for writing SIF or CSV graph data to file."""
    with open(graph_path, 'w') as graph_file:
        graph_writer = csv.writer(graph_file, delimiter=delimiter or ',')
        for out_node in graph_data:
            for rel_type in graph_data[out_node]:
                in_nodes = graph_data[out_node][rel_type]
                values = [out_node, rel_type] + in_nodes
                graph_writer.writerow(values)

    return graph_path


def _create_mapping(relations: List[dict], ) -> dict:
    """Generates a mapping dict of rids to integers"""
    nodes = dict()

    # Map rids to their BEL statements
    for rel in relations:
        nodes[rel['out_rid']] = {BEL: rel['out_bel']}
        nodes[rel['in_rid']] = {BEL: rel['in_bel']}

    for index, rid in enumerate(set(nodes.keys())):
        nodes[rid][INDEX] = index

    return nodes
