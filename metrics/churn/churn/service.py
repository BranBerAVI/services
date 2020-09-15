import logging

from nameko.dependency_providers import Config
from nameko.rpc import rpc, RpcProxy

from .models import Churn
from .schemas import DeltasSchema, ChurnSchema, ProjectSchema

logger = logging.getLogger(__name__)


def _get_churn(deltas):
    deltas = ((d.commit, p, dd) for d in deltas for p, dd in d.deltas.items())
    for commit, path, delta in deltas:
        yield Churn(commit, path, delta.insertions, delta.deletions)


class ChurnService:
    name = 'churn'

    config = Config()
    parser_rpc = RpcProxy('parser')
    project_rpc = RpcProxy('project')
    repository_rpc = RpcProxy('repository')

    @rpc
    def collect(self, project, sha, **options):
        logger.debug(project)

        project = ProjectSchema().load(self.project_rpc.get(project))
        deltas = self._get_deltas(project, sha)
        return ChurnSchema(many=True).dump(_get_churn(deltas))

    def _get_deltas(self, project, sha):
        deltas = self.repository_rpc.get_deltas(project.name, sha)
        return DeltasSchema(many=True).load(deltas)
