#!/usr/bin/bash

#File: tree-md

tree=$(tree --gitignore -tf --matchdirs --noreport -I '*~' -I '__pycache__' --charset ascii "$1" |
       sed -e 's/| \+/  /g' -e 's/[|`]-\+/ */g' -e 's:\(* \)\(\(.*/\)\([^/]\+\)\):\1[\4](\2):g')

printf "# Project tree\n\n %s" "${tree}"
