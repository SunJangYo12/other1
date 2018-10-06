#!/bin/bash

pid=$1
delay=0.15
spinstr='|/-\'
while [ true ]; do
	temp=${spinstr#?}
	printf " [%c]  " "$spinstr"
	spinstr=$temp${spinstr%"$temp"}
	sleep $delay
	printf "\b\b\b\b\b\b"
done
printf "    \b\b\b\b"
