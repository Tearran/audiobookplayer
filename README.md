# Introduction
 
This project uses a Pimoroni Pirate Audio HAT on a Raspberry Pi Zero to play audiobooks. It is written in Python with Tkinter. I run it in Openbox at startup. [Fbcp-ili9341](https://github.com/juj/fbcp-ili9341) shows HDMI output on the display. 

![player](/photos/player.png "player")

### Info

The app is a work in progress and customized for our personal needs. When I started out with this project, I couldn't find any example code that incorporated all the parts I wanted to use into one project. Maybe this helps someone with their project.

### Components I used:

- Raspberry Pi zero
- SD-Card with Raspberry Pi OS with desktop, configured (especially I2C enabled, SPI disabled) and updated
- Pirate Audio Hat ( tested with Amp and Speaker)

## Python App Overview
The Tkinter App is quite simple. You can navigate with the four buttons of the Pirate Audio HAT. It needs python-vlc installed. For test purposes I configured the keys 'U'->A, 'J'->B, 'I'->X and 'K'->Y to use on a keyboard instead.

### Want to test it?
You will need:
- everything in the player folder.
- python-vlc installed (`pip install python-vlc`)
- run `python3 player/main.py`
- GPIO Pin for the Y button changed at some point from 20 to 24
you can change it in `player/constants.py`
- shutdown.sh, turnwifion.sh and turnwifioff.sh need to be owned by root and need to be executable

#### Play View
![playview](/photos/playview.png "playview")

- change volume **[A,B]**
- play/pause **[Y]**
- go to navi view **[X]**

#### Navi View
![naviview](/photos/naviview.png "naviview")

- restart audio book **[A]**
- chapter forward/backward **[B,Y]**
- go to file view **[X]**

#### File View
![fileview](/photos/fileview.png "fileview")

- left buttons navigate the directory structure **[A,B]**
- go to settings view **[X]**
- ok **[Y]** 
opens directory or if it is an mp3 or m4a open the file for playback

#### Settings View
![settingsview1](/photos/settingsview_turnsleepoff_turnwifioff_.png "settingsview1")

![settingsview2](/photos/settingsview_turnsleepon_turnwifion.png "settingsview2")

- turn sleep timer on/off **[A]**
if on, the player saves the current audiobook and position and shuts down the pi
default is 30min, change it in 'player/constants.py'
- go to play view **[B]**
- turn wifi on/off **[X]**
uses rfkill
- shutdown **[Y]**
save audiobook and position and shut down the pi


## Installing FBCP-ILI9341 for Pirate Audio HAT
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


## How to autostart an app with Openbox

- Configure Openbox to start program at boot:
```  
cd ~
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

```xml
<applications>
    <application class="*">
        <decor>no</decor>
    </application>
</applications>
```

This removes all decorations, especially the top menu.

### Problems with PIL
When I get
`ImportError: cannot import name 'ImageTk' from 'PIL'`
at startup, I delete the PIL and Pillow packages in the dist-packages folder and install Pillow with `pip install Pillow`.
