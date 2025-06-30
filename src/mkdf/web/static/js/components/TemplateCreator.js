const TemplateCreator = {
    template: `
        <div class="tab-content">
            <h2>Templates</h2>
            <div class="form-group">
                <label for="template-project-name">Project Name:</label>
                <input type="text" id="template-project-name" v-model="templateProjectName">
            </div>
            <div class="form-group">
                <label for="template-type">Template Type:</label>
                <select id="template-type" v-model="selectedTemplate">
                    <option value="simple">Simple</option>
                    <option value="low_level">Low Level (C/C++)</option>
                    <option value="react">React</option>
                    <option value="vue">Vue</option>
                    <option value="flask">Flask</option>
                    <option value="fastapi">FastAPI</option>
                    <option value="express">Express</option>
                    <option value="laravel">Laravel</option>
                    <option value="slim">Slim</option>
                </select>
            </div>
            <button @click="createTemplate"><i class="fas fa-plus-circle"></i> Create Project</button>
        </div>
    `,
    data() {
        return {
            templateProjectName: '',
            selectedTemplate: 'simple'
        };
    },
    methods: {
        /**
         * Fetches available templates from the server.
         * This method can be expanded to populate the template options dynamically.
         */
        async get_templates() {
            try {
                const response = await fetch('/api/templates');
                const data = await response.json();
                if (data.templates) {
                    this.templates = data.templates;
                } else {
                    console.error('No templates found');
                }
            } catch (error) {
                console.error('Error fetching templates:', error);
            }
        },

        /**
         * Creates a new project template based on the selected type.
         * Sends a POST request to the server with the project name and template type.
         */
        async createTemplate() {
            try {
                const response = await fetch('/create_template', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ project_name: this.templateProjectName, template_type: this.selectedTemplate }),
                });
                const data = await response.json();
                alert(data.message); // Replace with a proper notification system
            } catch (error) {
                alert(`Error creating project: ${error}`); // Replace with a proper notification system
            }
            }
        },
        mounted() {
            /**
             * Initializes the component by fetching available templates from the server.
             */
            this.get_templates();
        }
    }
