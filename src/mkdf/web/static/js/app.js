
const { createApp } = Vue

createApp({
    data() {
        return {
            themes: [],
            selectedTheme: 'dark'
        }
    },
    methods: {
        async getThemes() {
            const response = await fetch('/api/themes');
            const data = await response.json();
            this.themes = data.artistic;
        },
        setTheme(theme) {
            this.selectedTheme = theme;
            document.getElementById('theme-link').href = `/static/css/${theme}.css`;
        }
    },
    mounted() {
        this.getThemes();
    }
}).mount('#app');
