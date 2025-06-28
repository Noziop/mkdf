from mkdf.templates.docker.base.service_template import DockerService
from typing import List, Dict, Any, Optional
from mkdf.templates.docker.base.db_utils import detect_database_service

class GoFiberService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        if components is None:
            components = []

        db_config = detect_database_service(components)
        depends_on = []
        if db_config:
            depends_on.append(db_config['service_name'])

        config = {
            'build': {
                'context': './backend',
                'dockerfile': 'Dockerfile'
            },
            'container_name': '${PROJECT_NAME:-fullstack}-backend',
            'ports': ['3000'],
            'volumes': ['./backend:/app'],
            'networks': ['app-network']
        }

        if depends_on:
            config['depends_on'] = depends_on

        return config

    def get_dockerfile_content(self) -> Optional[str]:
        return '''FROM golang:1.19-alpine

WORKDIR /app

COPY go.mod ./
RUN go mod download

COPY . .

RUN go build -o /go-fiber-app

EXPOSE 3000

CMD ["/go-fiber-app"]
'''

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        if components is None:
            components = []

        db_config = detect_database_service(components)
        
        go_mod_content = '''module my-gofiber-app

        go 1.19

        require github.com/gofiber/fiber/v2 v2.40.1
        '''
        main_go_content = '''package main

        import "github.com/gofiber/fiber/v2"

        func main() {
            app := fiber.New()

            app.Get("/", func(c *fiber.Ctx) error {
                return c.SendString("Hello, from Go Fiber!")
            })

            app.Listen(":3000")
        }
        '''

        if db_config:
                    go_mod_content += f'\nrequire {db_config["req"]["gofiber"]}'
                    main_go_content = f'''package main

        import (
            "github.com/gofiber/fiber/v2"
            "fmt"
            "os"
            "{db_config['req']['gofiber']}"
        )

        func main() {{
            app := fiber.New()

            dbURL := os.Getenv("DATABASE_URL")
            if dbURL == "" {{
                fmt.Println("DATABASE_URL environment variable not set.")
                // Handle error or use a default database
            }}

            // Example: Connect to database (replace with actual connection logic)
            // db, err := gorm.Open(postgres.Open(dbURL), &gorm.Config{{}})
            // if err != nil {{
            // 	panic("failed to connect database")
            // }}

            app.Get("/", func(c *fiber.Ctx) error {{
                return c.SendString("Hello, from Go Fiber!")
            }})

            app.Listen(":3000")
        }}
        '''

        return {
            'go.mod': go_mod_content,
            'main.go': main_go_content
        }