__copyright__ = "Copyright (c) 2021 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

from typing import List, Tuple

from jina import DocumentArray, Executor, requests


class MatchMerger(Executor):
    """
    The MatchMerger merges the results of shards by appending all matches..
    """

    def __init__(self, default_traversal_paths: Tuple[str, ...] = ('r',), **kwargs):
        """
        :param default_traversal_paths: traverse path on docs, e.g. ['r'], ['c']
        """
        super().__init__(**kwargs)
        self.default_traversal_paths = default_traversal_paths

    @requests
    def merge(self, docs_matrix: List[DocumentArray], parameters: dict, **kwargs):
        traversal_paths = parameters.get(
            'traversal_paths', self.default_traversal_paths
        )
        results = {}
        for docs in docs_matrix:
            self._merge_shard(results, docs, traversal_paths)
        return DocumentArray(list(results.values()))

    def _merge_shard(self, results, docs, traversal_paths):
        for doc in docs.traverse_flat(traversal_paths):
            if doc.id in results:
                results[doc.id].matches.extend(doc.matches)
            else:
                results[doc.id] = doc
