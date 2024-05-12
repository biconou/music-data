#!/bin/bash

KNIME_HOME=/mnt/DATA/software/knime_5.2.0


#allmusic-list-search-artists

${KNIME_HOME}/knime -consoleLog -noexit -nosplash -reset \
    -data /mnt/DATA/develop/music-data/ \
    -workflowDir="/mnt/DATA/develop/music-data/knime-workspace/music-data/allmusic-list-search-artists/" \
    -application org.knime.product.KNIME_BATCH_APPLICATION