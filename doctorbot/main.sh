#!/bin/bash

set -eux
DATE="11-04"
SITE="http://www.fjsdsrmyy.com/showdoc.aspx?Id=4bbb332d-2c77-4d03-8f94-0a350343"

python doctorbot/spider.py ${DATE} ${SITE}
