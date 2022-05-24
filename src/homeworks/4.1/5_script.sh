#!/usr/bin/env bash

commitMessage=$1

if ! grep -qE "^\[.+\]\s.+" "$commitMessage"

then
    cat $commitMessage
    echo $'\nCommit message does not match pattern'
    exit 1
fi

maxLength=30
commitString=$(cat $commitMessage)
commitLength=${#commitString} 

if ((commitLength>maxLength))
then
    echo $'\n'$commitString
    echo $'\nCommit message is to long, maximum length '$maxLength
    exit 1
fi

exit 0