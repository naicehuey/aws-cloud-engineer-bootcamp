# Project 06 — Learning Notes

## EBS
Amazon Elastic Block Store (EBS) provides persistent block-level storage for EC2.

```text
EC2 = compute
EBS = storage
```

## Linux storage terms
| Term | Meaning | Mine |
|---|---|---|
| Block device | A disk exposed to Linux | `/dev/nvme1n1` |
| Partition | A section of a disk | `/dev/nvme1n1p1` |
| Filesystem | The structure used to store files | XFS |
| Mount point | The directory where the filesystem is reached | `/data` |

## Commands
| Command | Purpose |
|---|---|
| `lsblk` | List disks, partitions and mount points |
| `fdisk` | Create and manage partitions |
| `mkfs` | Create a filesystem |
| `mkdir` | Create a directory |
| `mount` | Mount a filesystem |
| `umount` | Unmount a filesystem |
| `df -h` | Show filesystem usage |
| `blkid` | Show UUID and filesystem details |
| `touch` | Create an empty file |
| `tee` | Write input to a file |
| `cat` | Display file contents |
| `nano` | Edit text files |

## Storage workflow
```text
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
```bash
lsblk
sudo fdisk /dev/nvme1n1
```

Inside `fdisk`:
```text
n
p
1
Enter
Enter
w
```

Always check the disk first. Never run `fdisk` or `mkfs` blindly against a device I don't know.

## Formatting
```bash
sudo mkfs -t xfs /dev/nvme1n1p1
```

## Mounting
```bash
sudo mkdir /data
sudo mount /dev/nvme1n1p1 /data
df -h
lsblk
```

## Testing
```bash
echo "Project 06 EBS storage is working." | sudo tee /data/ebs-test.txt
cat /data/ebs-test.txt
```

## UUID and fstab
Get the UUID:
```bash
sudo blkid /dev/nvme1n1p1
```

Persistent entry:
```text
UUID=<EBS_VOLUME_UUID> /data xfs defaults,nofail 0 2
```

Test it:
```bash
sudo umount /data
sudo mount -a
df -h /data
cat /data/ebs-test.txt
```

## Why UUID?
Linux device names can change depending on the order the devices are found. A filesystem UUID is a stable ID for `/etc/fstab`.

## Why nofail?
`nofail` is useful for extra, non-root storage. If the EBS volume isn't available, the system is less likely to fail to boot because of that optional mount.

## Troubleshooting

### `fdisk` "Value out of range"
I typed `w` while `fdisk` was asking for the partition type. The right answer to that prompt is:
```text
p
```
Then continue with the default partition number and sector values.

### `fstab` parse error
A malformed `/etc/fstab` entry can cause:
```text
mount: /etc/fstab: parse error
```
The EBS entry should have six fields:
```text
UUID=<UUID> /data xfs defaults,nofail 0 2
```
Check it with:
```bash
sudo mount -a
```

## Cost awareness
An EBS volume costs money while it exists, even when the instance is stopped. Delete the volume and the instance when I'm finished, and check Billing.

## Self-test
1. What is the difference between EC2 and EBS?
2. What is the difference between a partition and a filesystem?
3. Why run `lsblk` before `fdisk` or `mkfs`?
4. Why use a UUID in `/etc/fstab`?
5. What does `nofail` do?
6. How do I test an `fstab` change safely?

### Answers
1. EC2 is the virtual server (compute). EBS is persistent block storage attached to it.
2. A partition is a section of a disk. A filesystem is the structure that stores files on it.
3. To make sure I'm working on the right disk. These commands can erase data.
4. Device names can change, but the UUID stays the same.
5. It lets the server boot even if that extra volume is missing.
6. Run `sudo mount -a` and check `df -h` before rebooting.

## Core takeaway
**Attach → Detect → Partition → Format → Mount → Persist → Verify**
