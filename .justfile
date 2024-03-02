user    := "atareao"
name    := `basename ${PWD}`
version := `git tag -l  | tail -n1`

default:
    @just --list

rebuild:
    echo {{version}}
    echo {{name}}
    docker build --no-cache \
                 -t {{user}}/{{name}}:{{version}} \
                 -t {{user}}/{{name}}:latest \
                 .
build:
    echo {{version}}
    echo {{name}}
    docker build -t {{user}}/{{name}}:{{version}} \
                 -t {{user}}/{{name}}:latest \
                 .

push:
    docker push {{user}}/{{name}}:{{version}}
    docker push {{user}}/{{name}}:latest

build-test:
    echo {{version}}
    echo {{name}}
    docker build -t {{user}}/{{name}}:test \
                 .
test:
    #!/bin/bash
    docker ps | grep {{name}}
    if [[ $? -eq 0 ]]; then
        docker stop {{name}}
        docker wait {{name}}
        while docker ps | grep {{name}};do
            echo "sleeping"
            sleep 1
        done
    fi
    echo "starting"
    docker run --rm \
               --init \
               --name {{name}} \
               --detach \
               -p 8000:8000 \
               --volume $PWD/config.toml:/app/config.toml:ro \
               --volume /etc/timezone:/etc/timezone:ro \
               --volume /etc/localtime:/etc/localtime:ro \
               {{user}}/{{name}}:latest

stop:
    docker stop {{name}}

run:
    poetry run python expertos/main.py

run-test:
    poetry run pytest tests --show-capture=all
