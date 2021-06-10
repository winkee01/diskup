#!/usr/bin/bash
chia_executable=chia_plot
#!/bin/bash
chia_executable=chia
me=`basename "$0"`
target_dir=${1:?"You must specify a target directory"}

if [ ! -d $target_dir ]; then
       echo "directory $target_dir does not exist"
       exit -1
fi

printf "\n"
printf "target dir: $target_dir\n"

log_file=${2:?"You must specify a log file"}
if ! `touch $log_file`; then
    echo "file to create $log_file"
    exit -1
fi
printf  "log file: $PWD/$log_file\n"

check_times=0

while true; do
    if [[ $check_times -gt 12 ]]; then
        break
    fi

    chia_running=$(pgrep $chia_executable)
    if [[ $chia_running == "" ]]; then
        check_times=$(expr $check_times + 1)
        sleep 10
        continue
    fi

    cur_time=$(date +%H:%M:%S)
    dir_size=$(du -c $target_dir/* 2>&1 | tail -1 | awk '{print $1}')
    p1_size=$(du -c $target_dir/*.p1* 2>&1 | tail -1 | awk '{print $1}')
    p2_size=$(du -c $target_dir/*.p2* 2>&1 | tail -1 | awk '{print $1}')
    p3_size=$(du -c $target_dir/*.p3* 2>&1 | tail -1 | awk '{print $1}')
    p4_size=$(du -c $target_dir/*.p4* 2>&1 | tail -1 | awk '{print $1}')
    table_size=$(du -c $target_dir/*table* 2>&1 | tail -1 | awk '{print $1}')

    phase_string="$p1_size $p2_size $p3_size $p4_size"

    if [[ $dir_size -gt 4 ]]; then
        echo "$cur_time $dir_size $phase_string $table_size" >> $log_file
    fi

    sleep 10
done

pkill $me