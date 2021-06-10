### Introduction
This program helps you visualize the disk usage when running chia plotting job are running. 

By visualizing the disk usage throughout the whole plotting process, you can find a good point to start a new parallel plotting job while not exceeding your SSD's capacity.

For example, you have a 380GB SSD (real capacity is only 362GB), and you want to find out if you can run two k32 plotting jobs and when can you start the second job, you can tell it from this graph.

![](https://github.com/winkee01/diskup/blob/master/sample.png?raw=true) 

### Usage

##### 1) record.sh
before you start your plotting job, run this command:

```
./record.sh <tmp_dir> <log_filename>
```

e.g. `./record.sh /mnt/my_ssd my_ssd.log`

You can change the interval by modidying `record.sh`, default is 10 seconds.

##### 2) my_ssd.log
After plottting process finished its job, you can draw diagram from `my_ssd.log` by this:

```
python3 draw.py ssd.log
```

### Requirements

- **Python3**
- libs:

```
pip install numpy
pip install pandas
pip install matplotlib
```