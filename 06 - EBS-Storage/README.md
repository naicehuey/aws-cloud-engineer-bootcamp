# Project 06 — EBS Storage

## Overview
My first lab with Amazon EBS (Elastic Block Store). I attached an extra 10 GiB disk to an Amazon Linux 2023 EC2 instance and then set it up by hand in Linux: found the disk, partitioned it, formatted it, mounted it, tested it, and set it up so it mounts again automatically. This project mixed AWS with Linux storage, which made it harder than my earlier ones. I'm a beginner with both, so this README records what I did and what I understood so far.

## Stack
Amazon EBS · Amazon EC2 · Amazon Linux 2023 · Linux (`fdisk`, XFS, `/etc/fstab`) · AWS Management Console

## What I practiced
- Attaching an extra EBS volume to an EC2 instance
- Finding a new disk with `lsblk`
- Creating a partition with `fdisk`
- Creating an XFS filesystem with `mkfs`
- Mounting a filesystem and testing it with a file
- Using a UUID in `/etc/fstab` so the mount survives a reboot
- Troubleshooting an `fdisk` mistake and an `fstab` error

## Configuration
| Setting | Value |
|---|---|
| EC2 instance | `06-ebs-storage-server` |
| Instance type | `t3.micro` |
| Operating system | Amazon Linux 2023 |
| Region | `us-east-1` |
| Additional EBS volume | 10 GiB |
| Disk / partition | `/dev/nvme1n1` / `/dev/nvme1n1p1` |
| Filesystem | XFS |
| Mount point | `/data` |

Account IDs, IP addresses and credentials are left out of this project on purpose.

## The storage path
```text
EC2
 └── 10 GiB EBS volume
      └── /dev/nvme1n1
           └── /dev/nvme1n1p1
                └── XFS
                     └── /data
                          └── ebs-test.txt
```

## Project structure
```text
01 - project/
02 - documentation/
03 - screenshots/
```

## Commands I used
```bash
lsblk
sudo fdisk /dev/nvme1n1
sudo mkfs -t xfs /dev/nvme1n1p1
sudo mkdir /data
sudo mount /dev/nvme1n1p1 /data
df -h
sudo blkid /dev/nvme1n1p1
```

Inside `fdisk`, I typed these, one per line:
```text
n
p
1
Enter
Enter
w
```

Storage test:
```bash
sudo touch /data/ebs-test.txt
echo "Project 06 EBS storage is working." | sudo tee /data/ebs-test.txt
cat /data/ebs-test.txt
```

Persistent mount entry in `/etc/fstab`:
```text
UUID=<EBS_VOLUME_UUID> /data xfs defaults,nofail 0 2
```

Final check:
```bash
sudo umount /data
sudo mount -a
df -h /data
cat /data/ebs-test.txt
```

## What I did
1. Attached a 10 GiB EBS volume to the EC2 instance.
2. Connected to the instance and found the new disk with `lsblk`. It showed up separately from the root disk.
3. Created a primary partition with `fdisk`.
4. Formatted the partition with XFS.
5. Created the mount point `/data`.
6. Mounted the filesystem at `/data` and checked it with `df -h` and `lsblk`.
7. Created a test file and read it back.
8. Got the filesystem UUID with `blkid`.
9. Added the UUID entry to `/etc/fstab`.
10. Unmounted `/data`, ran `mount -a`, and checked that the test file was still there.
11. Organised the screenshots and wrote this documentation.

## Key ideas (in my own words)
- **EC2 vs EBS:** EC2 is the virtual server (compute). EBS is persistent block storage that I attach to it.
- **Block device:** a disk that Linux can see, for example `/dev/nvme1n1`.
- **Partition:** a section of a disk, for example `/dev/nvme1n1p1`.
- **Filesystem:** the structure that lets Linux store files. I used XFS.
- **Mount point:** the folder where I can reach the filesystem. Mine is `/data`.
- **UUID:** a stable ID for the filesystem. Device names like `/dev/nvme1n1` can change, so `/etc/fstab` uses the UUID.
- **`nofail`:** for extra, non-root storage, it makes the server less likely to fail to boot if that volume isn't available.
- **My workflow:** Attach → Detect → Partition → Format → Mount → Persist → Verify.

## Challenges
1. **`fdisk` said "Value out of range".** I typed `w` while `fdisk` was asking for the partition type. The answer to that prompt is `p` (primary). After that I used the defaults and finished with `w`.
2. **`/etc/fstab` parse error.** I got `mount: /etc/fstab: parse error` because my entry wasn't written correctly. An `fstab` entry needs six fields. I fixed the line and tested it with `sudo mount -a` before relying on it.

Lesson: always run `lsblk` before a disk command like `fdisk` or `mkfs`, and always test an `fstab` change with `mount -a`.

## Validation checklist
- [x] EBS volume attached
- [x] Disk detected with `lsblk`
- [x] Partition created
- [x] XFS filesystem created
- [x] `/data` mount point created
- [x] EBS volume mounted
- [x] Test file written and read back
- [x] UUID obtained
- [x] `/etc/fstab` configured
- [x] Persistent mount tested with `mount -a`
- [x] Screenshots captured (see `03 - screenshots/`)

## Notes
An EBS volume costs money while it exists, even when the instance is stopped, so I check my billing page and delete the volume and the instance when I'm finished. I'm still learning Linux storage and want to practice it more.

Documentation was written with AI assistance (Claude) for structure and clarity. I did the lab in the AWS Console myself and checked what is written here against what I did.
