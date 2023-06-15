"""Top-level package for eBEL API client."""

from ebel_rest.manager.core import connect
from ebel_rest.manager.export import export_graph, Exporter
from ebel_rest.manager import export, query, statistics


__author__ = """Christian Ebeling"""
__email__ = 'Christian.Ebeling@scai.fraunhofer.de'
__version__ = '1.0.24'
