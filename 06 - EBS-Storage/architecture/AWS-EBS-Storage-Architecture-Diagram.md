# Project 06 — Architecture

```
   Me (browser)
        |
        | connect to the instance
        v
+--------------------------------------------------+
| EC2 instance: 06-ebs-storage-server              |
| t3.micro, Amazon Linux 2023, us-east-1           |
|                                                  |
|   Root volume (operating system)                 |
|                                                  |
|   Additional EBS volume: 10 GiB                  |
|        |                                         |
|        v                                         |
|   Block device   /dev/nvme1n1                    |
|        |                                         |
|        v                                         |
|   Partition      /dev/nvme1n1p1   (fdisk)        |
|        |                                         |
|        v                                         |
|   Filesystem     XFS              (mkfs)         |
|        |                                         |
|        v                                         |
|   Mount point    /data            (mount)        |
|        |                                         |
|        v                                         |
|   Test file      /data/ebs-test.txt              |
|                                                  |
|   /etc/fstab: UUID=<EBS\_VOLUME\_UUID> /data       |
|               xfs defaults,nofail 0 2            |
|               (mounts /data again after reboot)  |
+--------------------------------------------------+

Workflow: Attach -> Detect -> Partition -> Format -> Mount -> Persist -> Verify
```

