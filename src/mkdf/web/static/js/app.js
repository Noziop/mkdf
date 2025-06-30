const { createApp } = Vue

createApp({
    components: {
        'navbar': Navbar,
        'pattern-creator': PatternCreator,
        'template-creator': TemplateCreator,
        'docker-creator': DockerCreator,
        'history-section': HistorySection
    },
    data() {
        return {
            activeTab: 'pattern' // Default active tab
        };
    },
    template: `
        <navbar></navbar>
        <div class="page-container">
            <nav class="tabs">
                <div class="tab" :class="{ active: activeTab === 'pattern' }" @click="activeTab = 'pattern'">
                    <i class="fas fa-code-branch"></i> Pattern Creator
                </div>
                <div class="tab" :class="{ active: activeTab === 'templates' }" @click="activeTab = 'templates'">
                    <i class="fas fa-file-code"></i> Templates
                </div>
                <div class="tab" :class="{ active: activeTab === 'docker' }" @click="activeTab = 'docker'">
                    <i class="fab fa-docker"></i> Docker Combos
                </div>
                <div class="tab" :class="{ active: activeTab === 'history' }" @click="activeTab = 'history'">
                    <i class="fas fa-history"></i> History
                </div>
            </nav>
            <div class="content-area">
                <pattern-creator v-show="activeTab === 'pattern'"></pattern-creator>
                <template-creator v-show="activeTab === 'templates'"></template-creator>
                <docker-creator v-show="activeTab === 'docker'"></docker-creator>
                <history-section v-show="activeTab === 'history'"></history-section>
            </div>
        </div>
    `
}).mount('#app');