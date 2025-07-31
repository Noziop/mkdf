from typing import List, Dict, Any, Optional

def detect_database_service(components: List[str]) -> Optional[Dict[str, Any]]:
    """Detect the first database service and return its connection config (for backward compatibility)"""
    db_configs = {
        'postgresql': {
            'url_template': 'postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgresql:5432/${POSTGRES_DB}',
            'env_vars': ['POSTGRES_USER=user', 'POSTGRES_PASSWORD=password', 'POSTGRES_DB=dbname'],
            'service_name': 'postgresql',
            'req': {
                'fastapi': 'psycopg2-binary',
                'django': 'psycopg2-binary>=2.9,<3.0',
                'flask': 'psycopg2-binary',
                'gofiber': 'github.com/jinzhu/gorm/dialects/postgres',
                'laravel': 'doctrine/dbal',
                'symfony': 'doctrine/dbal'
            }
        },
        'mariadb': {
            'url_template': 'mysql+pymysql://${MARIADB_USER}:${MARIADB_PASSWORD}@mariadb:3306/${MARIADB_DATABASE}',
            'env_vars': ['MARIADB_ROOT_PASSWORD=rootpassword', 'MARIADB_DATABASE=dbname', 'MARIADB_USER=user', 'MARIADB_PASSWORD=password'],
            'service_name': 'mariadb',
            'req': {
                'fastapi': 'pymysql',
                'django': 'mysqlclient>=2.1,<2.2',
                'flask': 'PyMySQL',
                'gofiber': 'github.com/jinzhu/gorm/dialects/mysql',
                'laravel': 'doctrine/dbal',
                'symfony': 'doctrine/dbal'
            }
        },
        'mysql': {
            'url_template': 'mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@mysql:3306/${MYSQL_DATABASE}',
            'env_vars': ['MYSQL_ROOT_PASSWORD=rootpassword', 'MYSQL_DATABASE=dbname', 'MYSQL_USER=user', 'MYSQL_PASSWORD=password'],
            'service_name': 'mysql',
            'req': {
                'fastapi': 'pymysql',
                'django': 'mysqlclient>=2.1,<2.2',
                'flask': 'PyMySQL',
                'gofiber': 'github.com/jinzhu/gorm/dialects/mysql',
                'laravel': 'doctrine/dbal',
                'symfony': 'doctrine/dbal'
            }
        },
        'mongodb': {
            'url_template': 'mongodb://${MONGO_INITDB_ROOT_USERNAME}:${MONGO_INITDB_ROOT_PASSWORD}@mongodb:27017/',
            'env_vars': ['MONGO_INITDB_ROOT_USERNAME=user', 'MONGO_INITDB_ROOT_PASSWORD=password', 'MONGO_INITDB_DATABASE=dbname'],
            'service_name': 'mongodb',
            'req': {
                'fastapi': 'motor',
                'gofiber': 'go.mongodb.org/mongo-driver/mongo',
                'laravel': 'mongodb/laravel-mongodb',
                'symfony': 'mongodb/mongodb'
            }
        }
    }

    for component in components:
        if component in db_configs:
            return db_configs[component]
    return None

def detect_all_database_services(components: List[str]) -> List[Dict[str, Any]]:
    """Detect all database services and return their configs"""
    db_configs = {
        'postgresql': {
            'url_template': 'postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgresql:5432/${POSTGRES_DB}',
            'env_vars': ['POSTGRES_USER=user', 'POSTGRES_PASSWORD=password', 'POSTGRES_DB=dbname'],
            'service_name': 'postgresql',
            'req': {
                'fastapi': 'psycopg2-binary',
                'django': 'psycopg2-binary>=2.9,<3.0',
                'flask': 'psycopg2-binary',
                'gofiber': 'github.com/jinzhu/gorm/dialects/postgres',
                'laravel': 'doctrine/dbal',
                'symfony': 'doctrine/dbal'
            }
        },
        'mariadb': {
            'url_template': 'mysql+pymysql://${MARIADB_USER}:${MARIADB_PASSWORD}@mariadb:3306/${MARIADB_DATABASE}',
            'env_vars': ['MARIADB_ROOT_PASSWORD=rootpassword', 'MARIADB_DATABASE=dbname', 'MARIADB_USER=user', 'MARIADB_PASSWORD=password'],
            'service_name': 'mariadb',
            'req': {
                'fastapi': 'pymysql',
                'django': 'mysqlclient>=2.1,<2.2',
                'flask': 'PyMySQL',
                'gofiber': 'github.com/jinzhu/gorm/dialects/mysql',
                'laravel': 'doctrine/dbal',
                'symfony': 'doctrine/dbal'
            }
        },
        'mysql': {
            'url_template': 'mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@mysql:3306/${MYSQL_DATABASE}',
            'env_vars': ['MYSQL_ROOT_PASSWORD=rootpassword', 'MYSQL_DATABASE=dbname', 'MYSQL_USER=user', 'MYSQL_PASSWORD=password'],
            'service_name': 'mysql',
            'req': {
                'fastapi': 'pymysql',
                'django': 'mysqlclient>=2.1,<2.2',
                'flask': 'PyMySQL',
                'gofiber': 'github.com/jinzhu/gorm/dialects/mysql',
                'laravel': 'doctrine/dbal',
                'symfony': 'doctrine/dbal'
            }
        },
        'mongodb': {
            'url_template': 'mongodb://${MONGO_INITDB_ROOT_USERNAME}:${MONGO_INITDB_ROOT_PASSWORD}@mongodb:27017/',
            'env_vars': ['MONGO_INITDB_ROOT_USERNAME=user', 'MONGO_INITDB_ROOT_PASSWORD=password', 'MONGO_INITDB_DATABASE=dbname'],
            'service_name': 'mongodb',
            'req': {
                'fastapi': 'motor',
                'gofiber': 'go.mongodb.org/mongo-driver/mongo',
                'laravel': 'mongodb/laravel-mongodb',
                'symfony': 'mongodb/mongodb'
            }
        }
    }
    
    found_configs = []
    for component in components:
        if component in db_configs:
            found_configs.append(db_configs[component])
    
    return found_configs
