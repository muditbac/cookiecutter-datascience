#!/usr/bin/env bash

while true; do
  inotifywait -r -e modify,create,delete ./
  rsync -r -a -v -z -e "ssh -l <<username>> -i <<key>>" ./ <<host>>:<<path>> \
    --exclude ".git/" \
    --exclude "data/"
done



#Exclude Files and Directories from a List
#When you need to exclude a large number of different files and directories,
# you can use the rsync --exclude-from flag. To do so, create a text file with the name of the files and
# directories you want to exclude. Then, pass the name of the file to the --exlude-from option.
#
#The command looks like this:
#
#rsync -av --exclude-from={'list.txt'} sourcedir/ destinationdir/
