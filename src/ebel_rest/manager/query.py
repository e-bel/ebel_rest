from ebel_rest.manager.core import Graph, Client
from ebel_rest.manager import ss_functions


def annotation(namespace: str, name: str = '') -> Graph:
    """Retrieve a list of BEL statements defined by a given namespace and name/term.

    :param str namespace: The namespace of the given name/term/value e.g. 'HGNC' or 'MGI'.
    :param str name: The term or value e.g. a protein symbol or MeSH term.
    :return: Graph of the results
    :rtype: Graph
    """
    return Graph().apply_api_function(ss_functions.BEL_BY_ANNOTATION, namespace, name)


def last_author(author: str, edge_class: str = '', node_class: str = '', exclude_namespace: str = '') -> Graph:
    """Retrieve a list of BEL statements defined by a last author and filtered using edge/node classes or
    node namespace.

    Parameters
    ----------
    author: str
        Last name and first initial of the last author of a publication e.g. "Neumann H".
    edge_class: str
        Type of edge class to include in results. Can be specific (e.g. 'increases') or a parent class (e.g. 'causal').
    node_class: str
        Type of node class to include in results. Can be specific (e.g. 'protein') or a parent class (e.g. 'bel').
    exclude_namespace: str
        A namespace to exclude such as 'MGI' to exclude mouse proteins.

    Returns
    -------
    Graph object.
    """
    return Graph().apply_api_function(ss_functions.BEL_BY_LAST_AUTHOR,
                                      author,
                                      edge_class,
                                      node_class,
                                      exclude_namespace)


def pmid(pmid: int) -> Graph:
    """Retrieve a list of BEL statements extracted from a given PMID.

    Parameters
    ----------
    pmid: int
        PubMed ID of a publication.

    Returns
    -------
    Graph
    """
    return Graph().apply_api_function(ss_functions.BEL_BY_PMID, pmid)


def list_pmids() -> list:
    """Returns a list of curated PMIDs in the knowledge graph."""
    return Client().apply_api_function(ss_functions.ALL_PMIDS).table['pmid'].values.tolist()


def subgraph(subgraph_name: str = '') -> Graph:
    """Retrieve a list of BEL statements with the given subgraph_name in their annotations.

    Parameters
    ----------
    subgraph_name: str
        The name of an annotation used for identifying relationships part of a subgraph or pathway.

    Returns
    -------
    Graph
    """
    return Graph().apply_api_function(ss_functions.BEL_BY_SUBGRAPH, subgraph_name)


def causal_correlative_by_gene(gene_symbol: str) -> Graph:
    return Graph().apply_api_function(ss_functions.BEL_CAUSAL_CORRELATIVE_BY_GENE, gene_symbol)


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

    return Graph().apply_api_function(ss_functions.BEL_PATH, source, target, num_range)


def belish(statement: str) -> Graph:
    """Retrieve a list of BEL statements that match the given customized BEL statement.

    Parameters
    ----------
    statement: str
        BEL like statement in which "?" serve as wild cards. Example: 'p(?) causal p(?)'

    Returns
    -------
    Graph
    """
    return Graph().apply_api_function(ss_functions.BELISH, statement)


def find_contradictions() -> Client:
    """Returns a list of contradictions in the knowledge graph. A contradiction is defined as edges of opposite
    types (e.g. increases/decreases) existing between the same out node and in node."""
    return Client().apply_api_function('find_contradictions')


def sql(sql_query: str = '') -> Client:
    """Executes an SQL function in the Knowledge Graph.

    :param str sql_query: a valid OrientDB style SQL query for a knowledge graph built by e(BE:L).
    :return: Client
    """
    return Client().apply_api_function(ss_functions.DIRECT_SQL, sql_query)
