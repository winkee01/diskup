### Introduction
This program helps you visualize the disk usage when running chia plotting job are running. 

By visualizing the disk usage throughout the whole plotting process, you can find a good point to start a new parallel plotting job while not exceeding your SSD's capacity.

For example, you have a 380GB SSD, and you want to find out if you can run 2 plotting jobs and when can you start the second job, you can tell it from this graph.

![](https://github.com/winkee01/diskup/blob/main/image.png?raw=true) 

### Usage

**1) record.sh**
before you start your plotting job, run this command:

```
./record.sh <tmp_dir> <log_filename>
```

e.g. `./record.sh /mnt/my_ssd my_ssd.log`

You can change the interval by modidying `record.sh`, default is 10 seconds.

**2) my_ssd.log** 
Now we can draw diagram from `my_ssd.log` you generate in the previous step.

```
python3 diskup.py ssd.log
```

### Requirements

- **Python3**
- libs:

```
pip install numpy
pip install numpy
pip install matplotlib
```