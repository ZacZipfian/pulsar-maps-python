import psrqpy
from math import *
import numpy as np
from PIL import Image, ImageDraw

p_defult =['J1731-4744', 'J1456-6843', 'J1243-6423', 'J0835-4510', 'J0953+0755', 'J0826+2637', 'J0534+2200', 'J0528+2200',
        'J0332+5434', 'J2219+4754', 'J2018+2839', 'J1935+1616', 'J1932+1059', 'J1645-0317']

def PulsarMap(pulsars = p_defult, width = 1600, height = 1000, m_point = (500, 550), gc_len = 1000, line_width = 2, line_colour = 'black', 
              tick_len = 6, tick_colour = 'black', bc_colour = 'white'):
    # fix (need even int tick length)
    if tick_len % 2 != 0:
        tick_len = round(tick_len + 1)

    # query ATNF database, make table 
    q = psrqpy.QueryATNF(params=['JName', 'PosEpoch', 'P0', 'Dist', 'ZZ', 'XX', 'YY'], psrs=pulsars)
    t = q.table

    # Calculate vector of basic angles for puslars from the sun (helios)
    heilos = [-8.5, 0] #sun
    #origin = [0, 0] #GC
    a_dist = 8.5
    angle_vec = np.zeros(len(pulsars), dtype=float)
    for i in range(len(t['XX'])):
        b_dist = sqrt((t['XX'][i])**2 + (t['YY'][i])**2)
        c_dist = sqrt((t['XX'][i]- heilos[0])**2 + (t['YY'][i] - heilos[1])**2)
        angle = acos((1/(2*a_dist*c_dist))*(a_dist**2 + c_dist**2 - b_dist**2))
        angle_vec[i] = angle

    # Draw Pulsar map using straight lines on a canvas
    img = Image.new('RGB', (width, height), bc_colour)
    draw = ImageDraw.Draw(img)
    end_point = (m_point[0] + gc_len, m_point[1]) # set gc line (gc = galactic center)
    draw.line([m_point, end_point], fill=line_colour, width=line_width)

    # Draw binary and z-axis indicators
    draw.line([(end_point[0],m_point[1]-(tick_len/2)),(end_point[0],m_point[1]+(tick_len/2))], fill=line_colour, width=line_width)

    # Fix angles and plot
    for j in range(len(angle_vec)):
        ratio_dist = t['DIST'][j]/a_dist
        angle = angle_vec[j]
        if t['YY'][j] < 0:
            if t['XX'][j] < -8.5:
                angle -= 2*pi
                angle = angle*-1
            else:
                angle -= 2*pi
                angle = angle*-1
        angle = angle*-1   
        # lines
        draw.line([m_point,(round(m_point[0] + (gc_len*ratio_dist*cos(angle))), round(m_point[1] + (gc_len*ratio_dist*sin(angle))))],
                   fill=line_colour, width=line_width)   
        # z-axis indicators
        zz_new = abs(t['ZZ'][j]/a_dist)*ratio_dist*gc_len
        c_len = sqrt(((gc_len*ratio_dist)-zz_new)**2 + (tick_len/2)**2)
        alpha = asin((tick_len/2)/c_len)
        draw.line([(round(m_point[0] + (c_len*cos(angle-alpha))), round(m_point[1] + (c_len*sin(angle-alpha)))),
                   (round(m_point[0] + (c_len*cos(angle+alpha))), round(m_point[1] + (c_len*sin(angle+alpha))))], fill=line_colour, width=line_width)
        # binary encoding
        # constants
        HTH = 1420405751.7682 # hyperfine transition of hydrogen (Hz) (from Wikipedia)
        HTH_s = 1/HTH # seconds
        b10_val = t['P0'][j] / HTH_s 
        b2_val = bin(round(b10_val))[2:] # binary sequence
        # plot
        add_len = tick_len + 4
        for char in b2_val:
            if char == '1':
                # calculate angle
                c2_len = sqrt(((gc_len*ratio_dist) + add_len)**2 + (tick_len/2)**2)
                alpha2 = asin((tick_len/2)/c2_len)
                draw.line([(round(m_point[0] + (c2_len*cos(angle-alpha2))), round(m_point[1] + (c2_len*sin(angle-alpha2)))),
                           (round(m_point[0] + (c2_len*cos(angle+alpha2))), round(m_point[1] + (c2_len*sin(angle+alpha2))))], fill=tick_colour, width=line_width)
                add_len += line_width + (tick_len/2)
            else:
                c3_len = (gc_len*ratio_dist) + add_len + tick_len
                c4_len = (gc_len*ratio_dist) + add_len
                draw.line([(round(m_point[0] + (c4_len*cos(angle))), round(m_point[1] + (c4_len*sin(angle)))),
                           (round(m_point[0] + (c3_len*cos(angle))), round(m_point[1] + (c3_len*sin(angle))))], fill=tick_colour, width=line_width)
                add_len += tick_len + 4

    return img