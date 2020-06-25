from ebel_rest.manager.core import Graph, Client


def annotation(namespace: str, name: str = '') -> Graph:
    """Retrieve a list of BEL statements defined by a given namespace and name/term.

    :param str namespace: The namespace of the given name/term/value e.g. 'HGNC' or 'MGI'.
    :param str name: The term or value e.g. a protein symbol or MeSH term.
    :return: Graph of the results
    :rtype: Graph
    """
    return Graph().apply_api_function('_bel_by_annotation', namespace, name)


def last_author(namespace: str, name: str = '') -> Graph:
    return Graph().apply_api_function('_bel_by_last_author', namespace, name)


def pmid(pmid: int) -> Graph:
    return Graph().apply_api_function('_bel_by_pmid', pmid)


def list_pmids() -> list:
    """Returns a list of PMIDs in KG."""
    return Client().apply_api_function('all_pmids').table['distinct'].values.tolist()


def subgraph(namespace: str, name: str = '') -> Graph:
    return Graph().apply_api_function('_bel_by_subgraph', namespace, name)


def causal_correlative_by_gene(gene_symbol: str) -> Graph:
    return Graph().apply_api_function('_bel_causal_correlative_by_gene', gene_symbol)


def path(source: str, target: str, min_edges: int = 1, max_edges: int = 4) -> Graph:
    """Generates a graph of all paths from a source node to a target node.

    Parameters
    ----------
    source: str
        Label of the source node.
    target: str
        Label of the target node.
    min_edges: int
        The minimum number of edges between the source and target nodes. Must be > 1 and < max_edges.
    max_edges: int
        The maximum number of edges between the source and target nodes. Must be > min_edges.

    Returns
    -------
    Graph object
    """
    num_range = f"{min_edges}-{max_edges}"
    if min_edges > max_edges:
        raise ValueError("min_edges must be a smaller value than max_edges!")

    if min_edges < 1:
        raise ValueError("min_edges must a value greater than 1!")

    return Graph().apply_api_function('_bel_path', source, target, num_range)


def belish(statement: str) -> Graph:
    return Graph().apply_api_function('_belish', statement)


def find_contradictions() -> Client:
    return Client().apply_api_function('find_contradictions')


# TODO: Implemnet this in ebel
# def get_all_causal():
#     return Graph().apply_api_function('get_all_causal')
