# Project 06 --- AWS EBS Storage Server

## Overview

This project demonstrates attaching and configuring an Amazon Elastic
Block Store (EBS) volume on an Amazon Linux 2023 EC2 instance.

**Final configuration** - EC2 instance: `06-ebs-storage-server` -
Instance type: `t3.micro` - OS: Amazon Linux 2023 - Region:
`us-east-1` - Additional EBS volume: 10 GiB - Filesystem: XFS - Mount
point: `/data`

Sensitive account identifiers, IP addresses, and credentials are
intentionally excluded.

## Architecture

``` text
AWS EBS Volume
      ↓
EC2 Instance
      ↓
Linux block device
      ↓
Partition
      ↓
XFS filesystem
      ↓
/data
      ↓
Persistent /etc/fstab mount
```

## What Was Completed

1.  Attached a 10 GiB EBS volume to the EC2 instance.
2.  Detected the disk with `lsblk`.
3.  Created a partition using `fdisk`.
4.  Formatted the partition with XFS.
5.  Created `/data`.
6.  Mounted the EBS filesystem at `/data`.
7.  Created and read a test file.
8.  Retrieved the filesystem UUID with `blkid`.
9.  Configured `/etc/fstab` for persistent mounting.
10. Verified the mount with `mount -a` and `df -h`.

## Core Commands

``` bash
lsblk
sudo fdisk /dev/nvme1n1
sudo mkfs -t xfs /dev/nvme1n1p1
sudo mkdir /data
sudo mount /dev/nvme1n1p1 /data
df -h
sudo blkid /dev/nvme1n1p1
```

Test:

``` bash
echo "Project 06 EBS storage is working." | sudo tee /data/ebs-test.txt
cat /data/ebs-test.txt
```

Persistent mount entry:

``` text
UUID=<EBS_VOLUME_UUID> /data xfs defaults,nofail 0 2
```

Verification:

``` bash
sudo umount /data
sudo mount -a
df -h /data
cat /data/ebs-test.txt
```

## Key Lessons

-   EC2 provides compute; EBS provides persistent block storage.
-   A new disk must be detected, partitioned, formatted, mounted, and
    verified.
-   `lsblk` is useful for identifying disks and partitions.
-   `mkfs` creates a filesystem.
-   `mount` makes a filesystem accessible through a directory.
-   UUIDs are useful for persistent filesystem identification.
-   `/etc/fstab` controls persistent mounts.
-   `nofail` is appropriate for optional additional storage.
-   Always run `lsblk` before destructive disk commands such as `fdisk`
    or `mkfs`.

## Troubleshooting Lessons

During the project, `fdisk` initially rejected `w` because the utility
was asking for the partition type. The correct sequence was:

``` text
n
p
1
Enter
Enter
w
```

An `/etc/fstab` syntax error also occurred during configuration. The
entry was corrected and then validated with:

``` bash
sudo mount -a
```

## Suggested Evidence

Use only screenshots actually captured during the project. Suggested
names:

-   `01-ec2-ebs-attached.png`
-   `02-ebs-volume-details.png`
-   `03-ec2-running.png`
-   `04-ebs-device-detected.png`
-   `05-ebs-partition-created.png`
-   `06-ebs-filesystem-created.png`
-   `07-ebs-mounted-and-tested.png`
-   `08-ebs-fstab-verified.png`

## Status

**Completed successfully.**
