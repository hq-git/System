#!/bin/bash

ps aux | grep -v grep|grep -v defunct| awk '/^apache/ {sum+=$6; n++}; END {print "total-process:\t" n "\taverage:\t " sum/n}'
