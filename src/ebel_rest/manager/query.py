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


def path(from_gene: str, to_gene: str, min_edges: int = 1, max_edges: int = 4) -> Graph:
    num_range = f"{min_edges}-{max_edges}"
    return Graph().apply_api_function('_bel_path', from_gene, to_gene, num_range)


def belish(statement: str) -> Graph:
    return Graph().apply_api_function('_belish', statement)


def find_contradictions() -> Client:
    return Client().apply_api_function('find_contradictions')


# TODO: Implemnet this in ebel
# def get_all_causal():
#     return Graph().apply_api_function('get_all_causal')
