"""Main module."""
import os
import re
import json

import graphviz
import urllib.parse
import urllib.request
import pandas as pd
from IPython.display import display, Image

from ebel_rest.visualisation.colours.graphviz import edge_colours, node_colours
from ebel_rest.defaults import pics_path


class Connector:
    user = None
    password = None
    server = None
    db_name = None
    print_url = False


def connect(user, password, server, db_name, print_url=False) -> None:
    """Connects to the database.

    :param str user: Database username.
    :param str password: Database password for specified username.
    :param str server: Server or URL where database is hosted.
    :param str db_name: Name of database.
    :param bool print_url: Boolean to choose whether to print the REST API call.
    """
    Connector.user = user
    Connector.password = password
    Connector.server = server
    Connector.db_name = db_name
    Connector.print_url = print_url


class Client:
    def __init__(self):
        self._user = Connector.user
        self.__passwd = Connector.password
        self.url_template = f"{Connector.server}/function/{Connector.db_name}/{{function_name}}/{{arguments}}"
        self._data = None
        self.function_name = None
        self.print_url = Connector.print_url

    def _get_data(self, function_name, *args):
        """Get data ."""
        parameters = []
        for arg in args:
            parameters.append(urllib.parse.quote(str(arg)))
        url = self.url_template.format(
            function_name=function_name,
            arguments='/'.join(parameters))

        passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, self._user, self.__passwd)
        authhandler = urllib.request.HTTPBasicAuthHandler(passman)
        opener = urllib.request.build_opener(authhandler)
        urllib.request.install_opener(opener)
        if self.print_url:
            print(url)
        res = urllib.request.urlopen(url)
        res_body = res.read()

        self._data = json.loads(res_body, strict=False)['result']

    def apply_api_function(self, function_name, *args):
        self.function_name = function_name
        self._get_data(function_name, *args)
        return self

    @property
    def data(self):
        return [{k: v for k, v in x.items() if not k.startswith('@')} for x in self._data]

    @property
    def table(self):
        """Returns pandas dataframe."""
        if len(self._data):
            if 'edge_id' in self._data[0].keys():
                cols = ['subject_bel', 'relation', 'object_bel', 'pmid', 'edge_id']
                results = [tuple([x[col] for col in cols if col in x]) for x in self._data]
                df = pd.DataFrame(results, columns=cols)
                df.set_index('edge_id', inplace=True)
            else:
                results = [{k: v for k, v in x.items() if not k.startswith('@')} for x in self._data]
                df = pd.DataFrame(results)
            return df
        return "No results"


class Statistics(Client):
    # in the moment only a copy of Client
    pass


class Graph(Client):
    @property
    def edge_ids(self):
        return set([x['edge_id'] for x in self._data])

    @property
    def edges(self):
        data_unique = {x['edge_id']: x for x in self._data}
        return list(data_unique.values())

    def __xor__(self, other):
        """
        Return new graph with edges in either this or the other Graph object but not both.
        :param other: BEL graph
        :return: BEL graph
        """
        if isinstance(other, Graph):
            new_graph = Graph()
            set_edge_ids = self.edge_ids.symmetric_difference(other.edge_ids)
            union_edges = self.edges + other.edges
            new_graph._data = [x for x in union_edges if x['edge_id'] in set_edge_ids]
            new_graph.function_name = "joined_graph"
            return new_graph
        else:
            raise IOError('Second element is not a graph')

    def __or__(self, other):
        """Return new graph with edges in both graphs.

        :param other: BEL graph
        :return: BEL graph
        """
        return self.__add__(other)

    def __add__(self, other):
        """Return new graph with edges in both graphs.

        :param other: BEL graph
        :return: BEL graph
        """
        if isinstance(other, Graph):
            new_graph = Graph()
            set_edge_ids = self.edge_ids.union(other.edge_ids)
            union_edges = self.edges + other.edges
            new_graph._data = [x for x in union_edges if x['edge_id'] in set_edge_ids]
            new_graph.function_name = "joined_graph"
            return new_graph
        else:
            raise IOError('Second element is not a graph')

    def __sub__(self, other):
        """Return new graph with edges in this, but not the other graph.

        :param other: BEL graph
        :return: BEL graph
        """
        if isinstance(other, Graph):
            new_graph = Graph()
            set_edge_ids = self.edge_ids.difference(other.edge_ids)
            union_edges = self.edges + other.edges
            new_graph._data = [x for x in union_edges if x['edge_id'] in set_edge_ids]
            new_graph.function_name = "subtracted_graph"
            return new_graph
        else:
            raise IOError('Second element is not a graph')

    def __and__(self, other):
        """
        Return new graph with edges common to both graphs.
        :param other: BEL graph
        :return: BEL graph
        """
        if isinstance(other, Graph):
            new_graph = Graph()
            set_edge_ids = self.edge_ids.intersection(other.edge_ids)
            union_edges = self.edges + other.edges
            new_graph._data = [x for x in union_edges if x['edge_id'] in set_edge_ids]
            new_graph.function_name = "unioned_graph"
            return new_graph
        else:
            raise IOError('Second element is not a graph')

    def __ge__(self, other) -> bool:
        """Test whether every this graph is a supergraph of other graph."""
        if isinstance(other, Graph):
            return self.edge_ids.issuperset(other.edge_ids)
        else:
            raise IOError('Second element is not a graph')

    def __le__(self, other) -> bool:
        """Test whether every edge in this graph is in other graph."""
        if isinstance(other, Graph):
            return self.edge_ids.issubset(other.edge_ids)
        else:
            raise IOError('Second element is not a graph')

    def __len__(self) -> int:
        """Return number of edges.

        :return: int
        """
        return len(self.edge_ids)

    def __eq__(self, other):
        """Return true if both graphs are equivalent.

        :param other: BEL graph
        :return:
        """
        if isinstance(other, Graph):
            return self.edge_ids == other.edge_ids
        else:
            raise IOError('Second element is not a graph')

    def __ne__(self, other):
        """Return true if both graphs are not equivalent.

        :param other: BEL graph
        :return:
        """
        if isinstance(other, Graph):
            return self.edge_ids != other.edge_ids
        else:
            raise IOError('Second element is not a graph')

    def as_graph(self):
        """Creates a simple graph visualization."""
        self._ebel_graph(False, False)

    def as_graph_with_ids(self):
        """Creates a graph visualization that includes the edge ID numbers."""
        self._ebel_graph(True, False)

    def as_graph_bel(self):
        """Creates a graph visualization with the nodes as BEL statements."""
        self._ebel_graph(False, True)

    def as_graph_bel_with_ids(self):
        """Creates a graph visualization that includes both edge ID numbers and nodes as BEL statements."""
        self._ebel_graph(True, True)

    def _ebel_graph(self, with_edge_id, bel_names):
        rs = self.edges
        d = graphviz.Digraph(format='png')
        d.attr(size="300,300")
        d.attr('node', shape='box')
        d.attr('node', style='filled')

        node_names = []

        for i in range(len(rs)):
            for so in ['subject', 'object']:
                node_id = rs[i][f'{so}_id'] = rs[i][f'{so}_id'].replace(':', '.')
                if bel_names:
                    node_label = re.sub('"', '\"', rs[i][so + "_bel"])
                else:
                    involved = rs[i][so + "_involved_genes"] + rs[i][so + "_involved_other"]
                    node_label = ', '.join(involved)
                    node_label = rs[i][so + "_class"] + "\n" + node_label
                node_class = rs[i][so + "_class"]
                d.attr('node', fillcolor=node_colours.get(node_class, 'grey'))
                d.node(node_id, node_label)
                node_names.append(node_id)

        for r in rs:
            d.attr('edge', color=edge_colours.get(r['relation'], 'grey'))
            if with_edge_id:
                edge_lable = f"{r['relation']} {r['edge_id']}"
            else:
                edge_lable = r['relation']
            d.edge(r['subject_id'], r['object_id'], edge_lable)

        file_path = d.render(os.path.join(pics_path, self.function_name))
        display(Image(filename=file_path))

    @property
    def table_all_columns(self) -> pd.DataFrame:
        """Returns a pandas dataframe of the results."""
        cols = ['subject_bel',
                'relation',
                'object_bel',
                'annotation',
                'last_author',
                'publication_date',
                'title',
                'evidence',
                'pmid',
                'edge_id']
        if len(self._data):
            results = [tuple([x[col] for col in cols]) for x in self._data]
            df = pd.DataFrame(results, columns=cols)
            df.set_index('edge_id', inplace=True)
            return df
        return "No results"
