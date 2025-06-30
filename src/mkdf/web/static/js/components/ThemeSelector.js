const ThemeSelector = {
    template: `
        <div class="theme-selector">
            <label for="theme-select"><i class="fas fa-palette"></i></label>
            <select id="theme-select" v-model="selectedTheme" @change="setTheme(selectedTheme)">
                <option v-for="theme in themes" :value="theme">{{ theme }}</option>
            </select>
        </div>
    `,
    data() {
        return {
            themes: [],
            selectedTheme: localStorage.getItem('selectedTheme') || 'dark'
        };
    },
    methods: {
        async getThemes() {
            const response = await fetch('/api/themes');
            const data = await response.json();
            this.themes = data.artistic;
        },
        setTheme(theme) {
            this.selectedTheme = theme;
            localStorage.setItem('selectedTheme', theme);
            document.getElementById('theme-link').href = `/static/css/${theme}.css`;
        }
    },
    mounted() {
        this.getThemes();
        this.setTheme(this.selectedTheme); // Apply theme on mount
    }
};
