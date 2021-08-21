from array import array
import usb.core
import usb.util
import os


def main():
    dev = usb.core.find(idVendor=0x04D8, idProduct=0xF372)

    if dev is None:
        print("Luxafor Mute is not connected")
        return
    try:
        dev.detach_kernel_driver(0)
    except usb.core.USBError:
        pass
    try:
        dev.set_configuration()
    except usb.core.USBError:
        print(
            "If you receive this error, it is likely you haven't configured the rule for the Luxafor device"
        )
        return
    dev.set_configuration()
    while True:
        data = dev.read(0x81, 0x8, 0)

        if data == array("B", [131, 1, 0, 0, 0, 0, 0, 0]):
            # Run pactl list and grep by input to find your microphone source, mine is 2 - yours could be different
            # The command bellow toggles the mute flag
            os.system("pactl set-source-mute 2 toggle")
            # This command gets the mute status of all devices, finds the final mute in the output and uses this to
            # figure out the current mute status of the microphone
            mute = os.popen("pacmd list-sources | grep -e 'index: 2' -e muted | tail -1").read()

            # Just a bit of logic to handle the colour of the light dependant on mute status
            # This part of the write command contains 8 bytes of data:
            # [1, 1, 255, 0, 0, 0, 0, 0]
            # Byte 1: Always set to 1 (Think this means solid colour)
            # Byte 2: Value is set as 1-6 for each LED in the device
            # Byte 3-5: RGB value for the colour you want to select
            # Byte 6-8: Not sure what these are for, likely to be flash patterns etc

            if "muted: yes" in mute:
                dev.write(1, [1, 1, 255, 0, 0, 0, 0, 0])
                dev.write(1, [1, 2, 255, 0, 0, 0, 0, 0])
                dev.write(1, [1, 3, 255, 0, 0, 0, 0, 0])
                dev.write(1, [1, 4, 255, 0, 0, 0, 0, 0])
                dev.write(1, [1, 5, 255, 0, 0, 0, 0, 0])
                dev.write(1, [1, 6, 255, 0, 0, 0, 0, 0])
            elif "muted: no" in mute:
                dev.write(1, [1, 1, 0, 128, 0, 0, 0, 0])
                dev.write(1, [1, 2, 0, 128, 0, 0, 0, 0])
                dev.write(1, [1, 3, 0, 128, 0, 0, 0, 0])
                dev.write(1, [1, 4, 0, 128, 0, 0, 0, 0])
                dev.write(1, [1, 5, 0, 128, 0, 0, 0, 0])
                dev.write(1, [1, 6, 0, 128, 0, 0, 0, 0])


if __name__ == "__main__":
    main()
