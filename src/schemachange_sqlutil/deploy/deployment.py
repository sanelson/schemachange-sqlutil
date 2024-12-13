import structlog
import re
from schemachange.deploy import Deployment
from schemachange.config.Plugin import Plugin, PluginBaseConfig, PluginJobConfig

logger = structlog.getLogger(__name__)

# Plugin specific imports


class DependentDeployment(Deployment):
    # Overload the run method to rerun all repeatable scripts after main deployment
    def run(self):
        # Run the main deployment
        self.deploy()
