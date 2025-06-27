from .config.config_manager import load_config, TEMPLATES_FILE

class TemplateManager:
    def __init__(self):
        self.templates = load_config(TEMPLATES_FILE)

    def get_template(self, name):
        return self.templates.get(name)

    def list_templates(self):
        return list(self.templates.keys())
