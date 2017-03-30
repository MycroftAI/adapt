#!/bin/bash
TOP=$(cd $(dirname $0) && pwd)

function doc() {
  local MODULE=$1
  local OUTPUT_DIR=${TOP}/build/doc/html/$(dirname $MODULE)
  mkdir -p ${OUTPUT_DIR}
  PYTHONPATH=. pdoc --html\
       --overwrite\
       --html-dir ${OUTPUT_DIR}\
       $MODULE
}
cd ${TOP}
doc adapt
for i in $(find adapt/*| grep -v pyc); do
  doc $i
done
for i in $(find adapt/* -type d | sed -s 's/\//./g'); do
  doc $i
done
#OUTPUT_DIR=${TOP}/build/doc/html/
#cd $OUTPUT_DIR && python -m SimpleHTTPServer 1234
#PYTHONPATH=. pydoc -p 1234 --html-dir ${OUTPUT_DIR}\


