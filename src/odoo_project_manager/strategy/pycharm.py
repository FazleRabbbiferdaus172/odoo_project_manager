import os
from jinja2 import Environment, FileSystemLoader


from odoo_project_manager.options import Options
from odoo_project_manager.strategy.strategy import Strategy


class PycharmStrategy(Strategy):

    def __init__(self, manager, options: Options):
        super().__init__(manager, options)

    def run_create(self):
        super().run_create()
        self.generate_idea_things()

    def generate_idea_things(self):
        idea_template_path = os.path.join(
            self.root_directory, "sample", "pycharm", "pycharm_project_template"
        )
        self._generate_from_template(idea_template_path, self.project_path)

    def _generate_from_template(self, src_dir_path, dest_dir_path):
        env = Environment(loader=FileSystemLoader(src_dir_path))
        idea_module_path = os.path.join(self.project_path, ".idea")
        relative_odoo_community_path = os.path.relpath(self.odoo_path, idea_module_path)
        # Todo: change this
        relative_conf_path = os.path.relpath(self.odoo_path, idea_module_path)
        context_vars = {
            "relative_conf_path": relative_conf_path,
            "relative_odoo_community_path": relative_odoo_community_path,
            "relative_odoo_enterprise_path": relative_odoo_community_path,
            "jdk_name": f"Python ({self.options.project_name})",
            "project_name": self.options.project_name,
        }
        for root, dirs, files in os.walk(src_dir_path):
            for file in files:
                # Construct the full absolute or relative path to the source file
                src_path = os.path.join(root, file)

                rel_path = os.path.relpath(src_path, src_dir_path)

                # 2. Split the path to isolate the file name from its folders
                dir_name, file_name = os.path.split(rel_path)

                if "project_module" in file_name:
                    file_name = file_name.replace(
                        "project_module", self.options.project_name
                    )

                rel_dest_path = os.path.join(dir_name, file_name)

                dest_path = os.path.join(dest_dir_path, rel_dest_path)

                dest_dir_path_now = os.path.dirname(dest_path)
                os.makedirs(dest_dir_path_now, exist_ok=True)

                # Check if the file is a Jinja template
                if src_path.endswith(".jinja"):
                    template_name = rel_path.replace(os.sep, "/")
                    template = env.get_template(template_name)
                    rendered_content = template.render(context_vars)

                    # Remove the '.j2' extension from the final file name
                    final_dest_path = os.path.splitext(dest_path)[0]

                    # Write the rendered content to the new file
                    with open(final_dest_path, "w", encoding="utf-8") as f:
                        f.write(rendered_content)

                    print(f"Rendered: {final_dest_path}")
        # breakpoint()

    def execute(self):
        super().execute()
        print(f"executed:  {self.manager.commands} options {self.manager.options}")
