#!/bin/sh
source ~/.bashrc

echo "Enter your design name:"
read design

if `ls | grep -q "\<${design}.sp\>"`
    then
        echo "HSPICE simulation of ${design} will be executed"

        mkdir pre_stress
        hs -mt 20 -i ./${design}.sp -o ./pre_stress/${design}.lis
    else
        echo "Can't find ${design} in this directory"
fi




