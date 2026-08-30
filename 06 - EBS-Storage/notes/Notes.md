# Project 06 --- EBS Storage Notes

## EBS

Amazon Elastic Block Store provides persistent block-level storage for
EC2.

``` text
EC2 = compute
EBS = storage
```

## Linux Storage Terms

-   **Block device:** disk exposed to Linux, e.g. `/dev/nvme1n1`
-   **Partition:** section of a disk, e.g. `/dev/nvme1n1p1`
-   **Filesystem:** structure used to store files; this project used XFS
-   **Mount point:** directory through which the filesystem is accessed;
    this project used `/data`

## Commands

  Command    Purpose
  ---------- -----------------------------------------
  `lsblk`    List disks, partitions and mount points
  `fdisk`    Create/manage partitions
  `mkfs`     Create a filesystem
  `mkdir`    Create a directory
  `mount`    Mount a filesystem
  `umount`   Unmount a filesystem
  `df -h`    Show filesystem usage
  `blkid`    Show UUID and filesystem metadata
  `touch`    Create an empty file
  `tee`      Write input to a file
  `cat`      Display file contents
  `nano`     Edit text files

## Storage Workflow

``` text
EBS volume
    ↓
Linux disk
    ↓
Partition
    ↓
Filesystem
    ↓
Mount point
    ↓
/etc/fstab
    ↓
Verification
```

## Partitioning

``` bash
lsblk
sudo fdisk /dev/nvme1n1
```

Inside `fdisk`:

``` text
n
p
1
Enter
Enter
w
```

Always verify the disk first. Never blindly run `fdisk` or `mkfs`
against an unknown device.

## Formatting

``` bash
sudo mkfs -t xfs /dev/nvme1n1p1
```

## Mounting

``` bash
sudo mkdir /data
sudo mount /dev/nvme1n1p1 /data
df -h
lsblk
```

## Testing

``` bash
echo "Project 06 EBS storage is working." | sudo tee /data/ebs-test.txt
cat /data/ebs-test.txt
```

## UUID and fstab

Get the UUID:

``` bash
sudo blkid /dev/nvme1n1p1
```

Persistent entry:

``` text
UUID=<EBS_VOLUME_UUID> /data xfs defaults,nofail 0 2
```

Test it:

``` bash
sudo umount /data
sudo mount -a
df -h /data
cat /data/ebs-test.txt
```

## Why UUID?

Linux device names can change depending on device discovery order. A
filesystem UUID provides a stable identifier for `/etc/fstab`.

## Why nofail?

`nofail` is useful for additional, non-root storage. If the EBS volume
is unavailable, the system is less likely to fail its boot process
because of that optional mount.

## Troubleshooting

### fdisk "Value out of range"

`w` was entered while `fdisk` expected a partition type. The correct
response to the partition type prompt is:

``` text
p
```

Then continue with the default partition number and sector values.

### fstab parse error

A malformed `/etc/fstab` entry can cause:

``` text
mount: /etc/fstab: parse error
```

The EBS entry should have six fields:

``` text
UUID=<UUID> /data xfs defaults,nofail 0 2
```

Validate with:

``` bash
sudo mount -a
```

## Final Checklist

-   [x] EBS volume attached
-   [x] Disk detected with `lsblk`
-   [x] Partition created
-   [x] XFS filesystem created
-   [x] `/data` mount point created
-   [x] EBS mounted
-   [x] Test file written
-   [x] Test file read successfully
-   [x] UUID obtained
-   [x] `/etc/fstab` configured
-   [x] Persistent mount tested
-   [x] Project completed

## Core Takeaway

**Attach → Detect → Partition → Format → Mount → Persist → Verify**
