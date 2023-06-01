#!/bin/bash

# File containing the measures
file="/var/www/html/monitoring/measures"

### Measuring and converting data into %
# Date format ssss
date=$(date +"%s")
# Processor: 100 - idling time
processor=$(mpstat | awk '$12 ~ /[0-9.]+/ { print 100 - $12 }' | cut -d "," -f 1)
# Availible memory
memoryTotal=$(free | awk 'NR==2{ print $2}')
# Used memory
memoryUsed=$(free | awk 'NR==2{ print $3}')
# Memory in %
memory=$((memoryUsed*100/memoryTotal))
# Disc: used volume
disk=$(df -t ext4 | awk 'NR==2{ print $5}' | grep -Eo '[0-9]{1,3}') 

### Writing into the file
# Log line
echo "${date};${processor};${memory};${disk};" >> $file
# Croping the file
echo "$(tail -n 60 $file)" > $file