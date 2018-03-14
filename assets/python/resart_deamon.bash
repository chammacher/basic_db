#!/bin/bash


result=`pgrep -fl check_deamon.py | wc -l`
if [ $result -eq 0 ]
then
    run = `/home/oper/qc/chance/mcusers/assets/python/check_deamon.py&>/dev/null&`
    $run 
    exit 1
fi


