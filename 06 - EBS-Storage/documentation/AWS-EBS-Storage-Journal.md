# Project 06 — Project Journal

## Goal
Get hands-on experience with Amazon EBS by attaching an extra volume to an EC2 instance, preparing it in Linux, mounting it, testing it, and making the mount last after a reboot.

## Work completed
1. Attached a 10 GiB EBS volume to the Amazon Linux 2023 instance `06-ebs-storage-server`.
2. Found the new disk with `lsblk`. It appeared separately from the root disk.
3. Opened the disk with `sudo fdisk /dev/nvme1n1` and created a primary partition (`n`, `p`, `1`, Enter, Enter, `w`).
4. Formatted the partition with XFS: `sudo mkfs -t xfs /dev/nvme1n1p1`.
5. Created the mount point (`sudo mkdir /data`) and mounted the partition (`sudo mount /dev/nvme1n1p1 /data`).
6. Confirmed the roughly 10 GiB filesystem at `/data` with `df -h` and `lsblk`.
7. Created `ebs-test.txt` with the message "Project 06 EBS storage is working." and read it back with `cat`.
8. Got the UUID with `sudo blkid /dev/nvme1n1p1`.
9. Added `UUID=<EBS_VOLUME_UUID> /data xfs defaults,nofail 0 2` to `/etc/fstab`.
10. Ran `sudo umount /data`, `sudo mount -a`, `df -h /data` and `cat /data/ebs-test.txt` to check the result.

## What I learned
- EC2 is compute and EBS is persistent block storage.
- A new disk needs several steps before it's usable: detect, partition, format, mount.
- A block device or partition is not a filesystem until I format it.
- A disk command must target the right device, so I check with `lsblk` first.
- `/etc/fstab` controls what mounts at boot, and a UUID is a more stable ID than a device name.
- `nofail` helps a server boot even if an extra volume is missing.

## Issue and lesson
This project was challenging at first because it combined AWS concepts with Linux storage.

- **`fdisk` "Value out of range":** I typed `w` when `fdisk` was asking for the partition type. The right answer was `p`. After that I kept the defaults and wrote the changes with `w`.
- **`/etc/fstab` parse error:** my entry was malformed. I corrected it and tested it again with `sudo mount -a`.

Lesson: the workflow matters more than memorising every command. **Attach → Detect → Partition → Format → Mount → Persist → Verify.** When I know what each layer does, the commands are easier to remember.

## Mistakes to avoid (for my future projects)
- Running `fdisk` or `mkfs` on a device I haven't checked with `lsblk`.
- Typing `w` before `fdisk` has finished asking its questions.
- Rebooting before testing an `/etc/fstab` change with `mount -a`.
- Leaving an EBS volume or instance behind when I'm finished.

## Evidence
Screenshots of the attached volume, the running instance, the detected disk, the partition, the filesystem, the mounted and tested volume, and the `fstab` check (see `03 - screenshots/`).

## Outcome
I have an extra 10 GiB EBS volume mounted at `/data` that stays mounted through `/etc/fstab`, and my test file is still readable after unmounting and mounting again. I'm still a beginner with Linux storage. Next is Project 07: the Application Load Balancer.

## Cost reminder
An EBS volume and a running instance can cost money. I check my billing page and delete the volume and instance when I no longer need them.
