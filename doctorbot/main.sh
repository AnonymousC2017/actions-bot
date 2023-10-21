#!/bin/bash

set -eux
DATE="10-23"
SITE="http://www.fjsdsrmyy.com/showdoc.aspx?Id=4bbb332d-2c77-4d03-8f94-0a350346"

python doctorbot/spider.py ${DATE} ${SITE}
