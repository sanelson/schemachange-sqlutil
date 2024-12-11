import structlog
import re
from schemachange.job import Job
from schemachange.config.Plugin import Plugin, PluginBaseConfig, PluginJobConfig

logger = structlog.getLogger(__name__)

# Plugin specific imports


class RerunJob(Job):
    def run_script(self, script):
        logger.info(f"(Re)running script: {script.name}")

        # Render the script content
        content = self.render_script_content(script)

        # Execute the script
        self.session.apply_change_script(
            script=script,
            script_content=content,
            dry_run=self.config.dry_run,
            logger=logger,
        )

        if self.config.dry_run:
            logger.info("Dry run, script not applied")
            self.scripts_skipped += 1
        else:
            self.scripts_applied += 1

    def run(self):
        if self.config.rerun_repeatable:
            logger.info("Rerunning all repeatable scripts")

            # We can ignore script history, or can we?

            # Get all scripts
            self.find_scripts()

            # Loop through all scripts
            for script in self.all_scripts.values():
                if script.type == "R":
                    self.run_script(script)
            logger.info(
                "Completed successfully",
                scripts_applied=self.scripts_applied,
                scripts_skipped=self.scripts_skipped,
            )

        elif self.config.rerun_repeatable_pattern:
            # Repeatable pattern runs against file path so in addition to the script name we can also include based on a folder
            pattern = self.config.rerun_repeatable_pattern.strip(" '")
            logger.info(
                "Rerunning repeatable scripts with pattern",
                pattern=pattern,
            )
            regex = None
            try:
                # Compile the pattern
                regex = re.compile(pattern)
            except re.error as e:
                logger.error(
                    "Invalid repeatable pattern",
                    pattern=pattern,
                    error=str(e),
                )
                raise

            # Get all scripts
            self.find_scripts()

            # Loop through all scripts
            for script in self.all_scripts.values():
                if script.type == "R" and regex.match(str(script.file_path)):
                    self.run_script(script)
            logger.info(
                "Completed successfully",
                scripts_applied=self.scripts_applied,
                scripts_skipped=self.scripts_skipped,
            )

        return
