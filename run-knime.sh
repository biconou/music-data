#!/usr/bin/env bash


KNIME_HOME=/mnt/DATA/software/knime_4.7.0/
WF_DIR=/mnt/DATA/develop/music-data/knime-workspace/allmusic-artist/

cd ${KNIME_HOME}

${KNIME_HOME}/knime -nosplash  -consoleLog -application org.knime.product.headless.KNIME_BATCH_APPLICATION​ \
    -workflowDir="${WF_DIR}"


