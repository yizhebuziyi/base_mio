#!/bin/bash
pidfile="/tmp/${1}.pid"
kill -INT $(cat ${pidfile})