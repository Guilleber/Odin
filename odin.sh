#!/bin/bash

LOCAL_PATH="$(dirname "$(readlink -f "$0")")"

VERB=$1
shift

case $VERB in
	start)
		$LOCAL_PATH/start.sh
		;;
	stop)
		$LOCAL_PATH/stop.sh
		;;
	add)
		$LOCAL_PATH/venv/bin/python3 $LOCAL_PATH/add.py "$@"
		;;
	find)
		$LOCAL_PATH/venv/bin/python3 $LOCAL_PATH/find.py "$@"
		;;
	move|mv)
		$LOCAL_PATH/venv/bin/python3 $LOCAL_PATH/move.py "$@"
		;;
	*)
		echo "Invalid verb: options are 'start', 'stop', 'add', 'find', 'move'"
		;;
esac
