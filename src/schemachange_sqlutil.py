import structlog
from schemachange.config.DeployConfig import DeployConfig
from schemachange.config.Plugin import Plugin, PluginBaseConfig
import dataclasses

logger = structlog.getLogger(__name__)

# Plugin specific imports


class SchemachangePlugin(Plugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plugin_name = "sqlutil"
        self.plugin_description = "Custom SQL utility plugin for schemachange"
        self.plugin_version = "0.1.0"
        self.plugin_author = "Sam Nelson"
        self.plugin_author_email = "sanelson@siliconfuture.net"

        # Plugin subcommands and their classes
        self.plugin_classes = {
            "deploy": DeployPluginConfig,
            "sqlutil": SQLUtilPluginConfig,
        }


@dataclasses.dataclass(frozen=True)
class SQLUtilPluginConfig(PluginBaseConfig):
    # Define the dataclass attributes for each plugin argument
    analyze_sql: bool = False  # Default value for the --analyze-sql argument

    plugin_subcommand = "sqlutil"
    plugin_parent_arguments = []
    plugin_subcommand_arguments = [
        {
            "name_or_flags": [
                "--analyze-sql",
            ],
            "action": "store_const",
            "const": True,
            "default": None,
            "help": "Analyze SQL and re-run all dependent R__ scripts of the changed/new R__ and new V__ scripts (the default is False)",
            "required": False,
        },
    ]

    def plugin_run(self):
        print("Running SQLUtilPlugin")
        return


@dataclasses.dataclass(frozen=True)
class DeployPluginConfig(PluginBaseConfig, DeployConfig):
    # Define the dataclass attributes for each plugin argument
    run_deps: bool = False  # Default value for the --run-deps argument
    rerun_repeatable: bool = False  # Default value for the --rerun-repeatable argument

    plugin_subcommand = "deploy"
    plugin_parent_arguments = []
    plugin_subcommand_arguments = [
        {
            "name_or_flags": [
                "--run-deps",
            ],
            "action": "store_const",
            "const": True,
            "default": None,
            "help": "Analyze SQL and re-run all dependent R__ scripts of the changed/new R__ and new V__ scripts (the default is False)",
            "required": False,
        },
        {
            "name_or_flags": [
                "--rerun-repeatable",
            ],
            "action": "store_const",
            "const": True,
            "default": None,
            "help": "Rerun ALL repeatable sc,ripts (the default is False)",
            "required": False,
        },
    ]

    def pre_command_tasks(self):
        print("Pre-command tasks")
        return

    def post_command_tasks(self):
        print("Post-command tasks")
        return
