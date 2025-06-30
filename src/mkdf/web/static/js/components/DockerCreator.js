const DockerCreator = {
    template: `
        <div class="tab-content">
            <h2>Docker Combos</h2>
            <div class="form-group">
                <label for="docker-project-name">Project Name:</label>
                <input type="text" id="docker-project-name" v-model="dockerProjectName">
            </div>
            <div class="form-group">
                <label>Components:</label>
                <div class="component-grid">
                    <div class="component-category">
                        <h4>Backend</h4>
                        <div class="component-list">
                            <label v-for="component in dockerComponents.backend" :key="component" class="component-item">
                                <input type="checkbox" :value="component" v-model="selectedDockerComponents" @change="previewDockerCompose">
                                {{ component }}
                            </label>
                        </div>
                    </div>
                    <div class="component-category">
                        <h4>Frontend</h4>
                        <div class="component-list">
                            <label v-for="component in dockerComponents.frontend" :key="component" class="component-item">
                                <input type="checkbox" :value="component" v-model="selectedDockerComponents" @change="previewDockerCompose">
                                {{ component }}
                            </label>
                        </div>
                    </div>
                    <div class="component-category">
                        <h4>Databases</h4>
                        <div class="component-list">
                            <label v-for="component in dockerComponents.databases" :key="component" class="component-item">
                                <input type="checkbox" :value="component" v-model="selectedDockerComponents" @change="previewDockerCompose">
                                {{ component }}
                            </label>
                        </div>
                    </div>
                    <div class="component-category">
                        <h4>Infrastructure</h4>
                        <div class="component-list">
                            <label v-for="component in dockerComponents.infrastructure" :key="component" class="component-item">
                                <input type="checkbox" :value="component" v-model="selectedDockerComponents" @change="previewDockerCompose">
                                {{ component }}
                            </label>
                        </div>
                    </div>
                </div>
            </div>
            <div class="form-group">
                <label>Docker Compose Preview:</label>
                <pre class="tree-preview">{{ dockerComposePreview }}</pre>
            </div>
            <button @click="createDocker"><i class="fas fa-plus-circle"></i> Create Project</button>
        </div>
    `,
    data() {
        return {
            dockerProjectName: '',
            dockerComponents: {
                backend: ['fastapi', 'flask', 'express', 'laravel', 'slim', 'django', 'springboot', 'aspnet', 'gofiber', 'echo', 'ruby-rails'],
                frontend: ['react', 'vue', 'nextjs', 'nuxtjs', 'angular', 'svelte', 'static'],
                databases: ['postgresql', 'mysql', 'mongodb', 'redis', 'mariadb', 'rabbitmq', 'kafka'],
                infrastructure: ['nginx', 'traefik', 'caddy', 'monitoring']
            },
            selectedDockerComponents: [],
            dockerComposePreview: ''
        };
    },
    methods: {
        async previewDockerCompose() {
            const components = this.selectedDockerComponents;
            if (components.length > 0) {
                try {
                    const response = await fetch('/preview_docker_compose', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ components: components }),
                    });
                    const data = await response.json();
                    if (data.success) {
                        this.dockerComposePreview = data.compose_yml;
                    } else {
                        this.dockerComposePreview = `Error: ${data.error}`;
                    }
                } catch (error) {
                    this.dockerComposePreview = `Error fetching Docker Compose preview: ${error}`;
                }
            } else {
                this.dockerComposePreview = '';
            }
        },
        async createDocker() {
            const projectName = this.dockerProjectName;
            const components = this.selectedDockerComponents;
            try {
                const response = await fetch('/create_docker', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ project_name: projectName, components: components }),
                });
                const data = await response.json();
                alert(data.message); // Replace with a proper notification system
            } catch (error) {
                alert(`Error creating project: ${error}`); // Replace with a proper notification system
            }
        }
    }
};
