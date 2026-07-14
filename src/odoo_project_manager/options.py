class Options:

    def __init__(self):
        self.target_ide: str | None = None
        self.source_location = None
        self.output_location = None
        self.project_name = None
        self.edition = "Enterprise"

    @classmethod
    def builder(cls) -> "Builder":
        return cls.Builder()

    @classmethod
    def auto_built(cls, options) -> "Options":
        builder = cls.builder()
        for k, v in options:
            if k in ["-s", "--project-source"]:
                builder.set_source_location(v)
            elif k in ["-l", "--output-location"]:
                builder.set_output_location(v)
            elif k in ["-e", "--edition"]:
                builder.set_edition(v)
            elif k in ["-n", "--name"]:
                builder.set_project_name(v)

        return builder.build()

    class Builder:

        def __init__(self) -> None:
            self._options = Options()

        def set_target_ide(self, target_ide):
            self._options.target_ide = target_ide

        def set_source_location(self, source_location):
            self._options.source_location = source_location

        def set_output_location(self, output_location):
            self._options.output_location = output_location

        def set_project_name(self, project_name):
            self._options.project_name = project_name

        def set_edition(self, edition):
            self._options.edition = edition

        def build(self):
            return self._options
