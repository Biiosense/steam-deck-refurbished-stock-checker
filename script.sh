#!/bin/bash

dir=/home/Max/GitHome/steam-deck-refurbished-stock-checker
${dir}/venv/bin/python ${dir}/checker.py >> ${dir}/steamdeck.log 2>&1

