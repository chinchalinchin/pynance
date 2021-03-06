SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='web-server'
nl=$'\n'
tab="     "
ind="   "
SCRIPT_DES="Execute this script to launch the development frontend server. Change WEB_PORT in\
\e[3m/env/.env\e[0m to modify the port ${nl}${ind}the server will run on. The server can either\
started locally or inside of a container. If no argument${nl}${ind} is provided, the script will\
default to \e[3mlocal\e[0m${nl}${nl}${tab}${tab}OPTIONS: ${nl}${tab}${tab}${ind}--local/-l\ = \
Invokes \e[2mng serve --port WEB_PORT\e[0m from the \e[3m/frontend/\e[0m directory.\
${nl}${tab}${tab}${ind}--container/-c\= Builds and runs a Docker image of the application within\
an nginx container mapped to WEB_PORT.${nl}${tab}${tab}${ind}--help/-h = Displays this help message." 

source $SCRIPT_DIR/../util/logging.sh

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help "$SCRIPT_DES" $SCRIPT_NAME
else
    # DIRECTORIES
    PROJECT_DIR="$SCRIPT_DIR/../.."
    DOCKER_DIR="$PROJECT_DIR/scripts/docker"
    FRONTEND_DIR="$PROJECT_DIR/frontend/pynance-web"
    BUILD_DIR="$PROJECT_DIR/frontend/build"
    SERVER_DIR="$PROJECT_DIR/frontend/server"
    FRONTEND_DOCS_DIR="$FRONTEND_DIR/src/assets/docs"
    DOCS_RAW_DIR="$PROJECT_DIR/frontend/docs"
    DOCS_BUILD_DIR="$DOCS_RAW_DIR/build/html"
    UTIL_DIR="$PROJECT_DIR/scripts/util"
    ENV_DIR="$PROJECT_DIR/env"

    # Run in development mode
    if [ "$1" == "--dev" ] || [ "$1" == "-dev" ] || [ "$1"  == "--d" ] || [ "$1" == "-d" ] || [ $# -eq 0 ]
    then
        log "Invoking \e[3menv-vars\e[0m script." $SCRIPT_NAME
        source "$UTIL_DIR/env-vars.sh" local

        cd "$DOCS_RAW_DIR"
        log "Installing documentation dependencies." $SCRIPT_NAME
        pip3 install -r requirements.txt

        log "Building documentation pages." $SCRIPT_NAME
        make html

        log "Copying generated documentation into Angular assets directory." $SCRIPT_NAME
        cp -r "$DOCS_BUILD_DIR"/* "$FRONTEND_DOCS_DIR/"

        cd "$FRONTEND_DIR"
        log "Installing Node dependencies." $SCRIPT_NAME
        npm install 

        log "Launching Angular Development server on \e[3mlocalhost:$WEB_PORT\e[0m." $SCRIPT_NAME
        ng serve --port "$WEB_PORT"
    fi

    # Run in local mode
    if [ "$1" == "--local" ] || [ "$1" == "-local" ] || [ "$1"  == "--l" ] || [ "$1" == "-l" ] || [ $# -eq 0 ]
    then
        log "Invoking \e[3menv-vars\e[0m script." "$SCRIPT_NAME"
        source "$UTIL_DIR/env-vars.sh" local

        cd "$DOCS_RAW_DIR"
        log "Installing documentation dependencies." "$SCRIPT_NAME"
        pip3 install -r requirements.txt

        log "Building documentation pages." "$SCRIPT_NAME"
        make html

        log "Copying generated documentation into Angular assets directory." "$SCRIPT_NAME"
        cp -r "$DOCS_BUILD_DIR"/* "$FRONTEND_DOCS_DIR/"

        cd "$FRONTEND_DIR"
        log "Installing Node dependencies." "$SCRIPT_NAME"
        npm install 

        log "Building Angular webpacks." "$SCRIPT_NAME"
        ng build --prod --output-hashing none

        log "Configuring nginx server." "$SCRIPT_NAME"
        ROOT_DIR="$(cd $BUILD_DIR && pwd)"
        echo "$ROOT_DIR"
        envsubst '$APP_PORT,$APP_HOST,$WEB_PORT, $ROOT_DIR' < "$SERVER_DIR/nginx.template.conf" | sponge "$SERVER_DIR/nginx.conf"

        log "Launching nginx server on $WEB_HOST:$WEB_PORT" "$SCRIPT_NAME"
        # don't like having sudo here...
        sudo nginx -c "$SERVER_DIR/nginx.conf" -s reload
    fi

    # Run in container mode
    if [ "$1" == "--container" ] || [ "$1" = "-container" ] || [ "$1" == "--c" ] || [ "$1" == "-c" ]
    then
        log "Invoking \e[3menv-vars\e[0m script." $SCRIPT_NAME
        source "$UTIL_DIR/env-vars.sh" container

        log "Checking if \e[3m$WEB_CONTAINER_NAME\e[0m container is currently running." $SCRIPT_NAME
        if [ "$(docker ps -q -f name=$WEB_CONTAINER_NAME)" ]
        then
            log "Stopping \e[3m$WEB_CONTAINER_NAME\e[0m container." $SCRIPT_NAME
            docker container stop "$WEB_CONTAINER_NAME"

            log "Removing \e[3m$WEB_CONTAINER_NAME\e[0m container." $SCRIPT_NAME
            docker rm "$WEB_CONTAINER_NAME"
        fi

        log "Invoking \e[3mweb-container\e[0m script." $SCRIPT_NAME
        bash "$DOCKER_DIR/build-container.sh" frontend

        log "Publishing \e[3m$WEB_IMG_NAME:$WEB_TAG_NAME\e[0m with container name \e[3m$WEB_CONTAINER_NAME\e[0m on \e[3mlocalhost:$APP_PORT\e[0m." $SCRIPT_NAME
        docker run \
        --name $WEB_CONTAINER_NAME \
        --publish $WEB_PORT:$WEB_PORT \
        --env-file $ENV_DIR/container.env \
        $WEB_IMG_NAME:$WEB_TAG_NAME
    fi
fi