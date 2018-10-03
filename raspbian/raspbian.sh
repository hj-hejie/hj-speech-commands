mount -v -o offset = 70254592 -t ext4 ~/qemu_vms/<your-img-file.img> /mnt/raspbian
qemu-system-arm -M ?
qemu-system-arm -kernel kernel-qemu-4.9.59-stretch -cpu arm1176 -m 256 -M versatilepb -dtb versatile-pb.dtb -no-reboot -append "root=/dev/sda2 panic=1 rootfstype=ext4 rw" -net nic -net user,hostfwd=tcp::5022-:22 -hda 2017-11-29-raspbian-stretch.img  -hdb ../sda3/raspbian/img.img

qemu-system-arm -kernel kernel-qemu-4.9.59-stretch -cpu arm1176 -m 256 -M versatilepb -dtb versatile-pb.dtb -no-reboot -append "root=/dev/sda2 panic=1 rootfstype=ext4 rw" -net nic -net user,hostfwd=tcp::5022-:22 -hda 2017-11-29-raspbian-stretch.img  -hdb ../sda3/raspbian/img.img

qemu-system-arm -m 2048M -M vexpress-a15 -cpu cortex-a15 -kernel ./kernel-qemu-4.4.1-vexpress -dtb ./vexpress-v2p-ca15_a7.dtb -sd ../sda3/raspbian/2017-11-29-raspbian-stretch.img -append "root=/dev/mmcblk0p2 rootwait" -net nic -net user,hostfwd=tcp::5022-:22
