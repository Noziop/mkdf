def get_react_template():    return {        'package.json': '''{
  "name": "react-app",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.17.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}''',
        'public/index.html': '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>React App</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>''',
        'src/index.js': '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
''',
        'src/App.js': '''import React from 'react';

function App() {
  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>Hello React!</h1>
      <p>Your React app is running successfully.</p>
    </div>
  );
}

export default App;
'''
    }


def get_vue_template():
    return {
        'package.json': '''{
  "name": "vue-app",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.3.4"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.4.0",
    "vite": "^4.4.5"
  }
}''',
        'vite.config.js': '''import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 3000
  }
})
''',
        'index.html': '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vue App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>''',
        'src/main.js': '''import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'

const routes = [
  { path: '/', component: Home }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

createApp(App).use(router).mount('#app')
''',
        'src/App.vue': '''<template>
  <div id="app">
    <nav class="navbar">
      <h1>{{ appName }}</h1>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      appName: 'Fullstack App'
    }
  }
}
</script>

<style>
.navbar {
  background: #2c3e50;
  color: white;
  padding: 1rem;
}
</style>
''',
        'src/views/Home.vue': '''<template>
  <div style="padding: 20px; text-align: center;">
    <h1>Hello Vue!</h1>
    <p>Your Vue app is running successfully.</p>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>
'''
    }


def get_flask_template():
    return {
        'app.py': '''from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return jsonify({"message": "Hello Flask!"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
''',
        'requirements.txt': '''Flask==3.0.0
Flask-CORS==4.0.0
python-dotenv==1.0.0
''',
        '.env': 'FLASK_ENV=development\nFLASK_DEBUG=true'
    }


def get_fastapi_template():
    return {
        'main.py': '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI App", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello FastAPI!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
''',
        'requirements.txt': '''fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-decouple==3.8
''',
        '.env': '''DATABASE_URL=postgresql://user:password@db:5432/dbname
SECRET_KEY=your-secret-key-here
DEBUG=true
'''
    }


def get_express_template():
    return {
        'server.js': '''const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
    res.json({ message: 'Hello Express!' });
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
''',
        'package.json': '''{
  "name": "express-app",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  }
}''',
        '.env': 'PORT=3000\nNODE_ENV=development'
    }


def get_laravel_template():
    return {
        'public/index.php': '''<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});
''',
        'app/Http/Controllers/ExampleController.php': '''<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ExampleController extends Controller
{
    public function index()
    {
        return response()->json(['message' => 'Hello Laravel!']);
    }
}
''',
        'routes/web.php': '''<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});
''',
        'routes/api.php': '''<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
''',
        'config/app.php': '''<?php

return [
    'name' => env('APP_NAME', 'Laravel'),
    'env' => env('APP_ENV', 'production'),
    'debug' => (bool) env('APP_DEBUG', false),
    'url' => env('APP_URL', 'http://localhost'),
    'timezone' => 'UTC',
    'locale' => 'en',
    'fallback_locale' => 'en',
    'key' => env('APP_KEY'),
    'cipher' => 'AES-256-CBC',
    'providers' => [
        // Laravel Framework Service Providers...
        Illuminate\\Auth\\AuthServiceProvider::class,
        Illuminate\\Broadcasting\\BroadcastServiceProvider::class,
        Illuminate\\Bus\\BusServiceProvider::class,
        Illuminate\\Cache\\CacheServiceProvider::class,
        Illuminate\\Foundation\\Providers\\ConsoleSupportServiceProvider::class,
        Illuminate\\Routing\\ControllerServiceProvider::class,
        Illuminate\\Cookie\\CookieServiceProvider::class,
        Illuminate\\Database\\DatabaseServiceProvider::class,
        Illuminate\\Encryption\\EncryptionServiceProvider::class,
        Illuminate\\Filesystem\\FilesystemServiceProvider::class,
        Illuminate\\Foundation\\Providers\\FoundationServiceProvider::class,
        Illuminate\\Hashing\\HashServiceProvider::class,
        Illuminate\\Mail\\MailServiceProvider::class,
        Illuminate\\Notifications\\NotificationServiceProvider::class,
        Illuminate\\Pagination\\PaginationServiceProvider::class,
        Illuminate\\Pipeline\\PipelineServiceProvider::class,
        Illuminate\\Queue\\QueueServiceProvider::class,
        Illuminate\\Redis\\RedisServiceProvider::class,
        Illuminate\\Auth\\Passwords\\PasswordResetServiceProvider::class,
        Illuminate\\Session\\SessionServiceProvider::class,
        Illuminate\\Translation\\TranslationServiceProvider::class,
        Illuminate\\Validation\\ValidationServiceProvider::class,
        Illuminate\\View\\ViewServiceProvider::class,

        // Package Service Providers...

        // Application Service Providers...
        App\\Providers\\AppServiceProvider::class,
        App\\Providers\\AuthServiceProvider::class,
        // App\\Providers\\BroadcastServiceProvider::class,
        App\\Providers\\EventServiceProvider::class,
        App\\Providers\\RouteServiceProvider::class,

    ],
    'aliases' => [
        'App' => Illuminate\\Support\\Facades\\App::class,
        'Arr' => Illuminate\\Support\\Arr::class,
        'Artisan' => Illuminate\\Support\\Facades\\Artisan::class,
        'Auth' => Illuminate\\Support\\Facades\\Auth::class,
        'Blade' => Illuminate\\Support\\Facades\\Blade::class,
        'Bus' => Illuminate\\Support\\Facades\\Bus::class,
        'Cache' => Illuminate\\Support\\Facades\\Cache::class,
        'Config' => Illuminate\\Support\\Facades\\Config::class,
        'Cookie' => Illuminate\\Support\\Facades\\Cookie::class,
        'Crypt' => Illuminate\\Support\\Facades\\Crypt::class,
        'DB' => Illuminate\\Support\\Facades\\DB::class,
        'Eloquent' => Illuminate\\Database\\Eloquent\\Model::class,
        'Event' => Illuminate\\Support\\Facades\\Event::class,
        'File' => Illuminate\\Support\\Facades\\File::class,
        'Gate' => Illuminate\\Support\\Facades\\Gate::class,
        'Hash' => Illuminate\\Support\\Facades\\Hash::class,
        'Lang' => Illuminate\\Support\\Facades\\Lang::class,
        'Log' => Illuminate\\Support\\Facades\\Log::class,
        'Mail' => Illuminate\\Support\\Facades\\Mail::class,
        'Notification' => Illuminate\\Support\\Facades\\Notification::class,
        'Password' => Illuminate\\Support\\Facades\\Password::class,
        'Queue' => Illuminate\\Support\\Facades\\Queue::class,
        'Redirect' => Illuminate\\Support\\Facades\\Redirect::class,
        'Redis' => Illuminate\\Support\\Facades\\Redis::class,
        'Request' => Illuminate\\Support\\Facades\\Request::class,
        'Response' => Illuminate\\Support\\Facades\\Response::class,
        'Route' => Illuminate\\Support\\Facades\\Route::class,
        'Schema' => Illuminate\\Support\\Facades\\Schema::class,
        'Session' => Illuminate\\Support\\Facades\\Session::class,
        'Storage' => Illuminate\\Support\\Facades\\Storage::class,
        'Str' => Illuminate\\Support\\Str::class,
        'URL' => Illuminate\\Support\\Facades\\URL::class,
        'Validator' => Illuminate\\Support\\Facades\\Validator::class,
        'View' => Illuminate\\Support\\Facades\\View::class,
    ],
];
''',
        '.env': '''APP_NAME="Laravel"
APP_ENV=local
APP_KEY=base64:YOUR_APP_KEY_HERE
APP_DEBUG=true
APP_URL=http://localhost

LOG_CHANNEL=stack
LOG_LEVEL=debug

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=

BROADCAST_DRIVER=log
CACHE_DRIVER=file
FILESYSTEM_DISK=local
QUEUE_CONNECTION=sync
SESSION_DRIVER=file
SESSION_LIFETIME=120

MEMCACHED_HOST=127.0.0.1

REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

MAIL_MAILER=smtp
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
MAIL_FROM_ADDRESS="hello@example.com"
MAIL_FROM_NAME="${APP_NAME}"

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=
AWS_USE_PATH_STYLE_ENDPOINT=false

PUSHER_APP_ID=
PUSHER_APP_KEY=
PUSHER_APP_SECRET=
PUSHER_APP_CLUSTER=mt1

VITE_APP_NAME="${APP_NAME}"
'''
    }


def get_slim_template():
    return {
        'public/index.php': '''<?php
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use Slim\Factory\AppFactory;

require __DIR__ . '/../vendor/autoload.php';

$app = AppFactory::create();

$app->get('/', function (Request $request, Response $response, array $args) {
    $response->getBody()->write("Hello Slim!");
    return $response;
});

$app->run();
''',
        'composer.json': '''{
    "name": "slim/app",
    "description": "A Slim Framework application skeleton",
    "type": "project",
    "license": "MIT",
    "require": {
        "php": "^7.4 || ^8.0",
        "slim/slim": "^4.0",
        "slim/psr7": "^1.0",
        "nyholm/psr7": "^1.0",
        "nyholm/psr7-server": "^1.0",
        "guzzlehttp/psr7": "^2.0",
        "laminas/laminas-httphandlerrunner": "^1.0"
    },
    "autoload": {
        "psr-4": {
            "App\\": "app/"
        }
    },
    "scripts": {
        "start": "php -S 0.0.0.0:8080 -t public",
        "test": "phpunit"
    }
}''',
        'src/routes.php': '''<?php
use Slim\App;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;

return function (App $app) {
    $app->get('/hello/{name}', function (Request $request, Response $response, array $args) {
        $name = $args['name'];
        $response->getBody()->write("Hello, $name");
        return $response;
    });
};
'''
    }


def get_nextjs_template():
    return {
        'package.json': '''{
  "name": "nextjs-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}''',
        'pages/index.js': '''import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>Create Next App</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <a href="https://nextjs.org">Next.js!</a>
        </h1>

        <p className={styles.description}>
          Get started by editing{' '}
          <code className={styles.code}>pages/index.js</code>
        </p>
      </main>
    </div>
  )
}
''',
        'styles/Home.module.css': '''.container {
  min-height: 100vh;
  padding: 0 0.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.main {
  padding: 5rem 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.title a {
  color: #0070f3;
  text-decoration: none;
}

.title a:hover,
.title a:focus,
.title a:active {
  text-decoration: underline;
}

.title {
  margin: 0;
  line-height: 1.15;
  font-size: 4rem;
}

.title,
.description {
  text-align: center;
}

.description {
  margin: 4rem 0;
  line-height: 1.5;
  font-size: 1.5rem;
}

.code {
  background: #fafafa;
  border-radius: 5px;
  padding: 0.75rem;
  font-size: 1.1rem;
  font-family: Menlo, Monaco, Lucida Console, Liberation Mono, DejaVu Sans Mono, Bitstream Vera Sans Mono, Courier New, monospace;
}
'''
    }


def get_nuxtjs_template():
    return {
        'package.json': '''{
  "name": "nuxt-app",
  "private": true,
  "scripts": {
    "build": "nuxt build",
    "dev": "nuxt dev",
    "generate": "nuxt generate",
    "preview": "nuxt preview"
  },
  "devDependencies": {
    "nuxt": "^3.0.0"
  }
}''',
        'app.vue': '''<template>
  <div>
    <NuxtWelcome />
  </div>
</template>
''',
        'nuxt.config.ts': '''// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: {
    enabled: true
  }
})
'''
    }


def get_angular_template():
    return {
        'package.json': '''{
  "name": "angular-app",
  "version": "0.0.0",
  "scripts": {
    "ng": "ng",
    "start": "ng serve",
    "build": "ng build",
    "watch": "ng build --watch --configuration development",
    "test": "ng test"
  },
  "private": true,
  "dependencies": {
    "@angular/animations": "^17.0.0",
    "@angular/common": "^17.0.0",
    "@angular/compiler": "^17.0.0",
    "@angular/core": "^17.0.0",
    "@angular/forms": "^17.0.0",
    "@angular/platform-browser": "^17.0.0",
    "@angular/platform-browser-dynamic": "^17.0.0",
    "@angular/router": "^17.0.0",
    "rxjs": "~7.8.0",
    "tslib": "^2.3.0",
    "zone.js": "~0.14.0"
  },
  "devDependencies": {
    "@angular-devkit/build-angular": "^17.0.0",
    "@angular/cli": "^17.0.0",
    "@angular/compiler-cli": "^17.0.0",
    "@types/jasmine": "~5.1.0",
    "jasmine-core": "~5.1.0",
    "karma": "~6.4.0",
    "karma-chrome-launcher": "~3.2.0",
    "karma-coverage": "~2.2.0",
    "karma-jasmine": "~5.1.0",
    "karma-jasmine-html-reporter": "~2.1.0",
    "typescript": "~5.2.2"
  }
}''',
        'angular.json': '''{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "newProjectRoot": "projects",
  "projects": {
    "angular-app": {
      "projectType": "application",
      "schematics": {},
      "root": "",
      "sourceRoot": "src",
      "prefix": "app",
      "architect": {
        "build": {
          "builder": "@angular-devkit/build-angular:browser",
          "options": {
            "outputPath": "dist/angular-app",
            "index": "src/index.html",
            "main": "src/main.ts",
            "polyfills": [
              "zone.js"
            ],
            "tsConfig": "tsconfig.app.json",
            "assets": [
              "src/favicon.ico",
              "src/assets"
            ],
            "styles": [
              "src/styles.css"
            ],
            "scripts": []
          },
          "configurations": {
            "production": {
              "budgets": [
                {
                  "type": "initial",
                  "maximumWarning": "500kb",
                  "maximumError": "1mb"
                },
                {
                  "type": "anyComponentStyle",
                  "maximumWarning": "2kb",
                  "maximumError": "4kb"
                }
              ],
              "outputHashing": "all"
            },
            "development": {
              "optimization": false,
              "extractLicenses": false,
              "sourceMap": true,
              "namedChunks": true
            }
          },
          "defaultConfiguration": "production"
        },
        "serve": {
          "builder": "@angular-devkit/build-angular:dev-server",
          "configurations": {
            "production": {
              "browserTarget": "angular-app:build:production"
            },
            "development": {
              "browserTarget": "angular-app:build:development"
            }
          },
          "defaultConfiguration": "development"
        },
        "extract-i18n": {
          "builder": "@angular-devkit/build-angular:extract-i18n",
          "options": {
            "browserTarget": "angular-app:build"
          }
        },
        "test": {
          "builder": "@angular-devkit/build-angular:karma",
          "options": {
            "polyfills": [
              "zone.js",
              "zone.js/testing"
            ],
            "tsConfig": "tsconfig.spec.json",
            "assets": [
              "src/favicon.ico",
              "src/assets"
            ],
            "styles": [
              "src/styles.css"
            ],
            "scripts": []
          }
        }
      }
    }
  }
}''',
        'src/main.ts': '''import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';


platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.error(err));
''',
        'src/index.html': '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AngularApp</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
</head>
<body>
  <app-root></app-root>
</body>
</html>
''',
        'src/app/app.module.ts': '''import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
''',
        'src/app/app.component.ts': '''import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <div style="text-align:center">
      <h1>
        Welcome to {{title}}!
      </h1>
      <img width="300" alt="Angular Logo" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNTAgMjUwIj4KICAgIDxwYXRoIGZpbGw9IiNERDAwMzEiIGQ9Ik0xMjUgMzBMMzEuOSA2My4ybDE0LjIgMTIzLjFMMTI1IDIyM2w3OC45LTM2LjdMMjE4LjEgNjMuMnoiIC8+CiAgICA8cGF0aCBmaWxsPSIjQzMwMDJGIiBkPSJNMTI1IDMwTDI1IDY2LjJsMTQuMiAxMjMuMUwxMjUgMjIzdDEwMC44LTMzLjZMNTguMSA2My4yWiIgLz4KICAgIDxwYXRoIGZpbGw9IiNGRkZGRkYiIGQ9Ik0xMjUgNTJMMTguNSA5OS42TDEyNSAxOTguNkwyMzEuNSAxMDAuNFoiIC8+CiAgICA8cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNMTI1IDUybDc0LjUgMTQ2LjVMNTguNSAxMDAuNFoiIC8+CiAgPC9zdmc+Cg==">
    </div>
    <h2>Here are some links to help you start: </h2>
    <ul>
      <li>
        <h2><a target="_blank" rel="noopener" href="https://angular.io/tutorial">Tour of Heroes</a></h2>
      </li>
      <li>
        <h2><a target="_blank" rel="noopener" href="https://angular.io/cli">CLI Documentation</a></h2>
      </li>
      <li>
        <h2><a target="_blank" rel="noopener" href="https://angular.io/docs">Angular Documentation</a></h2>
      </li>
    </ul>
  `,
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'angular-app';
}
''',
        'src/app/app.component.css': '''div {
  font-family: Arial, Helvetica, sans-serif;
}
'''
    }


def get_svelte_template():
    return {
        'package.json': '''{
  "name": "svelte-app",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "dev": "svelte-kit dev",
    "build": "svelte-kit build",
    "preview": "svelte-kit preview"
  },
  "devDependencies": {
    "@sveltejs/kit": "^1.0.0",
    "svelte": "^3.44.0",
    "vite": "^4.0.0"
  },
  "type": "module"
}''',
        'svelte.config.js': '''import adapter from '@sveltejs/adapter-auto';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter()
	}
};

export default config;
''',
        'src/app.html': '''<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8" />
		<link rel="icon" href="/favicon.ico" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		%sveltekit.head%
	</head>
	<body>
		<div>%sveltekit.body%</div>
	</body>
</html>
''',
        'src/routes/+page.svelte': '''<script>
	let name = 'world';
</script>

<h1>Hello {name}!</h1>

<style>
	h1 {
		color: #ff3e00;
	}
</style>
'''
    }


def get_static_template():
    return {
        'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Static Site</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Welcome to your Static Site!</h1>
    <p>This is a simple HTML page.</p>
</body>
</html>
'''
    }


def get_django_template():
    return {
        'manage.py': '''#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
''',
        'myproject/settings.py': '''import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'your-secret-key'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
''',
        'myproject/urls.py': '''from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
''',
        'myproject/wsgi.py': '''import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = get_wsgi_application()
''',
        'requirements.txt': '''Django==4.2.7
'''
    }


def get_springboot_template():
    return {
        'pom.xml': '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>3.2.0</version>
		<relativePath/> <!-- lookup parent from repository -->
	</parent>
	<groupId>com.example</groupId>
	<artifactId>demo</artifactId>
	<version>0.0.1-SNAPSHOT</version>
	<name>demo</name>
	<description>Demo project for Spring Boot</description>
	<properties>
		<java.version>17</java.version>
	</properties>
	<dependencies>
		<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
		</dependency>

		<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-test</artifactId>
			<scope>test</scope>
		</dependency>
	</dependencies>

	<build>
		<plugins>
			<plugin>
				<groupId>org.springframework.boot</groupId>
				<artifactId>spring-boot-maven-plugin</artifactId>
			</plugin>
		</plugins>
	</build>

</project>
''',
        'src/main/java/com/example/demo/DemoApplication.java': '''package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class DemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}

	@GetMapping("/")
	public String hello() {
		return "Hello Spring Boot!";
	}

}
'''
    }


def get_aspnet_template():
    return {
        'Program.cs': '''var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello ASP.NET Core!");

app.Run();
''',
        'AspNetCoreApp.csproj': '''<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

</Project>
'''
    }


def get_gofiber_template():
    return {
        'go.mod': '''module gofiber-app

go 1.21.0

require github.com/gofiber/fiber/v2 v2.51.0
''',
        'main.go': '''package main

import (
	"log"

	"github.com/gofiber/fiber/v2"
)

func main() {
	app := fiber.New()

	app.Get("/", func(c *fiber.Ctx) error {
		return c.SendString("Hello, Fiber!")
	})

	log.Fatal(app.Listen(":3000"))
}
'''
    }


def get_echo_template():
    return {
        'go.mod': '''module echo-app

go 1.21.0

require github.com/labstack/echo/v4 v4.11.4
''',
        'main.go': '''package main

import (
	"net/http"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	// Echo instance
	e := echo.New()

	// Middleware
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	// Routes
	e.GET("/", hello)

	// Start server
	e.Logger.Fatal(e.Start(":1323"))
}

// Handler
func hello(c echo.Context) error {
	return c.String(http.StatusOK, "Hello, Echo!")
}
'''
    }


def get_ruby_rails_template():
    return {
        'Gemfile': '''source "https://rubygems.org"

gem "rails", "~> 7.0.0"
gem "sqlite3", "~> 1.4"

group :development, :test do
  gem "debug", platforms: %i[ mri ruby ]
end

group :development do
  gem "web-console"
end

group :test do
  gem "capybara"
  gem "selenium-webdriver"
  gem "cuprite"
end
''',
        'config/routes.rb': '''Rails.application.routes.draw do
  root "hello#index"
end
''',
        'app/controllers/hello_controller.rb': '''class HelloController < ApplicationController
  def index
    render plain: "Hello, Rails!"
  end
end
'''
    }