#!/bin/sh
DIR=${1:-.}
FILES=`find $DIR \
       \( -name \*.pyc -o \
          -name \#\* -o \
          -name \*\~  -o \
          -name \.\*\~ \) -print`
if [ "$FILES" != "" ]
then
	echo Removing files $FILES
	rm  $FILES
fi

# reomve any data directory created inside the application (for example
# by running the application locally)
rm -rf wanderer/data
