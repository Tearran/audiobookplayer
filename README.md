# Introduction
 
This project uses a Pimoroni Pirate Audio HAT on a Raspberry Pi Zero to play audiobooks. It is written with Python and Tkinter. I run it in Openbox at startup. [Fbcp-ili9341](https://github.com/juj/fbcp-ili9341) shows HDMI output on the display. 

![player](/photos/player.png "player")

Components I used:

- Raspberry Pi zero
- SD-Card with Raspberry Pi OS with desktop, configured (especially I2C enabled, SPI disabled) and updated
- Pirate Audio Hat ( tested with Amp and Speaker)

### Python App Overview
The Tkinter App is quite simple. You can navigate in it with the four buttons of the Pirate Audio HAT. It needs python-vlc installed. For test purposes I configured the keys 'U'->A, 'J'->B, 'I'->X and 'K'->Y to use on a keyboard instead.

#### Play View
![playview](/photos/playview.png "playview")

#### Navi View
![naviview](/photos/naviview.png "naviview")

#### File View
![fileview](/photos/fileview.png "fileview")

#### Settings View
![settingsview1](/photos/settingsview_turnsleepoff_turnwifioff.png "settingsview1")
![settingsview2](/photos/settingsview_turnsleepon_turnwifioff.png "settingsview2")
![settingsview3](/photos/settingsview_turnsleepon_turnwifion.png "settingsview3")


### Installing FBCP-ILI9341 for Pirate Audio HAT
Follow the installation instructions for [fbcp-ili9341](https://github.com/juj/fbcp-ili9341/blob/master/README.md#installation)

I used the following cmake configuration:
```
cmake -DPIRATE_AUDIO_ST7789_HAT=ON -DSPI_BUS_CLOCK_DIVISOR=30 -DBACKLIGHT_CONTROL=ON -DUSE_DMA_TRANSFERS=OFF -DSTATISTICS=0 ..
```

I did not change any files in the main fbcp-ili9341 directory. The display is 90° rotated. I fixed that in /boot/config.txt (info from this [issue](https://github.com/juj/fbcp-ili9341/pull/203)):
```
display_rotate=1

hdmi_group=2
hdmi_mode=87
hdmi_cvt=240 240 60 1 0 0 0
hdmi_force_hotplug=1
```

while you are in /boot/config.txt turn audio off:
```
# Enable audio (loads snd_bcm2835)
dtparam=audio=off
```

and add:

```
dtoverlay=hifiberry-dac
gpio=25=op,dh
```

as is described [here](https://github.com/pimoroni/pirate-audio)

To autostart fbcp-ili9341 add `sudo /home/pi/fbcp-ili9341/build/fbcp-ili9341 &` to your `/etc/rc.local` file

### How to autostart an app with Openbox

- Configure Openbox to start program at boot:
```  
cd
cd .config
mkdir openbox
cd openbox
```

- create and edit file `autostart` and add
```
path/to/your/app &
```

in my case that is:
```
/home/pi/player.sh &
```

- run `sudo update-alternatives --config x-session-manager` and choose Openbox.

- I use raspi-config to start GUI at boot with autologin.

### Configure Openbox
In '~/.config/openbox/rc.xml' I added:
'''
<applications>
    <application class="*">
        <decor>no</decor>
    </application>
</applications>
'''
This removes all decorations, especially the top menu.