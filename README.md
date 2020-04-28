# BodyBreak
### Xilinx PYNQ-Z1 FPGA real time image processing game


<p align="center">
  <img src="https://github.com/RaphaelBijaoui/images/blob/master/BBlogo.png">
</p>
<p align="center">
    Watch the demo video <a href=https://drive.google.com/file/d/1r4Y0EkWBfWE3pWS-Mw4BluHcIIVYS1a-/preview> here! </a>
</p>

### Background
Body Break is a game that draws inspiration from blindfolded, hide-and-seek and code-breaking type games throughout history . The core design philosophy of the project was to develop an interactive game that encourages motion through rotation, contraction and extension of the joints and limbs, with the body transitioning between static and dynamic states as the player navigates towards the objective. Over the course of its development, Body Break has adhered to its underlying notion that as the user gets closer to the objective, the system informs the player that it is getting “warmer”, and “colder” otherwise. The aim of the game is simple: the players use their bodies to crack a code in the form of five different points on the screen... in a given timeframe. 

The current iteration of the system is able to detect and identify different colors that correspond to unique body parts, which for Body Break correspond to the head, wrists, and ankles around which a colored band (player marker) would be worn, as such achieving a functional positional tracking system for the player’s body. The system also can perform real-time image processing based on the positional values of the markers interpreted on an x-y coordinate system. These coordinates are translated to the heatmap, which is a real-time visual feedback in the forms of a full screen filter and marker-centered ring filter.

### Setting up
To start, you will need the following items:
- 1x Xilinx PYNQ-Z1 FPGA
- 2x HDMI Cable
- 1x HDMI compatible camera (for HDMI-IN). A HDMI compatible computer with webcam will work 
- 1x HDMI compatible monitor (for HDMI-OUT)
- 1x Computer

Clone project to your local machine
```
git clone https://github.com/RaphaelBijaoui/BodyBreak.git
```
Open up the Jupyter notebook body_break_v5(final).ipynb

Steps:
1. Link HDMI cable from PYNQ-Z1 board HDMI-IN to camera 
2. Link HDMI cable from monitor to HDMI-OUT
3. Connect computer to Pynq board via USB
4. Run Jupyter notebook
5. Follow in-game instructions on monitor
6. Wear your bands, break your body!

<p align="center">
  <img src="https://github.com/RaphaelBijaoui/images/blob/master/BBstartmenu.png">
</p>
<p align="center">
  <i>Start menu</i>
</p>

<p align="center">
  <img src="https://github.com/RaphaelBijaoui/images/blob/master/BBgameplay.png">
</p>
<p align="center">
  <i>Gameplay</i>
</p>

<p align="center">
  <img src="https://github.com/RaphaelBijaoui/images/blob/master/BBwinningpose.png">
</p>
<p align="center">
  <i>Demonstration of a winning pose!</i>
</p>



