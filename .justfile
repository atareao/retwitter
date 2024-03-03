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
    if docker ps | grep {{name}}; then
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
               -e CONFIG_FILE="/app/config.json" \
               -e COOKIES_FILE="/app/cookies.json" \
               --detach \
               --volume $PWD/config.json:/app/config.json:ro \
               --volume $PWD/cookies.json:/app/cookies.json:ro \
               --volume /etc/timezone:/etc/timezone:ro \
               --volume /etc/localtime:/etc/localtime:ro \
               {{user}}/{{name}}:latest

stop:
    docker stop {{name}}

run:
    poetry run python expertos/main.py

run-test:
    poetry run pytest tests --show-capture=all
