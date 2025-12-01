#!/bin/bash

mode="$1"
shift  # Supprime le premier argument de la liste

if [ "$mode" = "togodo" ] || [ "$mode" = "dev" ]; then
    autres_args=("$@")  # Stocker le reste des arguments dans un tableau
    echo "Mode : $mode"
    echo "Autres arguments : ${autres_args[*]}"
else
    echo "Erreur : le premier argument doit être 'togodo' ou 'dev'" >&2
    exit 1
fi

docker-compose --project-name music-data-${mode} --env-file .env.${mode} ${autres_args[*]}
