#!/usr/bin/env bash

coverage run --source=. -m pytest 
coverage report
