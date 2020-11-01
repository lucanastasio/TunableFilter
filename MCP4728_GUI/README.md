## Usage

### Driver
Only tested on Arch Linux, actual configuration may vary on your system, don't follow our isntructions blindly, do it at your own risk.

A CP2112 USB to i2c adapter has been used, but newer kernels don't load `i2c-dev` module on boot, load it on purpose with `sudo modprobe i2c-dev` and then, for your convenience, `echo '12c-dev' | sudo tee /etc/modules-load.d/i2c-dev.conf` to load it on boot.

Add an i2c group with `sudo groupadd i2c` to use it as normal user, add yourself to that group with `sudo usermod -a $USER -G i2c` and make the group effective in the current shell with `newgrp i2c` to avoid having to log out and back in.

Create an udev rule to ensure permission to use the adapter with `echo 'KERNEL=="i2c-[0-9]*", GROUP="i2c", MODE="0660"' | sudo tee /etc/udev/rules.d/99-i2c-dev.rules` and plug the adapter, finally.
