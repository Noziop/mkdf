#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <termios.h>
#include <ctype.h>
#include "../include/cli_handler.h"
#include "../include/directory_handler.h"

#define MAX_PATH_LEN 4096
#define MAX_INPUT_LEN 1024
#define MAX_MENU_ITEMS 20

// Codes ANSI pour coloration et déplacement du curseur
#define ANSI_COLOR_RESET    "\x1b[0m"
#define ANSI_COLOR_RED      "\x1b[31m"
#define ANSI_COLOR_GREEN    "\x1b[32m"
#define ANSI_COLOR_YELLOW   "\x1b[33m"
#define ANSI_COLOR_BLUE     "\x1b[34m"
#define ANSI_COLOR_MAGENTA  "\x1b[35m"
#define ANSI_COLOR_CYAN     "\x1b[36m"
#define ANSI_BOLD           "\x1b[1m"
#define ANSI_CLEAR_SCREEN   "\x1b[2J\x1b[H"
#define ANSI_CURSOR_UP      "\x1b[1A"
#define ANSI_CURSOR_DOWN    "\x1b[1B"
#define ANSI_SAVE_CURSOR    "\x1b[s"
#define ANSI_RESTORE_CURSOR "\x1b[u"
#define ANSI_ERASE_LINE     "\x1b[2K"

// Touches spéciales
#define KEY_ESC     27
#define KEY_ENTER   10
#define KEY_UP      65
#define KEY_DOWN    66
#define KEY_RIGHT   67
#define KEY_LEFT    68

// Structure pour les menus
typedef struct {
    char title[256];
    char items[MAX_MENU_ITEMS][256];
    int count;
    int selected;
} menu_t;

// Configuration du terminal pour la saisie non canonique (sans attendre Entrée)
static struct termios old_term, new_term;

static void enter_raw_mode() {
    tcgetattr(STDIN_FILENO, &old_term);
    new_term = old_term;
    
    // Désactiver le mode canonique et l'écho
    new_term.c_lflag &= ~(ICANON | ECHO);
    
    // Configurer le timeout de lecture
    new_term.c_cc[VMIN] = 1;
    new_term.c_cc[VTIME] = 0;
    
    tcsetattr(STDIN_FILENO, TCSANOW, &new_term);
}

static void exit_raw_mode() {
    tcsetattr(STDIN_FILENO, TCSANOW, &old_term);
}

// Lecture d'une touche avec interprétation des séquences d'échappement
static int read_key() {
    char buf[3];
    int n = read(STDIN_FILENO, buf, 1);
    
    if (n == 1) {
        if (buf[0] == KEY_ESC) {
            // Séquence d'échappement, lire deux caractères de plus
            if (read(STDIN_FILENO, buf + 1, 2) == 2) {
                if (buf[1] == '[') {
                    return buf[2];
                }
            }
            return KEY_ESC;
        } else {
            return buf[0];
        }
    }
    
    return -1;
}

// Initialiser un menu
static void init_menu(menu_t *menu, const char *title) {
    strncpy(menu->title, title, sizeof(menu->title) - 1);
    menu->count = 0;
    menu->selected = 0;
}

// Ajouter un élément au menu
static void add_menu_item(menu_t *menu, const char *item) {
    if (menu->count < MAX_MENU_ITEMS) {
        strncpy(menu->items[menu->count], item, sizeof(menu->items[0]) - 1);
        menu->count++;
    }
}

// Afficher un menu
static void display_menu(menu_t *menu) {
    printf("%s%s%s\n\n", ANSI_BOLD, menu->title, ANSI_COLOR_RESET);
    
    for (int i = 0; i < menu->count; i++) {
        if (i == menu->selected) {
            printf("%s> %s%s\n", ANSI_COLOR_GREEN, menu->items[i], ANSI_COLOR_RESET);
        } else {
            printf("  %s\n", menu->items[i]);
        }
    }
    
    printf("\nUtilisez les flèches ↑↓ pour naviguer, Entrée pour sélectionner, Échap pour quitter\n");
}

// Traiter l'interaction avec le menu
static int handle_menu(menu_t *menu) {
    enter_raw_mode();
    int running = 1;
    int result = -1;
    
    while (running) {
        printf(ANSI_CLEAR_SCREEN);
        display_menu(menu);
        
        int key = read_key();
        
        switch (key) {
            case KEY_UP:
                if (menu->selected > 0) {
                    menu->selected--;
                }
                break;
                
            case KEY_DOWN:
                if (menu->selected < menu->count - 1) {
                    menu->selected++;
                }
                break;
                
            case KEY_ENTER:
                result = menu->selected;
                running = 0;
                break;
                
            case KEY_ESC:
                running = 0;
                break;
        }
    }
    
    exit_raw_mode();
    return result;
}

// Demander une entrée à l'utilisateur (mode normal)
static void prompt_input(const char *prompt, char *input, size_t max_len) {
    printf("%s: ", prompt);
    fflush(stdout);
    
    // S'assurer que nous sommes en mode canonique pour la saisie
    exit_raw_mode();
    
    if (fgets(input, max_len, stdin) != NULL) {
        // Supprimer le saut de ligne final
        size_t len = strlen(input);
        if (len > 0 && input[len - 1] == '\n') {
            input[len - 1] = '\0';
        }
    } else {
        input[0] = '\0';
    }
}

// Afficher la structure de répertoires de manière récursive avec indentation
void print_directory_structure(const char *path, int level) {
    DIR *dir;
    struct dirent *entry;
    struct stat statbuf;
    char full_path[MAX_PATH_LEN];
    
    // Ouvrir le répertoire
    if ((dir = opendir(path)) == NULL) {
        perror("Erreur lors de l'ouverture du répertoire");
        return;
    }
    
    // Lire les entrées du répertoire
    while ((entry = readdir(dir)) != NULL) {
        // Ignorer "." et ".."
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }
        
        // Construire le chemin complet
        snprintf(full_path, MAX_PATH_LEN, "%s/%s", path, entry->d_name);
        
        // Obtenir les informations sur le fichier
        if (stat(full_path, &statbuf) == -1) {
            perror("stat");
            continue;
        }
        
        // Indenter selon le niveau
        for (int i = 0; i < level; i++) {
            printf("  ");
        }
        
        // Afficher en utilisant les couleurs selon le type
        if (S_ISDIR(statbuf.st_mode)) {
            printf("%s├── %s/%s\n", ANSI_COLOR_BLUE, entry->d_name, ANSI_COLOR_RESET);
            // Récursivement afficher le contenu du sous-répertoire
            print_directory_structure(full_path, level + 1);
        } else {
            // Pour un fichier normal
            printf("├── %s\n", entry->d_name);
        }
    }
    
    closedir(dir);
}

// Créer un projet simple (mono répertoire)
static int create_simple_project(const char *path) {
    char structure[MAX_PATH_LEN];
    snprintf(structure, sizeof(structure), "%s/{src/,docs/,README.md}", path);
    return create_directory_structure(structure);
}

// Créer un projet multi-répertoires
static int create_multi_project(const char *path) {
    char structure[MAX_PATH_LEN];
    snprintf(structure, sizeof(structure), 
             "%s/{src/{lib/,bin/,include/},docs/{user/,dev/},tests/,README.md,LICENSE}", 
             path);
    return create_directory_structure(structure);
}

// Créer un projet avec Docker
static int create_docker_project(const char *path) {
    char structure[MAX_PATH_LEN];
    snprintf(structure, sizeof(structure), 
             "%s/{src/,docker/{app/Dockerfile,nginx/Dockerfile,docker-compose.yml},README.md}", 
             path);
    
    // Créer la structure de base
    if (create_directory_structure(structure) != EXIT_SUCCESS) {
        return EXIT_FAILURE;
    }
    
    // Créer les fichiers Docker avec du contenu de base
    char docker_compose[MAX_PATH_LEN];
    snprintf(docker_compose, sizeof(docker_compose), "%s/docker/docker-compose.yml", path);
    
    FILE *file = fopen(docker_compose, "w");
    if (file) {
        fprintf(file, "version: '3'\n\nservices:\n");
        fprintf(file, "  app:\n");
        fprintf(file, "    build: ./app\n");
        fprintf(file, "    ports:\n");
        fprintf(file, "      - \"8000:8000\"\n");
        fprintf(file, "    volumes:\n");
        fprintf(file, "      - ../src:/app\n\n");
        fprintf(file, "  nginx:\n");
        fprintf(file, "    build: ./nginx\n");
        fprintf(file, "    ports:\n");
        fprintf(file, "      - \"80:80\"\n");
        fprintf(file, "    depends_on:\n");
        fprintf(file, "      - app\n");
        fclose(file);
    }
    
    char app_dockerfile[MAX_PATH_LEN];
    snprintf(app_dockerfile, sizeof(app_dockerfile), "%s/docker/app/Dockerfile", path);
    
    file = fopen(app_dockerfile, "w");
    if (file) {
        fprintf(file, "FROM python:3.10-slim\n\n");
        fprintf(file, "WORKDIR /app\n\n");
        fprintf(file, "COPY requirements.txt .\n");
        fprintf(file, "RUN pip install --no-cache-dir -r requirements.txt\n\n");
        fprintf(file, "CMD [\"python\", \"main.py\"]\n");
        fclose(file);
    }
    
    char nginx_dockerfile[MAX_PATH_LEN];
    snprintf(nginx_dockerfile, sizeof(nginx_dockerfile), "%s/docker/nginx/Dockerfile", path);
    
    file = fopen(nginx_dockerfile, "w");
    if (file) {
        fprintf(file, "FROM nginx:alpine\n\n");
        fprintf(file, "COPY nginx.conf /etc/nginx/conf.d/default.conf\n");
        fclose(file);
    }
    
    char nginx_conf[MAX_PATH_LEN];
    snprintf(nginx_conf, sizeof(nginx_conf), "%s/docker/nginx/nginx.conf", path);
    
    file = fopen(nginx_conf, "w");
    if (file) {
        fprintf(file, "server {\n");
        fprintf(file, "    listen 80;\n\n");
        fprintf(file, "    location / {\n");
        fprintf(file, "        proxy_pass http://app:8000;\n");
        fprintf(file, "        proxy_set_header Host $host;\n");
        fprintf(file, "        proxy_set_header X-Real-IP $remote_addr;\n");
        fprintf(file, "    }\n");
        fprintf(file, "}\n");
        fclose(file);
    }
    
    return EXIT_SUCCESS;
}

// Créer un projet FastAPI
static int create_fastapi_project(const char *path) {
    char structure[MAX_PATH_LEN];
    snprintf(structure, sizeof(structure), 
             "%s/{app/{api/{v1/endpoints/{users,items}.py,deps.py,__init__.py},core/{config.py,security.py,__init__.py},db/{models/,session.py,__init__.py},main.py,__init__.py},tests/,requirements.txt,README.md}", 
             path);
    
    // Créer la structure de base
    if (create_directory_structure(structure) != EXIT_SUCCESS) {
        return EXIT_FAILURE;
    }
    
    // Créer les fichiers spécifiques à FastAPI
    char main_py[MAX_PATH_LEN];
    snprintf(main_py, sizeof(main_py), "%s/app/main.py", path);
    
    FILE *file = fopen(main_py, "w");
    if (file) {
        fprintf(file, "from fastapi import FastAPI\n");
        fprintf(file, "from fastapi.middleware.cors import CORSMiddleware\n\n");
        fprintf(file, "from app.api.v1.endpoints import users, items\n\n");
        fprintf(file, "app = FastAPI(title=\"FastAPI Example\")\n\n");
        fprintf(file, "# CORS configuration\n");
        fprintf(file, "app.add_middleware(\n");
        fprintf(file, "    CORSMiddleware,\n");
        fprintf(file, "    allow_origins=[\"*\"],\n");
        fprintf(file, "    allow_credentials=True,\n");
        fprintf(file, "    allow_methods=[\"*\"],\n");
        fprintf(file, "    allow_headers=[\"*\"],\n");
        fprintf(file, ")\n\n");
        fprintf(file, "# Include routers\n");
        fprintf(file, "app.include_router(users.router, prefix=\"/api/v1\")\n");
        fprintf(file, "app.include_router(items.router, prefix=\"/api/v1\")\n\n");
        fprintf(file, "@app.get(\"/\")\n");
        fprintf(file, "async def root():\n");
        fprintf(file, "    return {\"message\": \"Welcome to FastAPI!\"}\n\n");
        fprintf(file, "if __name__ == \"__main__\":\n");
        fprintf(file, "    import uvicorn\n");
        fprintf(file, "    uvicorn.run(\"app.main:app\", host=\"0.0.0.0\", port=8000, reload=True)\n");
        fclose(file);
    }
    
    char users_py[MAX_PATH_LEN];
    snprintf(users_py, sizeof(users_py), "%s/app/api/v1/endpoints/users.py", path);
    
    file = fopen(users_py, "w");
    if (file) {
        fprintf(file, "from fastapi import APIRouter, HTTPException\n\n");
        fprintf(file, "router = APIRouter(tags=[\"users\"])\n\n");
        fprintf(file, "@router.get(\"/users/\")\n");
        fprintf(file, "async def read_users():\n");
        fprintf(file, "    return [{\"id\": 1, \"name\": \"John\"}, {\"id\": 2, \"name\": \"Jane\"}]\n\n");
        fprintf(file, "@router.get(\"/users/{user_id}\")\n");
        fprintf(file, "async def read_user(user_id: int):\n");
        fprintf(file, "    if user_id == 1:\n");
        fprintf(file, "        return {\"id\": 1, \"name\": \"John\"}\n");
        fprintf(file, "    elif user_id == 2:\n");
        fprintf(file, "        return {\"id\": 2, \"name\": \"Jane\"}\n");
        fprintf(file, "    raise HTTPException(status_code=404, detail=\"User not found\")\n");
        fclose(file);
    }
    
    char requirements_txt[MAX_PATH_LEN];
    snprintf(requirements_txt, sizeof(requirements_txt), "%s/requirements.txt", path);
    
    file = fopen(requirements_txt, "w");
    if (file) {
        fprintf(file, "fastapi>=0.68.0\n");
        fprintf(file, "uvicorn>=0.15.0\n");
        fprintf(file, "sqlalchemy>=1.4.23\n");
        fprintf(file, "pydantic>=1.8.2\n");
        fprintf(file, "python-jose>=3.3.0\n");
        fprintf(file, "passlib>=1.7.4\n");
        fprintf(file, "python-multipart>=0.0.5\n");
        fclose(file);
    }
    
    return EXIT_SUCCESS;
}

// Créer un projet Vue + Vite
static int create_vuevite_project(const char *path) {
    char structure[MAX_PATH_LEN];
    snprintf(structure, sizeof(structure), 
             "%s/{public/{favicon.ico,robots.txt},src/{assets/,components/{HelloWorld.vue},views/{HomeView.vue,AboutView.vue},App.vue,main.js,router.js},package.json,vite.config.js,README.md}", 
             path);
    
    // Créer la structure de base
    if (create_directory_structure(structure) != EXIT_SUCCESS) {
        return EXIT_FAILURE;
    }
    
    // Créer les fichiers spécifiques
    char main_js[MAX_PATH_LEN];
    snprintf(main_js, sizeof(main_js), "%s/src/main.js", path);
    
    FILE *file = fopen(main_js, "w");
    if (file) {
        fprintf(file, "import { createApp } from 'vue'\n");
        fprintf(file, "import App from './App.vue'\n");
        fprintf(file, "import router from './router.js'\n\n");
        fprintf(file, "const app = createApp(App)\n");
        fprintf(file, "app.use(router)\n");
        fprintf(file, "app.mount('#app')\n");
        fclose(file);
    }
    
    char app_vue[MAX_PATH_LEN];
    snprintf(app_vue, sizeof(app_vue), "%s/src/App.vue", path);
    
    file = fopen(app_vue, "w");
    if (file) {
        fprintf(file, "<template>\n");
        fprintf(file, "  <header>\n");
        fprintf(file, "    <nav>\n");
        fprintf(file, "      <router-link to=\"/\">Home</router-link> |\n");
        fprintf(file, "      <router-link to=\"/about\">About</router-link>\n");
        fprintf(file, "    </nav>\n");
        fprintf(file, "  </header>\n\n");
        fprintf(file, "  <router-view/>\n");
        fprintf(file, "</template>\n\n");
        fprintf(file, "<style>\n");
        fprintf(file, "#app {\n");
        fprintf(file, "  font-family: Avenir, Helvetica, Arial, sans-serif;\n");
        fprintf(file, "  -webkit-font-smoothing: antialiased;\n");
        fprintf(file, "  -moz-osx-font-smoothing: grayscale;\n");
        fprintf(file, "  text-align: center;\n");
        fprintf(file, "  color: #2c3e50;\n");
        fprintf(file, "  margin-top: 60px;\n");
        fprintf(file, "}\n");
        fprintf(file, "</style>\n");
        fclose(file);
    }
    
    char package_json[MAX_PATH_LEN];
    snprintf(package_json, sizeof(package_json), "%s/package.json", path);
    
    file = fopen(package_json, "w");
    if (file) {
        fprintf(file, "{\n");
        fprintf(file, "  \"name\": \"vue-vite-app\",\n");
        fprintf(file, "  \"version\": \"0.0.0\",\n");
        fprintf(file, "  \"scripts\": {\n");
        fprintf(file, "    \"dev\": \"vite\",\n");
        fprintf(file, "    \"build\": \"vite build\",\n");
        fprintf(file, "    \"preview\": \"vite preview\"\n");
        fprintf(file, "  },\n");
        fprintf(file, "  \"dependencies\": {\n");
        fprintf(file, "    \"vue\": \"^3.3.4\",\n");
        fprintf(file, "    \"vue-router\": \"^4.2.4\"\n");
        fprintf(file, "  },\n");
        fprintf(file, "  \"devDependencies\": {\n");
        fprintf(file, "    \"@vitejs/plugin-vue\": \"^4.2.3\",\n");
        fprintf(file, "    \"vite\": \"^4.4.8\"\n");
        fprintf(file, "  }\n");
        fprintf(file, "}\n");
        fclose(file);
    }
    
    char vite_config[MAX_PATH_LEN];
    snprintf(vite_config, sizeof(vite_config), "%s/vite.config.js", path);
    
    file = fopen(vite_config, "w");
    if (file) {
        fprintf(file, "import { defineConfig } from 'vite'\n");
        fprintf(file, "import vue from '@vitejs/plugin-vue'\n\n");
        fprintf(file, "export default defineConfig({\n");
        fprintf(file, "  plugins: [vue()],\n");
        fprintf(file, "})\n");
        fclose(file);
    }
    
    return EXIT_SUCCESS;
}

// Créer un projet React
static int create_react_project(const char *path) {
    char structure[MAX_PATH_LEN];
    snprintf(structure, sizeof(structure), 
             "%s/{public/{favicon.ico,robots.txt,index.html},src/{components/{App.js,Header.js,Footer.js},pages/{Home.js,About.js},assets/images/,styles/,App.css,index.css,index.js},package.json,.gitignore,README.md}", 
             path);
    
    // Créer la structure de base
    if (create_directory_structure(structure) != EXIT_SUCCESS) {
        return EXIT_FAILURE;
    }
    
    // Créer les fichiers spécifiques
    char package_json[MAX_PATH_LEN];
    snprintf(package_json, sizeof(package_json), "%s/package.json", path);
    
    FILE *file = fopen(package_json, "w");
    if (file) {
        fprintf(file, "{\n");
        fprintf(file, "  \"name\": \"react-app\",\n");
        fprintf(file, "  \"version\": \"0.1.0\",\n");
        fprintf(file, "  \"private\": true,\n");
        fprintf(file, "  \"dependencies\": {\n");
        fprintf(file, "    \"@testing-library/jest-dom\": \"^5.16.5\",\n");
        fprintf(file, "    \"@testing-library/react\": \"^13.4.0\",\n");
        fprintf(file, "    \"@testing-library/user-event\": \"^13.5.0\",\n");
        fprintf(file, "    \"react\": \"^18.2.0\",\n");
        fprintf(file, "    \"react-dom\": \"^18.2.0\",\n");
        fprintf(file, "    \"react-router-dom\": \"^6.11.2\",\n");
        fprintf(file, "    \"react-scripts\": \"5.0.1\",\n");
        fprintf(file, "    \"web-vitals\": \"^2.1.4\"\n");
        fprintf(file, "  },\n");
        fprintf(file, "  \"scripts\": {\n");
        fprintf(file, "    \"start\": \"react-scripts start\",\n");
        fprintf(file, "    \"build\": \"react-scripts build\",\n");
        fprintf(file, "    \"test\": \"react-scripts test\",\n");
        fprintf(file, "    \"eject\": \"react-scripts eject\"\n");
        fprintf(file, "  },\n");
        fprintf(file, "  \"eslintConfig\": {\n");
        fprintf(file, "    \"extends\": [\n");
        fprintf(file, "      \"react-app\",\n");
        fprintf(file, "      \"react-app/jest\"\n");
        fprintf(file, "    ]\n");
        fprintf(file, "  },\n");
        fprintf(file, "  \"browserslist\": {\n");
        fprintf(file, "    \"production\": [\n");
        fprintf(file, "      \">0.2%%\",\n");
        fprintf(file, "      \"not dead\",\n");
        fprintf(file, "      \"not op_mini all\"\n");
        fprintf(file, "    ],\n");
        fprintf(file, "    \"development\": [\n");
        fprintf(file, "      \"last 1 chrome version\",\n");
        fprintf(file, "      \"last 1 firefox version\",\n");
        fprintf(file, "      \"last 1 safari version\"\n");
        fprintf(file, "    ]\n");
        fprintf(file, "  }\n");
        fprintf(file, "}\n");
        fclose(file);
    }
    
    char index_js[MAX_PATH_LEN];
    snprintf(index_js, sizeof(index_js), "%s/src/index.js", path);
    
    file = fopen(index_js, "w");
    if (file) {
        fprintf(file, "import React from 'react';\n");
        fprintf(file, "import ReactDOM from 'react-dom/client';\n");
        fprintf(file, "import './index.css';\n");
        fprintf(file, "import App from './components/App';\n");
        fprintf(file, "import reportWebVitals from './reportWebVitals';\n\n");
        fprintf(file, "const root = ReactDOM.createRoot(document.getElementById('root'));\n");
        fprintf(file, "root.render(\n");
        fprintf(file, "  <React.StrictMode>\n");
        fprintf(file, "    <App />\n");
        fprintf(file, "  </React.StrictMode>\n");
        fprintf(file, ");\n\n");
        fprintf(file, "// If you want to start measuring performance in your app, pass a function\n");
        fprintf(file, "// to log results (for example: reportWebVitals(console.log))\n");
        fprintf(file, "// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals\n");
        fprintf(file, "reportWebVitals();\n");
        fclose(file);
    }
    
    char app_js[MAX_PATH_LEN];
    snprintf(app_js, sizeof(app_js), "%s/src/components/App.js", path);
    
    file = fopen(app_js, "w");
    if (file) {
        fprintf(file, "import React from 'react';\n");
        fprintf(file, "import '../App.css';\n");
        fprintf(file, "import Header from './Header';\n");
        fprintf(file, "import Footer from './Footer';\n\n");
        fprintf(file, "function App() {\n");
        fprintf(file, "  return (\n");
        fprintf(file, "    <div className=\"App\">\n");
        fprintf(file, "      <Header />\n");
        fprintf(file, "      <main className=\"App-content\">\n");
        fprintf(file, "        <h1>Welcome to React</h1>\n");
        fprintf(file, "        <p>Edit <code>src/components/App.js</code> and save to reload.</p>\n");
        fprintf(file, "      </main>\n");
        fprintf(file, "      <Footer />\n");
        fprintf(file, "    </div>\n");
        fprintf(file, "  );\n");
        fprintf(file, "}\n\n");
        fprintf(file, "export default App;\n");
        fclose(file);
    }
    
    return EXIT_SUCCESS;
}

// Créer un projet Flask
static int create_flask_project(const char *path) {
    char structure[MAX_PATH_LEN];
    snprintf(structure, sizeof(structure), 
             "%s/{app/{static/{css/,js/,images/},templates/{base.html,index.html,about.html},__init__.py,routes.py,models.py,forms.py},tests/,migrations/,config.py,requirements.txt,run.py,README.md}", 
             path);
    
    // Créer la structure de base
    if (create_directory_structure(structure) != EXIT_SUCCESS) {
        return EXIT_FAILURE;
    }
    
    // Créer les fichiers spécifiques
    char init_py[MAX_PATH_LEN];
    snprintf(init_py, sizeof(init_py), "%s/app/__init__.py", path);
    
    FILE *file = fopen(init_py, "w");
    if (file) {
        fprintf(file, "from flask import Flask\n");
        fprintf(file, "from config import Config\n\n");
        fprintf(file, "app = Flask(__name__)\n");
        fprintf(file, "app.config.from_object(Config)\n\n");
        fprintf(file, "from app import routes, models\n");
        fclose(file);
    }
    
    char routes_py[MAX_PATH_LEN];
    snprintf(routes_py, sizeof(routes_py), "%s/app/routes.py", path);
    
    file = fopen(routes_py, "w");
    if (file) {
        fprintf(file, "from flask import render_template\n");
        fprintf(file, "from app import app\n\n");
        fprintf(file, "@app.route('/')\n");
        fprintf(file, "@app.route('/index')\n");
        fprintf(file, "def index():\n");
        fprintf(file, "    return render_template('index.html', title='Home')\n\n");
        fprintf(file, "@app.route('/about')\n");
        fprintf(file, "def about():\n");
        fprintf(file, "    return render_template('about.html', title='About')\n");
        fclose(file);
    }
    
    char run_py[MAX_PATH_LEN];
    snprintf(run_py, sizeof(run_py), "%s/run.py", path);
    
    file = fopen(run_py, "w");
    if (file) {
        fprintf(file, "from app import app\n\n");
        fprintf(file, "if __name__ == '__main__':\n");
        fprintf(file, "    app.run(debug=True)\n");
        fclose(file);
    }
    
    char config_py[MAX_PATH_LEN];
    snprintf(config_py, sizeof(config_py), "%s/config.py", path);
    
    file = fopen(config_py, "w");
    if (file) {
        fprintf(file, "import os\n\n");
        fprintf(file, "class Config(object):\n");
        fprintf(file, "    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'\n");
        fprintf(file, "    # Database configuration\n");
        fprintf(file, "    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \\\n");
        fprintf(file, "        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')\n");
        fprintf(file, "    SQLALCHEMY_TRACK_MODIFICATIONS = False\n");
        fclose(file);
    }
    
    char requirements_txt[MAX_PATH_LEN];
    snprintf(requirements_txt, sizeof(requirements_txt), "%s/requirements.txt", path);
    
    file = fopen(requirements_txt, "w");
    if (file) {
        fprintf(file, "flask==2.2.3\n");
        fprintf(file, "flask-sqlalchemy==3.0.3\n");
        fprintf(file, "flask-migrate==4.0.4\n");
        fprintf(file, "flask-wtf==1.1.1\n");
        fprintf(file, "flask-login==0.6.2\n");
        fprintf(file, "email-validator==2.0.0\n");
        fprintf(file, "python-dotenv==1.0.0\n");
        fclose(file);
    }
    
    // Créer le template base.html
    char base_html[MAX_PATH_LEN];
    snprintf(base_html, sizeof(base_html), "%s/app/templates/base.html", path);
    
    file = fopen(base_html, "w");
    if (file) {
        // Utiliser fputs pour éviter les problèmes avec les templates Jinja2
        fputs("<!DOCTYPE html>\n", file);
        fputs("<html lang=\"en\">\n", file);
        fputs("<head>\n", file);
        fputs("    <meta charset=\"UTF-8\">\n", file);
        fputs("    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n", file);
        fputs("    <title>{% if title %}{{ title }} - Flask App{% else %}Welcome to Flask{% endif %}</title>\n", file);
        fputs("    <link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/style.css') }}\">\n", file);
        fputs("</head>\n", file);
        fputs("<body>\n", file);
        fputs("    <header>\n", file);
        fputs("        <nav>\n", file);
        fputs("            <a href=\"{{ url_for('index') }}\">Home</a>\n", file);
        fputs("            <a href=\"{{ url_for('about') }}\">About</a>\n", file);
        fputs("        </nav>\n", file);
        fputs("    </header>\n", file);
        fputs("    <main>\n", file);
        fputs("        {% block content %}{% endblock %}\n", file);
        fputs("    </main>\n", file);
        fputs("    <footer>\n", file);
        fputs("        <p>Flask App - © 2023</p>\n", file);
        fputs("    </footer>\n", file);
        fputs("</body>\n", file);
        fputs("</html>\n", file);
        fclose(file);
    }
    
    char index_html[MAX_PATH_LEN];
    snprintf(index_html, sizeof(index_html), "%s/app/templates/index.html", path);
    
    file = fopen(index_html, "w");
    if (file) {
        // Utiliser fputs pour éviter les problèmes avec les templates Jinja2
        fputs("{% extends \"base.html\" %}\n\n", file);
        fputs("{% block content %}\n", file);
        fputs("    <h1>Welcome to Flask!</h1>\n", file);
        fputs("    <p>This is a simple Flask application template.</p>\n", file);
        fputs("{% endblock %}\n", file);
        fclose(file);
    }
    
    char about_html[MAX_PATH_LEN];
    snprintf(about_html, sizeof(about_html), "%s/app/templates/about.html", path);
    
    file = fopen(about_html, "w");
    if (file) {
        // Utiliser fputs pour éviter les problèmes avec les templates Jinja2
        fputs("{% extends \"base.html\" %}\n\n", file);
        fputs("{% block content %}\n", file);
        fputs("    <h1>About This Application</h1>\n", file);
        fputs("    <p>This is a Flask application created with MKDF.</p>\n", file);
        fputs("    <p>MKDF is a directory and file structure generator for various project types.</p>\n", file);
        fputs("{% endblock %}\n", file);
        fclose(file);
    }
    
    // Créer un fichier CSS de base
    char css_file[MAX_PATH_LEN];
    snprintf(css_file, sizeof(css_file), "%s/app/static/css/style.css", path);
    
    file = fopen(css_file, "w");
    if (file) {
        fprintf(file, "body {\n");
        fprintf(file, "    font-family: Arial, sans-serif;\n");
        fprintf(file, "    margin: 0;\n");
        fprintf(file, "    padding: 0;\n");
        fprintf(file, "    line-height: 1.6;\n");
        fprintf(file, "}\n\n");
        fprintf(file, "header {\n");
        fprintf(file, "    background-color: #333;\n");
        fprintf(file, "    padding: 1rem;\n");
        fprintf(file, "}\n\n");
        fprintf(file, "header nav {\n");
        fprintf(file, "    display: flex;\n");
        fprintf(file, "    gap: 1rem;\n");
        fprintf(file, "}\n\n");
        fprintf(file, "header a {\n");
        fprintf(file, "    color: white;\n");
        fprintf(file, "    text-decoration: none;\n");
        fprintf(file, "}\n\n");
        fprintf(file, "header a:hover {\n");
        fprintf(file, "    text-decoration: underline;\n");
        fprintf(file, "}\n\n");
        fprintf(file, "main {\n");
        fprintf(file, "    padding: 2rem;\n");
        fprintf(file, "}\n\n");
        fprintf(file, "footer {\n");
        fprintf(file, "    background-color: #333;\n");
        fprintf(file, "    color: white;\n");
        fprintf(file, "    text-align: center;\n");
        fprintf(file, "    padding: 1rem;\n");
        fprintf(file, "    position: fixed;\n");
        fprintf(file, "    bottom: 0;\n");
        fprintf(file, "    width: 100%%;\n");
        fprintf(file, "}\n");
        fclose(file);
    }
    
    return EXIT_SUCCESS;
}

// Fonction générique pour créer un projet à partir d'un modèle
int create_project_from_template(project_template_t template_type, const char *project_path) {
    switch (template_type) {
        case PROJECT_SIMPLE:
            return create_simple_project(project_path);
        
        case PROJECT_MULTI:
            return create_multi_project(project_path);
        
        case PROJECT_DOCKER:
            return create_docker_project(project_path);
        
        case PROJECT_FASTAPI:
            return create_fastapi_project(project_path);
        
        case PROJECT_VUEVITE:
            return create_vuevite_project(project_path);
        
        case PROJECT_REACT:
            return create_react_project(project_path);
        
        case PROJECT_FLASK:
            return create_flask_project(project_path);
        
        // Autres modèles de projet...
        default:
            fprintf(stderr, "Type de projet non pris en charge\n");
            return EXIT_FAILURE;
    }
}

int start_cli_mode(void) {
    char current_dir[MAX_PATH_LEN];
    char project_name[MAX_INPUT_LEN];
    char target_dir[MAX_PATH_LEN];
    
    // Obtenir le répertoire courant
    if (getcwd(current_dir, sizeof(current_dir)) == NULL) {
        perror("Erreur lors de l'obtention du répertoire courant");
        return EXIT_FAILURE;
    }
    
    // Menu principal
    menu_t main_menu;
    init_menu(&main_menu, "MKDF - Créateur de Structures de Fichiers");
    add_menu_item(&main_menu, "Afficher l'arborescence du répertoire courant");
    add_menu_item(&main_menu, "Créer un nouveau projet");
    add_menu_item(&main_menu, "Changer de répertoire courant");
    add_menu_item(&main_menu, "Quitter");
    
    // Menu des modèles de projet
    menu_t template_menu;
    init_menu(&template_menu, "Sélectionner un type de projet");
    add_menu_item(&template_menu, "Projet simple (mono répertoire)");
    add_menu_item(&template_menu, "Projet multi-répertoires");
    add_menu_item(&template_menu, "Projet avec configuration Docker");
    add_menu_item(&template_menu, "Projet FastAPI");
    add_menu_item(&template_menu, "Projet Vue+Vite");
    add_menu_item(&template_menu, "Projet React");
    add_menu_item(&template_menu, "Projet Flask");
    add_menu_item(&template_menu, "Retour");
    
    int running = 1;
    
    while (running) {
        int choice = handle_menu(&main_menu);
        
        switch (choice) {
            case 0: // Afficher l'arborescence
                printf(ANSI_CLEAR_SCREEN);
                printf("%sArborescence du répertoire courant:%s\n\n", ANSI_BOLD, ANSI_COLOR_RESET);
                printf("%s\n", current_dir);
                print_directory_structure(current_dir, 0);
                printf("\nAppuyez sur Entrée pour continuer...");
                getchar();
                break;
                
            case 1: // Créer un nouveau projet
                {
                    int template_choice = handle_menu(&template_menu);
                    
                    // Only proceed if a template was actually selected (not back button or escape)
                    if (template_choice >= 0 && template_choice < 7) {
                        printf(ANSI_CLEAR_SCREEN);
                        
                        // Map menu choice to project template enum
                        project_template_t selected_template;
                        switch (template_choice) {
                            case 0: selected_template = PROJECT_SIMPLE; break;
                            case 1: selected_template = PROJECT_MULTI; break;
                            case 2: selected_template = PROJECT_DOCKER; break;
                            case 3: selected_template = PROJECT_FASTAPI; break;
                            case 4: selected_template = PROJECT_VUEVITE; break;
                            case 5: selected_template = PROJECT_REACT; break;
                            case 6: selected_template = PROJECT_FLASK; break;
                            default: selected_template = PROJECT_SIMPLE; break;
                        }
                        
                        // Demander si on souhaite utiliser un répertoire personnalisé
                        printf("Répertoire courant: %s\n\n", current_dir);
                        printf("Souhaitez-vous utiliser un répertoire différent? (O/n): ");
                        fflush(stdout);
                        
                        char choice[10];
                        if (fgets(choice, sizeof(choice), stdin) != NULL) {
                            if (choice[0] == 'O' || choice[0] == 'o' || choice[0] == 'Y' || choice[0] == 'y') {
                                prompt_input("Chemin du répertoire (absolu ou relatif)", target_dir, MAX_PATH_LEN);
                                
                                // Expand tilde if present
                                if (target_dir[0] == '~') {
                                    char expanded_path[MAX_PATH_LEN];
                                    if (expand_tilde(target_dir, expanded_path, sizeof(expanded_path)) == 0) {
                                        strncpy(target_dir, expanded_path, MAX_PATH_LEN - 1);
                                    } else {
                                        fprintf(stderr, "Impossible d'expandre le chemin avec tilde: %s\n", target_dir);
                                    }
                                }
                                
                                // Si chemin relatif, le compléter à partir du répertoire courant
                                if (target_dir[0] != '/') {
                                    char temp[MAX_PATH_LEN];
                                    snprintf(temp, sizeof(temp), "%s/%s", current_dir, target_dir);
                                    strncpy(target_dir, temp, MAX_PATH_LEN - 1);
                                }
                                
                                // Vérifier si le répertoire existe
                                struct stat st;
                                if (stat(target_dir, &st) != 0 || !S_ISDIR(st.st_mode)) {
                                    printf("%sLe répertoire n'existe pas. Voulez-vous le créer? (O/n): %s", ANSI_COLOR_YELLOW, ANSI_COLOR_RESET);
                                    fflush(stdout);
                                    
                                    if (fgets(choice, sizeof(choice), stdin) != NULL) {
                                        if (choice[0] == 'O' || choice[0] == 'o' || choice[0] == 'Y' || choice[0] == 'y') {
                                            // Créer le répertoire
                                            if (create_directory_recursive(target_dir) != 0) {
                                                printf("%sErreur lors de la création du répertoire. Utilisation du répertoire courant.%s\n", 
                                                       ANSI_COLOR_RED, ANSI_COLOR_RESET);
                                                strncpy(target_dir, current_dir, MAX_PATH_LEN - 1);
                                            } else {
                                                printf("%sRépertoire créé avec succès.%s\n", ANSI_COLOR_GREEN, ANSI_COLOR_RESET);
                                            }
                                        } else {
                                            // Utiliser le répertoire courant
                                            strncpy(target_dir, current_dir, MAX_PATH_LEN - 1);
                                        }
                                    }
                                }
                            } else {
                                // Utiliser le répertoire courant
                                strncpy(target_dir, current_dir, MAX_PATH_LEN - 1);
                            }
                        }
                        
                        // Demander le nom du projet
                        prompt_input("Nom du projet", project_name, MAX_INPUT_LEN);
                        
                        if (strlen(project_name) > 0) {
                            char project_path[MAX_PATH_LEN];
                            
                            // Construire le chemin complet du projet
                            snprintf(project_path, sizeof(project_path), "%s/%s", target_dir, project_name);
                            
                            printf("Création du projet '%s' dans '%s'...\n", project_name, project_path);
                            
                            if (create_project_from_template(selected_template, project_path) == EXIT_SUCCESS) {
                                printf("%sProjet créé avec succès!%s\n", ANSI_COLOR_GREEN, ANSI_COLOR_RESET);
                            } else {
                                printf("%sÉchec de la création du projet.%s\n", ANSI_COLOR_RED, ANSI_COLOR_RESET);
                            }
                            
                            printf("\nAppuyez sur Entrée pour continuer...");
                            getchar();
                        }
                    }
                }
                break;
                
            case 2: // Changer de répertoire courant
                {
                    printf(ANSI_CLEAR_SCREEN);
                    printf("Répertoire courant: %s\n\n", current_dir);
                    prompt_input("Nouveau répertoire (absolu ou relatif)", target_dir, MAX_PATH_LEN);
                    
                    // Expand tilde if present
                    if (target_dir[0] == '~') {
                        char expanded_path[MAX_PATH_LEN];
                        if (expand_tilde(target_dir, expanded_path, sizeof(expanded_path)) == 0) {
                            strncpy(target_dir, expanded_path, MAX_PATH_LEN - 1);
                        } else {
                            fprintf(stderr, "Impossible d'expandre le chemin avec tilde: %s\n", target_dir);
                        }
                    }
                    
                    // Si chemin relatif, le compléter à partir du répertoire courant
                    if (target_dir[0] != '/' && target_dir[0] != '\0') {
                        char temp[MAX_PATH_LEN];
                        snprintf(temp, sizeof(temp), "%s/%s", current_dir, target_dir);
                        strncpy(target_dir, temp, MAX_PATH_LEN - 1);
                    }
                    
                    // Si rien n'est entré, garder le répertoire courant
                    if (target_dir[0] == '\0') {
                        printf("Répertoire inchangé.\n");
                    } else {
                        // Vérifier si le répertoire existe
                        struct stat st;
                        if (stat(target_dir, &st) == 0 && S_ISDIR(st.st_mode)) {
                            // Changer de répertoire
                            if (chdir(target_dir) == 0) {
                                if (getcwd(current_dir, sizeof(current_dir)) == NULL) {
                                    perror("Erreur lors de l'obtention du répertoire courant");
                                } else {
                                    printf("%sRépertoire courant changé : %s%s\n", 
                                           ANSI_COLOR_GREEN, current_dir, ANSI_COLOR_RESET);
                                }
                            } else {
                                perror("Erreur lors du changement de répertoire");
                            }
                        } else {
                            printf("%sLe répertoire n'existe pas. Voulez-vous le créer? (O/n): %s", ANSI_COLOR_YELLOW, ANSI_COLOR_RESET);
                            fflush(stdout);
                            
                            char choice[10];
                            if (fgets(choice, sizeof(choice), stdin) != NULL) {
                                if (choice[0] == 'O' || choice[0] == 'o' || choice[0] == 'Y' || choice[0] == 'y') {
                                    // Créer le répertoire
                                    if (create_directory_recursive(target_dir) != 0) {
                                        printf("%sErreur lors de la création du répertoire.%s\n", 
                                               ANSI_COLOR_RED, ANSI_COLOR_RESET);
                                    } else {
                                        printf("%sRépertoire créé avec succès.%s\n", ANSI_COLOR_GREEN, ANSI_COLOR_RESET);
                                        
                                        // Changer de répertoire
                                        if (chdir(target_dir) == 0) {
                                            if (getcwd(current_dir, sizeof(current_dir)) == NULL) {
                                                perror("Erreur lors de l'obtention du répertoire courant");
                                            } else {
                                                printf("%sRépertoire courant changé : %s%s\n", 
                                                       ANSI_COLOR_GREEN, current_dir, ANSI_COLOR_RESET);
                                            }
                                        } else {
                                            perror("Erreur lors du changement de répertoire");
                                        }
                                    }
                                }
                            }
                        }
                    }
                    
                    printf("\nAppuyez sur Entrée pour continuer...");
                    getchar();
                }
                break;
                
            case 3: // Quitter
            case -1: // Échap
                running = 0;
                break;
        }
    }
    
    return EXIT_SUCCESS;
}

#include "../include/web_handler.h"

/**
 * Arrête le serveur web en cours d'exécution
 * 
 * @return EXIT_SUCCESS si le serveur a été arrêté, EXIT_FAILURE sinon
 */
int stop_server(void) {
    extern int stop_web_interface(void);
    return stop_web_interface();
}

/**
 * Analyse les arguments de la ligne de commande et exécute les commandes correspondantes
 */
int handle_cli_args(int argc, char *argv[]) {
    // Variables pour stocker les options
    int verbose = 0;
    int quiet = 0;
    int simulate = 0;
    int force = 0;
    int port = 8080; // Port par défaut
    int port_specified = 0; // Indicateur si l'option port a été spécifiée
    
    // Si aucun argument n'est fourni, lancer le mode interactif
    if (argc == 1) {
        return start_cli_mode();
    }

    // Traitement des options
    for (int i = 1; i < argc; i++) {
        // Option d'aide
        if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {
            show_help();
            return EXIT_SUCCESS;
        }
        // Option de version
        else if (strcmp(argv[i], "--version") == 0) {
            printf("mkdf version 1.0.0\n");
            return EXIT_SUCCESS;
        }
        // Option mode verbeux
        else if (strcmp(argv[i], "--verbose") == 0 || strcmp(argv[i], "-v") == 0) {
            verbose = 1;
            printf("Mode verbeux activé\n");
        }
        // Option mode silencieux
        else if (strcmp(argv[i], "--quiet") == 0 || strcmp(argv[i], "-q") == 0) {
            quiet = 1;
            // Ne rien afficher en mode silencieux
        }
        // Option mode simulation
        else if (strcmp(argv[i], "--simulate") == 0 || strcmp(argv[i], "-s") == 0) {
            simulate = 1;
            if (!quiet) printf("Mode simulation activé. Aucune modification ne sera effectuée.\n");
        }
        // Option mode force
        else if (strcmp(argv[i], "--force") == 0 || strcmp(argv[i], "-f") == 0) {
            force = 1;
            if (!quiet && verbose) printf("Mode force activé. La création sera forcée même si les répertoires existent déjà.\n");
        }
        // Option mode interactif
        else if (strcmp(argv[i], "--interactive") == 0 || strcmp(argv[i], "-i") == 0) {
            if (!quiet) printf("Lancement du mode interactif...\n");
            return start_cli_mode();
        }
        // Option pour créer un projet
        else if (strcmp(argv[i], "--create") == 0 || strcmp(argv[i], "-c") == 0) {
            // Vérifier qu'il y a un argument après --create
            if (i + 1 < argc) {
                const char *project_path = argv[i + 1];
                i++; // Sauter l'argument du chemin
                
                // Vérifier s'il y a un type spécifié
                project_template_t template_type = PROJECT_SIMPLE; // Type par défaut
                if (i + 1 < argc && argv[i + 1][0] != '-') {
                    const char *type_str = argv[i + 1];
                    i++; // Sauter l'argument du type
                    
                    // Déterminer le type de projet
                    if (strcmp(type_str, "multi") == 0) {
                        template_type = PROJECT_MULTI;
                    } else if (strcmp(type_str, "docker") == 0) {
                        template_type = PROJECT_DOCKER;
                    } else if (strcmp(type_str, "fastapi") == 0) {
                        template_type = PROJECT_FASTAPI;
                    } else if (strcmp(type_str, "vuevite") == 0) {
                        template_type = PROJECT_VUEVITE;
                    } else if (strcmp(type_str, "react") == 0) {
                        template_type = PROJECT_REACT;
                    } else if (strcmp(type_str, "flask") == 0) {
                        template_type = PROJECT_FLASK;
                    } else if (strcmp(type_str, "nodejs") == 0) {
                        template_type = PROJECT_NODEJS;
                    } else if (strcmp(type_str, "nextjs") == 0) {
                        template_type = PROJECT_NEXTJS;
                    } else if (strcmp(type_str, "nuxtjs") == 0) {
                        template_type = PROJECT_NUXTJS;
                    } else {
                        if (!quiet) printf("Type de projet non reconnu : %s\n", type_str);
                        show_help();
                        return EXIT_FAILURE;
                    }
                }
                
                // En mode simulation, ne pas créer réellement le projet
                if (simulate) {
                    if (!quiet) printf("Simulation: création d'un projet de type %d à l'emplacement %s\n", template_type, project_path);
                    return EXIT_SUCCESS;
                }
                
                // Définir les options pour la création
                set_force_mode(force);
                set_verbose_mode(verbose);
                set_quiet_mode(quiet);
                
                return create_project_from_template(template_type, project_path);
            } else {
                if (!quiet) printf("Erreur : chemin du projet manquant après l'option --create\n");
                return EXIT_FAILURE;
            }
        }
        // Option pour afficher la structure d'un répertoire
        else if (strcmp(argv[i], "--tree") == 0 || strcmp(argv[i], "-t") == 0) {
            const char *path = ".";
            if (i + 1 < argc && argv[i + 1][0] != '-') {
                path = argv[i + 1];
                i++; // Sauter l'argument du chemin
            }
            print_directory_structure(path, 0);
            return EXIT_SUCCESS;
        }
        // Option pour démarrer l'interface web
        else if (strcmp(argv[i], "--web") == 0 || strcmp(argv[i], "-w") == 0) {
            // Vérifier si le port est spécifié
            if (i + 1 < argc && (strcmp(argv[i + 1], "--port") == 0 || strcmp(argv[i + 1], "-p") == 0)) {
                i++; // Sauter l'option --port
                if (i + 1 < argc) {
                    port = atoi(argv[i + 1]);
                    i++; // Sauter la valeur du port
                    port_specified = 1;
                }
            } else if (i + 1 < argc && strncmp(argv[i + 1], "--port=", 7) == 0) {
                port = atoi(argv[i + 1] + 7);
                i++; // Sauter l'argument du port
                port_specified = 1;
            } else if (i + 1 < argc && strncmp(argv[i + 1], "-p=", 3) == 0) {
                port = atoi(argv[i + 1] + 3);
                i++; // Sauter l'argument du port
                port_specified = 1;
            }
            
            if (!quiet) printf("Démarrage de l'interface web sur le port %d...\n", port);
            return start_web_interface_with_port(port);
        }
        // Option spécifique pour le port
        else if (strcmp(argv[i], "--port") == 0 || strcmp(argv[i], "-p") == 0) {
            if (i + 1 < argc) {
                port = atoi(argv[i + 1]);
                i++; // Sauter la valeur du port
                port_specified = 1;
                if (!quiet && verbose) printf("Port défini: %d\n", port);
            }
            if (port_specified && !quiet) {
                printf("L'option -p/--port doit être utilisée avec -w/--web pour démarrer l'interface web sur un port spécifique.\n");
                printf("Exemple d'utilisation: mkdf -w -p %d\n", port);
            }
        }
        // Option pour arrêter le serveur web
        else if (strcmp(argv[i], "--stop") == 0) {
            return stop_server();
        }
        // Si c'est une expression de structure de répertoires
        else {
            const char *expression = argv[i];
            
            // Mode simulation
            if (simulate) {
                if (!quiet) printf("Simulation: création de la structure '%s'\n", expression);
                return EXIT_SUCCESS;
            }
            
            // Définir les options
            set_force_mode(force);
            set_verbose_mode(verbose);
            set_quiet_mode(quiet);
            
            // Créer la structure
            return create_directory_structure(expression);
        }
    }

    // Si l'option -p a été spécifiée sans -w, afficher un message d'aide
    if (port_specified && !quiet) {
        printf("L'option -p/--port doit être utilisée avec -w/--web pour démarrer l'interface web sur un port spécifique.\n");
        printf("Exemple d'utilisation: mkdf -w -p %d\n", port);
    }

    return EXIT_SUCCESS;
}

/**
 * Affiche la liste des commandes disponibles
 */
void show_help(void) {
    printf("mkdf - Outil de création de structure de projets\n\n");
    printf("Usage:\n");
    printf("  mkdf [options]\n\n");
    printf("Options:\n");
    printf("  -h, --help                 Affiche cette aide\n");
    printf("  -v, --version              Affiche la version\n");
    printf("  -c, --create <path> [type] Crée un nouveau projet à l'emplacement spécifié\n");
    printf("  -t, --tree [path]          Affiche la structure d'un répertoire\n");
    printf("  -w, --web                  Démarre l'interface web sur http://localhost:8080\n");
    printf("  -s, --stop                 Arrête le serveur web s'il est en cours d'exécution\n\n");
    printf("Types de projets disponibles:\n");
    printf("  simple   Structure de projet simple (par défaut)\n");
    printf("  multi    Structure de projet multi-répertoires\n");
    printf("  docker   Projet avec configuration Docker\n");
    printf("  fastapi  Projet FastAPI (Python)\n");
    printf("  vuevite  Projet Vue.js + Vite\n");
    printf("  react    Projet React\n");
    printf("  flask    Projet Flask (Python)\n");
    printf("  nodejs   Projet Node.js\n");
    printf("  nextjs   Projet Next.js\n");
    printf("  nuxtjs   Projet Nuxt.js\n");
}

static int handle_directory_change(char *current_dir, size_t current_dir_size __attribute__((unused)), char *target_dir, size_t target_dir_size) {
    // Expand tilde if present
    if (target_dir[0] == '~') {
        char expanded_path[MAX_PATH_LEN];
        if (expand_tilde(target_dir, expanded_path, sizeof(expanded_path)) == 0) {
            strncpy(target_dir, expanded_path, target_dir_size - 1);
            target_dir[target_dir_size - 1] = '\0';
        } else {
            fprintf(stderr, "Impossible d'expandre le chemin avec tilde: %s\n", target_dir);
        }
    }
    
    // Si chemin relatif, le compléter à partir du répertoire courant
    if (target_dir[0] != '/' && target_dir[0] != '\0') {
        char temp[MAX_PATH_LEN];
        size_t current_len = strlen(current_dir);
        size_t target_len = strlen(target_dir);
        
        // Vérifier que la longueur totale ne dépasse pas MAX_PATH_LEN-2 (pour le / et le \0)
        if (current_len + target_len + 1 >= MAX_PATH_LEN) {
            fprintf(stderr, "Chemin trop long: %s/%s\n", current_dir, target_dir);
            return -1;
        }
        
        // Construire le chemin complet de manière sécurisée
        strcpy(temp, current_dir);
        strcat(temp, "/");
        strcat(temp, target_dir);
        
        strncpy(target_dir, temp, target_dir_size - 1);
        target_dir[target_dir_size - 1] = '\0';
    }
    
    return 0;
}