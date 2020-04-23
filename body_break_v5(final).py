
# coding: utf-8

# # EIE 1st Year Project - Body Break Version 5 (FINAL) 2019
# 
# This notebook demonstrates the interface between PYNQ's Processing Systems (PS) and a custom HLS hardware block integrated with PYNQ's base overlay for real-time Video Processing. It implements a Vertical-Edge detector capable of running in >30fps. 
# 
# This material can be used for academic purposes only. Any commerical use is prohibited. 
# 
# Contact: Alexandros Kouris (a.kouris16@imperial.ac.uk), Ph.D. Candidate, Imperial College London

# In[11]:


from pynq import Overlay, Xlnk
from pynq.overlays.base import BaseOverlay

allocator = Xlnk()

#Load customised version of Base-Overlay,that included the custom hardware block, instead of using BaseOverlay("base.bit")
#------------------------------------------------------------------------------------------------------------------------
#ol = Overlay("eie_v25.bit") #Grayscale, full-frame (33fps)
#ol = Overlay("eie_v25_2.bit") #Grayscale, half-frame (33fps)
ol = BaseOverlay("170519_plswork.bit") #Vertical Edge-Detector, half-frame (33fps)  - EIE2019


# In[12]:


from pynq.lib.video import *

hdmi_in = ol.video.hdmi_in
hdmi_out = ol.video.hdmi_out

hdmi_in.configure(PIXEL_RGBA)
hdmi_out.configure(hdmi_in.mode, PIXEL_RGBA)


# In[13]:


hdmi_in.start()
hdmi_out.start()


# In[14]:


from pynq import MMIO
#filter_reference = MMIO(0x00000000,0x10000)
filter_reference = MMIO(0x83C20000,0x10000)  #MMIO Addresses should always be double-checked when exporting a Vivado Design


# In[15]:


import time
import random
import cv2
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX
Delay1 = 0.3
Delay2 = 0.1
time_limit = 20
rgbled_position = [4, 5]
frame_w, frame_h = 1280, 720
win_condition = False
time_out = False
tolerance = 500
trial_set = [[640, 160], [440, 360], [840, 360], [740, 160], [540, 160]]
easy_set = [[[853, 561], [825, 213], [387, 283], [565, 547], [776, 84]],  # Pose 1
            [[932, 614], [864, 362], [486, 236], [1085, 465], [644, 149]]]     # Pose 4
hard_set = [[[745, 593], [1114, 212], [517, 206], [564, 443], [872, 125]],  # Pose 2
            [[876, 620], [1164, 182], [1055, 67], [964, 485], [942, 159]]]  # Pose 5

# solution = master_set[random.randint(0, len(master_set)-1)]
filter_reference.write(0x30, 0)
filter_reference.write(0x38, 0)
filter_reference.write(0x40, 0)
filter_reference.write(0x48, 0)
filter_reference.write(0x50, 0)
filter_reference.write(0x58, 0)
filter_reference.write(0x60, 0)
filter_reference.write(0x68, 0)
filter_reference.write(0x70, 0)
filter_reference.write(0x78, 0)

while (ol.buttons[3].read() == 0):
    color = 0
    for led in ol.leds:
        led.on()
    color = (color+7) % 8
    for led in rgbled_position:
        ol.rgbleds[led].write(color)
        ol.rgbleds[led].write(color)
        time.sleep(1)
    color = 0
    print("Choose a difficulty: Easy (BTN1) or Hard (BTN2) or Quit (BTN3)")
    in_frame = hdmi_in.readframe()
    out_frame = hdmi_out.newframe()
    frame_copy = out_frame.copy()
    cv2.rectangle(frame_copy, (0, 0),  (frame_w, frame_h), (0, 0, 255), -1)
    cv2.addWeighted(frame_copy, 1, out_frame, 0, 0, out_frame)
    cv2.putText(out_frame, "BODY BREAK", (100, 260), font, 3, (255, 0, 255), 4, cv2.LINE_AA)
    cv2.putText(out_frame, "< 1 - EASY >  < 2 - HARD >  < 3 - QUIT >", (100, 460), font, 1, (255, 0, 255), 4, cv2.LINE_AA)
    hdmi_out.writeframe(out_frame)

    while ((ol.buttons[1].read() == 0) and (ol.buttons[2].read() == 0) and (ol.buttons[3].read() == 0)):
        pass
    # Premature quit
    if (ol.buttons[3].read() == 1):
        break
    # Mode selection
    if (ol.buttons[1].read() == 1):
            print("Selected difficulty: Easy")
            color = (color+2) % 8
            for led in rgbled_position:
                ol.rgbleds[led].write(color)
                ol.rgbleds[led].write(color)
#             solution = easy_set[random.randint(0, len(easy_set)-1)]
            solution = easy_set[0]
            time.sleep(Delay1)

    elif (ol.buttons[2].read() == 1):
        print("Selected difficulty: Hard")
        color = (color+4) % 8
        for led in rgbled_position:
            ol.rgbleds[led].write(color)
            ol.rgbleds[led].write(color)
        solution = hard_set[random.randint(0, len(hard_set)-1)]
        time.sleep(Delay1)
    time.sleep(Delay1)
    # Playing game
    print("Game start")
    frames = 0
    start = time.time()
    while (ol.buttons[0].read() == 0 and ol.buttons[3].read() == 0):
        in_frame = hdmi_in.readframe()
        out_frame = hdmi_out.newframe()
        # Display solution on screen
#         cv2.circle(out_frame, (solution[0][0], solution[0][1]), 5, (0, 0, 255), -1)
#         cv2.circle(out_frame, (solution[1][0], solution[1][1]), 5, (255, 165, 0), -1)
#         cv2.circle(out_frame, (solution[2][0], solution[2][1]), 5, (255, 0, 255), -1)
#         cv2.circle(out_frame, (solution[3][0], solution[3][1]), 5, (0, 255, 0), -1)
#         cv2.circle(out_frame, (solution[4][0], solution[4][1]), 5, (255, 255, 0), -1)
#         cv2.circle(out_frame, (solution[0][0], solution[0][1]), 5, (0, 0, 0), -1)
#         cv2.circle(out_frame, (solution[1][0], solution[1][1]), 5, (0, 0, 0), -1)
#         cv2.circle(out_frame, (solution[2][0], solution[2][1]), 5, (0, 0, 0), -1)
#         cv2.circle(out_frame, (solution[3][0], solution[3][1]), 5, (0, 0, 0), -1)
#         cv2.circle(out_frame, (solution[4][0], solution[4][1]), 5, (0, 0, 0), -1)

        # Get Pointers to memory
        filter_reference.write(0x10, in_frame.physical_address)  # in_data
        filter_reference.write(0x18, out_frame.physical_address)  # out_data
    #     filter_reference.write(0x20, frame_w)   # Make sure that the input HDMI signal is set to 1280x720
    #     filter_reference.write(0x28, frame_h)
        filter_reference.write(0x00, 0x01)             # ap_start triggering
        while (filter_reference.read(0) & 0x4) == 0:   # ap_done checking
            pass
        if win_condition or time_out:
            hdmi_out.writeframe(out_frame)
            break

        ### DISTANCE CALCULATIONS ###
        # Yellow
        hd_x = filter_reference.read(0x30)
        hd_y = filter_reference.read(0x38)
        # Orange
        rh_x = filter_reference.read(0x40)
        rh_y = filter_reference.read(0x48)
        # Pink
        lh_x = filter_reference.read(0x50)
        lh_y = filter_reference.read(0x58)
        # Green
        rf_x = filter_reference.read(0x60)
        rf_y = filter_reference.read(0x68)
        # Blue
        lf_x = filter_reference.read(0x70)
        lf_y = filter_reference.read(0x78)

        hd_dist = np.sqrt((hd_x-solution[0][0])*(hd_x-solution[0][0]) + (hd_y-solution[0][1])*(hd_y-solution[0][1]))
        rh_dist = np.sqrt((rh_x-solution[1][0])*(rh_x-solution[1][0]) + (rh_y-solution[1][1])*(rh_y-solution[1][1]))
        lh_dist = np.sqrt((lh_x-solution[2][0])*(lh_x-solution[2][0]) + (lh_y-solution[2][1])*(lh_y-solution[2][1]))
        rf_dist = np.sqrt((rf_x-solution[3][0])*(rf_x-solution[3][0]) + (rf_y-solution[3][1])*(rf_y-solution[3][1]))
        lf_dist = np.sqrt((lf_x-solution[4][0])*(lf_x-solution[4][0]) + (lf_y-solution[4][1])*(lf_y-solution[4][1]))

        # Ring filter
        hd_r = int(hd_dist/3)
        cv2.circle(out_frame, (hd_x, hd_y), hd_r, (0, 0, 255), 2)  # Head, yellow
        rh_r = int(rh_dist/3)
        cv2.circle(out_frame, (rh_x, rh_y), rh_r, (255, 165, 0), 2)  # Right hand, orange
        lh_r = int(lh_dist/3)
        cv2.circle(out_frame, (lh_x, lh_y), lh_r, (255, 0, 255), 2)  # Left hand, pink
        rf_r = int(rf_dist/3)
        cv2.circle(out_frame, (rf_x, rf_y), rf_r, (0, 255, 0), 2)  # Right foot, green
        lf_r = int(lf_dist/3)
        cv2.circle(out_frame, (lf_x, lf_y), lf_r, (255, 255, 0), 2)  # Left foot, blue

        # Timer
        time_now = time.time()
        time_passed = time_now-start
        cv2.putText(out_frame, "TIME LEFT: {}s".format(int(
            time_limit - time_passed)), (900, 100), font, 1, (255, 0, 255), 3, cv2.LINE_AA)
        if time_passed >= time_limit:
            time_out = True

        ### CHECK WIN CONDITION ###
        if (lh_dist <= tolerance) and (rf_dist <= tolerance) and (hd_dist <= tolerance) and (rh_dist <= tolerance) and (lf_dist <= tolerance):
            win_condition = True

        ### VISUAL FEEDBACK OVERLAY ###
#         cv2.putText(out_frame, "hd_dist={}".format(int(hd_dist)), (70, 500), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(out_frame, "rh_dist={}".format(int(rh_dist)), (70, 550), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(out_frame, "lh_dist={}".format(int(lh_dist)), (70, 600), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(out_frame, "rf_dist={}".format(int(rf_dist)), (70, 650), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(out_frame, "lf_dist={}".format(int(lf_dist)), (70, 450), font, 1, (0, 0, 0), 1, cv2.LINE_AA)

        #############################
        hdmi_out.writeframe(out_frame)
        frames += 1

    end = time.time()

    if (ol.buttons[3].read() == 1):
        break
    elif (win_condition):
        cv2.putText(out_frame, "BODY", (200, 150), font,
                    4, (255, 0, 255), 10, cv2.LINE_AA)
        cv2.putText(out_frame, "BROKEN", (150, 600), font,
                    4, (255, 0, 255), 10, cv2.LINE_AA)
        print("Game won")
        for _ in range(10):
            for led in ol.leds:
                led.toggle()
                time.sleep(0.2)
        win_condition = time_out = False
        time_passed = time_now = 0
        cv2.putText(out_frame, "< 0 - MAIN MENU >  < 3 - QUIT >", (300, 460), font, 1, (255, 0, 255), 4, cv2.LINE_AA)
        while ((ol.buttons[0].read() == 0) and (ol.buttons[3].read() == 0)):
            pass
        if ol.buttons[3].read():
            break

    elif (time_out):
        cv2.putText(out_frame, "TIME OUT", (100, 360),
                    font, 8, (255, 0, 255), 10, cv2.LINE_AA)
        print("Time out")
        for _ in range(10):
            for led in ol.leds:
                led.toggle()
                time.sleep(0.2)
        win_condition = time_out = False
        time_passed = time_now = 0
        cv2.putText(out_frame, "< 0 - MAIN MENU >  < 3 - QUIT >", (300, 460), font, 1, (255, 0, 255), 4, cv2.LINE_AA)
        while ((ol.buttons[0].read() == 0) and (ol.buttons[3].read() == 0)):
            pass
        if ol.buttons[3].read():
            break

    elif (ol.buttons[0].read() == 1):
        print("Restarting game")
        for led in ol.leds:
            led.off()
        time.sleep(0.1)
        for led in ol.leds:
            led.toggle()
            time.sleep(0.1)
        win_condition = time_out = False
        time_passed = time_now = 0

    print(f"{frames} frames took {end-start} seconds at {frames/(end-start)} fps")


print("Quitting game")
for led in ol.leds:
    led.off()
for led in rgbled_position:
    ol.rgbleds[led].off()
hdmi_in.close()    # Don't forget to run this to free memory
hdmi_out.close()   # NEVERFORGET NEVERFORGET NEVERFORGET :p 
print("HDMI Released")

