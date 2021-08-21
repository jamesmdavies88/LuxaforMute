# Luxafor Mute for Linux

This Python script will allow you to use your Luxafor Mute button with Linux.  I have tested this with ```Ubuntu 21.04```

## Pre requisites

You will need to create a rule on your local machine before the script can be run, this allows your user access to the USB device.

Create a `luxafor.rules` file in `/etc/udev/rules.d/` containing:

``
SUBSYSTEM=="usb", ATTR{idVendor}=="04d8", ATTR{idProduct}=="f372" MODE="0664", OWNER="{Your user}"
``

Replace `{Your user}` with your Linux user.

Once this rule is in place you will need to run these commands to restart `udev`:

``
sudo udevadm control --reload
sudo udevadm trigger
``
