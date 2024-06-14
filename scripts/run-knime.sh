#!/bin/bash

KNIME_HOME=/mnt/DATA/software/knime_5.2.0
#WORKFLOW_NAME=allmusic-list-search-artists
WORKFLOW_NAME=test3

#allmusic-list-search-artists

#-noexit -nosave

${KNIME_HOME}/knime -consoleLog -nosplash -reset \
    -data /mnt/DATA/develop/music-data/ \
    -workflowDir="/mnt/DATA/develop/music-data/knime-workspace/music-data/${WORKFLOW_NAME}/" \
    -application org.knime.product.KNIME_BATCH_APPLICATION \
    -vmargs -Djava.io.tmpdir=/mnt/DATA/develop/music-data/scripts/TMP/