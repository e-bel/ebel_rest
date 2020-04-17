from .core import Graph
from typing import List


def annotation(namespace: str, name: str = '') -> Graph:
    """Retrieve a list of BEL statements defined by a given namespace and name/term.

    :param str namespace: The namespace of the given name/term/value e.g. 'HGNC' or 'MGI'.
    :param str name: The term or value e.g. a protein symbol or MeSH term.
    :return: Graph of the results
    :rtype: Graph
    """
    return Graph().apply_api_function('_bel_by_annotation', namespace, name)


def authors(author_list: List[str], edge_class: str = '', node_class: str = '', exclude_namespace: str = '') -> Graph:
    """Retrieve a list of BEL statements defined by a list of authors. For greater specificity, an edge and node class
    can be passed to filter results as well as namespaces to exclude.

    :param List[str] author_list: List of author names of publications.
    :param str edge_class: Desired edge class to filter results by.
    :param str node_class: Desired node class to filter results by.
    :param str exclude_namespace: Namespace to exclude in result set.
    :return: Graph of the results.
    :rtype: Graph
    """
    authors_query_str = ",".join(author_list)
    return Graph().apply_api_function('_bel_by_authors',
                                      authors_query_str,
                                      edge_class,
                                      node_class,
                                      exclude_namespace)


def last_author(namespace: str, name: str = '') -> Graph:
    return Graph().apply_api_function('_bel_by_last_author', namespace, name)


def pmid(pmid: int) -> Graph:
    return Graph().apply_api_function('_bel_by_pmid', pmid)


def subgraph(namespace: str, name: str = '') -> Graph:
    return Graph().apply_api_function('_bel_by_subgraph', namespace, name)


def causal_correlative_by_gene(gene_symbol: str) -> Graph:
    return Graph().apply_api_function('_bel_causal_correlative_by_gene', gene_symbol)


def path(from_gene: str, to_gene: str, min_edges: int = 1, max_edges: int = 4) -> Graph:
    num_range = f"{min_edges}-{max_edges}"
    return Graph().apply_api_function('_bel_path', from_gene, to_gene, num_range)


def belish(statement: str) -> Graph:
    return Graph().apply_api_function('_belish', statement)


# TODO: Implemnet this in ebel
# def get_all_causal():
#     return Graph().apply_api_function('get_all_causal')
