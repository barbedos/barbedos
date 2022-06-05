#!/bin/bash
# Used to deploy all functions in argument list

PROJECT_ID="serverless-d2414"
PROJECT_NAME="Serverless"
DEPLOY_TEST=false
DEPLOY_LOCAL=false

RUNTIME="python39"
REGION="us-central1"
FILES="files"
FORM="form"
ALL="$FILES $FORM"
CURPWD=$PWD

trap ctrl_c INT

function ctrl_c() {
    printf "\nKilling subprocesses\n"
    [[ -z "$(jobs -p)" ]] && return # no jobs to kill
    jobs -p | xargs kill  # kill each job's processes group
}

function usage() {
    echo "deploy.sh [-h] [-l] [-t] [func1] ..."
    echo "   -h   Help"
    echo "   -l   Start Local functions-framework"
    echo "   -t   Deploy -test Functions on Google Cloud"
}

# Process arguments
while getopts "hlt" opt; do
    case $opt in
        h) usage; exit 0;;
        t) DEPLOY_TEST=true;;
        l) DEPLOY_LOCAL=true;;
    esac
done
shift $((OPTIND-1))
funcs="$*"

# Make sure the GOOGLE_APPLICATION_CREDENTIALS variable is set
if [[ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]]; then
    echo "You must first set the GOOGLE_APPLICATION_CREDENTIALS env variable"
    exit 1
fi

# Bash version check
if [[ $BASH_VERSINFO -le 4 ]]; then
    echo "You're using a really old version of bash. Minimum version is 4"
    exit 1
fi

# Set gcloud
echo "gcloud config set account brian.barbe@gmail.com"
gcloud config set account brian.barbe@gmail.com
echo "gcloud config set project serverless-d2414"
gcloud config set project serverless-d2414

# Declare function ports
declare -A PORTS
PORTS[files]=8080
PORTS[form]=8081

# Install all functions if none are provided
if [[ -z "$funcs" ]]; then
    funcs="$ALL"
fi

# Deploy each function
for func in $funcs; do
    epoch_start=$(date -u '+%s')
    printf "Deploying $func ...\n"
    funcname=$func
    if [[ "$DEPLOY_TEST" == "true" ]]; then
        funcname="${funcname}-test"
    fi

    if [[ "$DEPLOY_LOCAL" == "false" ]]; then
        cmd=$(printf "%s %s %s %s %s %s %s" \
              "gcloud functions deploy $funcname" \
              "--entry-point $func" \
              "--source $func" \
              "--region $REGION" \
              "--runtime $RUNTIME" \
              "--trigger-http" \
              "--allow-unauthenticated")
    else
        cmd=$(printf "%s %s %s %s" \
              "functions-framework" \
              "--target $funcname" \
              "--port ${PORTS[$funcname]}" \
              "--debug")
        cd ${CURPWD}/$funcname
    fi
    printf "$cmd\n"
    # Run local scripts in the background
    if [[ "$DEPLOY_LOCAL" == "true" ]]; then
        $cmd &
    else
        $cmd
    fi

    epoch_end=$(date -u '+%s')
    if [[ "$DEPLOY_LOCAL" == "false" ]]; then
        printf "Elapsed time: $((epoch_end-epoch_start)) seconds\n\n"
        sleep 5
    fi
done
wait
