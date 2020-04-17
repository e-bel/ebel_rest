from .core import Statistics


def publication_by_year() -> Statistics:
    """Returns statistics on the number of publications per year in the knowledge graph."""
    return Statistics().apply_api_function('_bel_statistics_publication_by_year')


def publication_by_number_of_statements() -> Statistics:
    """Returns statistics on the number of statements per publication in the knowledge graph."""
    return Statistics().apply_api_function('_bel_statistics_publication_by_number_of_statements')


def last_author_by_number_of_publications() -> Statistics:
    """Returns statistics on the number of publications per author in the knowledge graph."""
    return Statistics().apply_api_function('_bel_statistics_last_author_by_number_of_publications')


def last_author_by_number_of_statements() -> Statistics():
    """Returns statistics on the number of statements per author in the knowledge graph."""
    return Statistics().apply_api_function('_bel_statistics_last_author_by_number_of_statements')


def node_namespace_order_by_count() -> Statistics():
    """Returns statistics on the frequency of each node type and each namespace in the knowledge graph
    in order of count."""
    return Statistics().apply_api_function('_bel_statistics_node_namespace_order_by_count')


def node_namespace_order_by_namespace() -> Statistics():
    return Statistics().apply_api_function('_bel_statistics_node_namespace_order_by_namespace')


def edges() -> Statistics():
    """Returns statistics on the frequency of each edge type in the knowledge graph."""
    return Statistics().apply_api_function('_bel_statistics_edges')


def nodes() -> Statistics():
    """Returns statistics on the frequency of each node type in the knowledge graph."""
    return Statistics().apply_api_function('_bel_statistics_nodes')


def total_bel_nodes() -> Statistics():
    """Returns the total number of nodes generated from curated statements in the knowledge graph."""
    return Statistics().apply_api_function('bel_statistics_total_bel_nodes')


def total_bel_edges() -> Statistics():
    """Returns the total number of BEL curated edges in the knowledge graph."""
    return Statistics().apply_api_function('bel_statistics_total_stmts')


def total_publications() -> Statistics():
    """Returns the total number of publications in the knowledge graph."""
    return Statistics().apply_api_function('bel_statistics_total_publications')


def subgraphs() -> Statistics():
    return Statistics().apply_api_function('_bel_statistics_subgraph')
