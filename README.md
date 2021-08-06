# Introduction
 
This project uses a Pimoroni Pirate Audio HAT on a Raspberry Pi Zero to play audiobooks. It is written in Python with Tkinter. I run it in Openbox at startup. [Fbcp-ili9341](https://github.com/juj/fbcp-ili9341) shows HDMI output on the display. 

![photo of Pirate Audio HAT on a Raspberry Pi Zero. The app is running with play view visible.](/photos/player.png "player")

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
![Screenshot of play view. Icons louder and quieter on the left. "Go to chapter view" and playpause buttons on the right.](/photos/playview.png "playview")

- **[A,B]** change volume
- **[X]** go to chapter view
- **[Y]** play/pause

#### Chapter View
![Screenshot of navi view. Chapter list is in the middle, scroll up or down icons on the left. "Go to file view" and ok icon on the right.](/photos/chapterview.png "chapterview")

- **[A]** restart audio book
- **[B,Y]** chapter forward/backward
- **[X]** go to file view

#### File View
![Screenshot of file view. List of files in current directory in the middle. On the left scroll up and down icons. "Go to settings view" and ok icon the right.](/photos/fileview.png "fileview")

- **[A,B]** left buttons navigate the directory structure
- **[X]** go to settings view
- **[Y]** ok: opens directory or if it is an mp3 or m4a open the file for playback

#### Settings View
![Screenshot of settings view 1. On the left is turn sleep timer off and turn wifi off. On the right is icon "go to play view" and shutdown](/photos/settingsview_turnsleepoff_turnwifioff_.png "settingsview1")

![Screenshot of settings view 2. On the left is turn sleep timer on and turn wifi on. On the right is icon "go to play view" and shutdown](/photos/settingsview_turnsleepon_turnwifion.png "settingsview2")

- **[A]** turn sleep timer on/off
if on, the player saves the current audiobook and position and shuts down the pi
default is 30min, change it in 'player/constants.py'
- **[B]** go to play view
- **[X]** turn wifi on/off
uses rfkill
- **[Y]** shutdown
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

## Problems with PIL
When I get
`ImportError: cannot import name 'ImageTk' from 'PIL'`
at startup, I delete the PIL and Pillow packages in the dist-packages folder and install Pillow with `pip install Pillow`.
