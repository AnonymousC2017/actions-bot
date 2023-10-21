#!/bin/bash

set -eux
DATE="11-01"
SITE="http://www.fjsdsrmyy.com/showdoc.aspx?docname=%E5%91%A8%E4%B8%BD"

python doctorbot/spider.py ${DATE} ${SITE}
