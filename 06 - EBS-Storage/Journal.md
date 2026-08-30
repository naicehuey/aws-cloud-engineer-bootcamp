# Project 06 --- EBS Storage Server Journal

## Objective

The objective was to gain practical experience with Amazon EBS and Linux
storage administration by attaching an additional EBS volume to an EC2
instance, preparing it for Linux, mounting it, testing it, and
configuring persistent mounting.

## 1. EBS Preparation

A 10 GiB EBS volume was attached to the Amazon Linux 2023 EC2 instance.

The first important concept was the distinction between compute and
storage:

-   EC2 = virtual server/compute
-   EBS = persistent block storage

## 2. Linux Disk Detection

After connecting to the instance, the storage devices were inspected
with:

``` bash
lsblk
```

The additional 10 GiB disk appeared separately from the root disk.

This was important because disk operations must target the correct
device.

## 3. Partitioning

The additional disk was opened with:

``` bash
sudo fdisk /dev/nvme1n1
```

The partition was created as a primary Linux partition using:

``` text
n
p
1
Enter
Enter
w
```

The result was:

``` text
nvme1n1
└─nvme1n1p1
```

## 4. Filesystem Creation

The new partition was formatted with XFS:

``` bash
sudo mkfs -t xfs /dev/nvme1n1p1
```

This taught the difference between a block device/partition and a usable
filesystem.

## 5. Mounting

A mount point was created:

``` bash
sudo mkdir /data
```

The filesystem was mounted:

``` bash
sudo mount /dev/nvme1n1p1 /data
```

`df -h` and `lsblk` confirmed that the approximately 10 GiB filesystem
was available at `/data`.

## 6. Storage Test

A test file was created:

``` bash
sudo touch /data/ebs-test.txt
echo "Project 06 EBS storage is working." | sudo tee /data/ebs-test.txt
```

It was verified with:

``` bash
cat /data/ebs-test.txt
```

The expected message was successfully returned.

## 7. Persistent Mount

The filesystem UUID was retrieved with:

``` bash
sudo blkid /dev/nvme1n1p1
```

The UUID was used in `/etc/fstab`:

``` text
UUID=<EBS_VOLUME_UUID> /data xfs defaults,nofail 0 2
```

There was an initial `/etc/fstab` parse error. The configuration was
corrected and tested again.

The final validation used:

``` bash
sudo umount /data
sudo mount -a
df -h /data
cat /data/ebs-test.txt
```

The final result confirmed that the filesystem could be mounted
successfully and that the test data remained accessible.

## Final Result

The completed storage path was:

``` text
EC2
 └── 10 GiB EBS
      └── /dev/nvme1n1
           └── /dev/nvme1n1p1
                └── XFS
                     └── /data
                          └── ebs-test.txt
```

## Reflection

The project was initially challenging because it combined AWS concepts
with Linux storage administration.

The most important lesson was the workflow rather than memorizing every
command:

**Attach → Detect → Partition → Format → Mount → Persist → Verify**

Understanding what each layer does makes the commands much easier to
remember.
