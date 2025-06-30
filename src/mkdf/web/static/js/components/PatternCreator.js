const PatternCreator = {
    template: `
        <div class="tab-content">
            <h2>Pattern Creator</h2>
            <div class="form-group">
                <label for="pattern-input">Pattern:</label>
                <input type="text" id="pattern-input" v-model="patternInput" @input="previewPattern" placeholder="e.g., myapp/{src/,docs/,README.md}">
            </div>
            <div class="form-group">
                <label>Preview:</label>
                <pre class="tree-preview">{{ patternPreview }}</pre>
            </div>
            <button @click="createPattern"><i class="fas fa-plus-circle"></i> Create Project</button>
        </div>
    `,
    data() {
        return {
            patternInput: '',
            patternPreview: ''
        };
    },
    methods: {
        async previewPattern() {
            const pattern = this.patternInput;
            if (pattern) {
                try {
                    const response = await fetch('/preview_pattern', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ pattern: pattern }),
                    });
                    const data = await response.json();
                    if (data.success) {
                        this.patternPreview = data.tree;
                    } else {
                        this.patternPreview = `Error: ${data.error}`;
                    }
                } catch (error) {
                    this.patternPreview = `Error fetching preview: ${error}`;
                }
            } else {
                this.patternPreview = '';
            }
        },
        async createPattern() {
            const pattern = this.patternInput;
            try {
                const response = await fetch('/create_pattern', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ pattern: pattern }),
                });
                const data = await response.json();
                alert(data.message); // Replace with a proper notification system
            } catch (error) {
                alert(`Error creating project: ${error}`); // Replace with a proper notification system
            }
        }
    }
};
