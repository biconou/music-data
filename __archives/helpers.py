#!/usr/bin/env python
import logging
import subprocess
import sys

def grabHTMLPage(pageUrl):
    logging.debug('Grab html page ' + pageUrl)
    response = subprocess.check_output(['curl',pageUrl]).decode(sys.stdout.encoding)
    return response
