import logging

from nameko.dependency_providers import Config
from nameko.rpc import rpc, RpcProxy

from .models import Churn
from .schemas import DeltasSchema, ChurnSchema

logger = logging.getLogger(__name__)


def _get_churn(deltas):
    for delta in deltas.deltas.values():
        return Churn(delta.insertions, delta.deletions)
    return None


class ChurnService:
    name = 'churn'

    config = Config()
    parser_rpc = RpcProxy('parser')
    repository_rpc = RpcProxy('repository')

    @rpc
    def collect(self, project, sha, path, **options):
        logger.debug(project)

        deltas = self._get_deltas(project, sha, path)
        return ChurnSchema().dump(_get_churn(deltas))

    def _get_deltas(self, project, sha, path):
        deltas = self.repository_rpc.get_deltas(project, sha, path)
        return DeltasSchema().load(deltas)
