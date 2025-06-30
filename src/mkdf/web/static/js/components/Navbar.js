const Navbar = {
    components: {
        'theme-selector': ThemeSelector
    },
    template: `
        <header class="navbar">
            <div class="brand">
                <h1><i class="fas fa-folder-plus"></i> MKDF</h1>
                <span class="version">v1.0.0</span>
            </div>
            <div class="controls">
                <theme-selector></theme-selector>
            </div>
        </header>
    `
};
