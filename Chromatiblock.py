#!/usr/bin/env python
# easyFig.py   Written by: Mitchell Sullivan   mjsull@gmail.com
# Supervisor: Dr. Scott Beatson and Dr. Nico Petty University of Queensland
# Version 2.2.3 08.11.2016
# License: GPLv3

import os
import subprocess
from math import ceil, hypot
import threading
import time
import struct
import base64
import string
from ftplib import FTP
import tarfile
import platform
import shutil
import webbrowser
import operator
import sys
import argparse
from itertools import groupby

def colorstr(rgb): return "#%02x%02x%02x" % (rgb[0],rgb[1],rgb[2])


color_list = [(240,163,255),(0,117,220),(153,63,0),(76,0,92),(25,25,25),(0,92,49),(43,206,72),(255,204,153),(128,128,128),(148,255,181),(143,124,0),(157,204,0),(194,0,136),(0,51,128),(255,164,5),(255,168,187),(66,102,0),(255,0,16),(94,241,242),(0,153,143),(224,255,102),(116,10,255),(153,0,0),(255,255,128),(255,255,0),(255,80,5)]
#pattern_list = ['circ_small', 'circ_large', 'diag_small', 'diag_large', 'dots_small', 'dots_large', 'horiz_small', 'horiz_large', 'vert_small', 'vert_large', 'cross_hatch']
pattern_list = ['horizontal', 'forward_diag', 'reverse_diag']


def hsl_to_rgb(h, s, l):
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs(h *1.0 / 60 % 2 - 1))
    m = l - c/2
    if h < 60:
        r, g, b = c + m, x + m, 0 + m
    elif h < 120:
        r, g, b = x + m, c+ m, 0 + m
    elif h < 180:
        r, g, b = 0 + m, c + m, x + m
    elif h < 240:
        r, g, b, = 0 + m, x + m, c + m
    elif h < 300:
        r, g, b, = x + m, 0 + m, c + m
    else:
        r, g, b, = c + m, 0 + m, x + m
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return (r,g,b)

def binar(s):
  transdict = {'0':'0000',
               '1':'0001',
               '2':'0010',
               '3':'0011',
               '4':'0100',
               '5':'0101',
               '6':'0110',
               '7':'0111',
               '8':'1000',
               '9':'1001',
               'a':'1010',
               'b':'1011',
               'c':'1100',
               'd':'1101',
               'e':'1110',
               'f':'1111'
  }
  outstring = ''
  for i in s:
    outstring += transdict[i]
  return outstring

class scalableVectorGraphics:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.out = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   height="%d"
   width="%d"
   id="svg2"
   version="1.1"
   inkscape:version="0.48.4 r9939"
   sodipodi:docname="easyfig">
  <metadata
     id="metadata122">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title>Easyfig</dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <defs
     id="defs120" />
  <sodipodi:namedview
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1"
     objecttolerance="10"
     gridtolerance="10"
     guidetolerance="10"
     inkscape:pageopacity="0"
     inkscape:pageshadow="2"
     inkscape:window-width="640"
     inkscape:window-height="480"
     id="namedview118"
     showgrid="false"
     inkscape:zoom="0.0584"
     inkscape:cx="2500"
     inkscape:cy="75.5"
     inkscape:window-x="55"
     inkscape:window-y="34"
     inkscape:window-maximized="0"
     inkscape:current-layer="svg2" />
  <title
     id="title4">Easyfig</title>
  <g
     style="fill-opacity:1.0; stroke:black; stroke-width:1;"
     id="g6">''' % (self.height, self.width)

    def drawLine(self, x1, y1, x2, y2, th=1, cl=(0, 0, 0)):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n        stroke-width="%d" stroke="%s" />\n' % (x1, y1, x2, y2, th, colorstr(cl))

    def writesvg(self, filename):
        outfile = open(filename, 'w')
        outfile.write(self.out + ' </g>\n</svg>')
        outfile.close()

    def drawRightArrow(self, x, y, wid, ht, fc, oc=(0,0,0), lt=1):
        if lt > ht /2:
            lt = ht/2
        x1 = x + wid
        y1 = y + ht/2
        x2 = x + wid - ht / 2
        ht -= 1
        if wid > ht/2:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x, y+ht/4, x2, y+ht/4,
                                                                                                x2, y, x1, y1, x2, y+ht,
                                                                                                x2, y+3*ht/4, x, y+3*ht/4)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x, y, x, y+ht, x + wid, y1)

    def drawLeftArrow(self, x, y, wid, ht, fc, oc=(0,0,0), lt=1):
        if lt > ht /2:
            lt = ht/2
        x1 = x + wid
        y1 = y + ht/2
        x2 = x + ht / 2
        ht -= 1
        if wid > ht/2:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y+ht/4, x2, y+ht/4,
                                                                                                x2, y, x, y1, x2, y+ht,
                                                                                                x2, y+3*ht/4, x1, y+3*ht/4)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x, y1, x1, y+ht, x1, y)

    def drawBlastHit(self, x1, y1, x2, y2, x3, y3, x4, y4, fill=(0, 0, 255), lt=0):
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr(fill), lt)
        self.out += '           points="%d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y2, x3, y3, x4, y4)

    def drawGradient(self, x1, y1, wid, hei, minc, maxc):
        self.out += '  <defs>\n    <linearGradient id="MyGradient" x1="0%" y1="0%" x2="0%" y2="100%">\n'
        self.out += '      <stop offset="0%%" stop-color="%s" />\n' % colorstr(maxc)
        self.out += '      <stop offset="100%%" stop-color="%s" />\n' % colorstr(minc)
        self.out += '    </linearGradient>\n  </defs>\n'
        self.out += '  <rect fill="url(#MyGradient)" stroke-width="0"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d"/>\n' % (x1, y1, wid, hei)

    def drawGradient2(self, x1, y1, wid, hei, minc, maxc):
        self.out += '  <defs>\n    <linearGradient id="MyGradient2" x1="0%" y1="0%" x2="0%" y2="100%">\n'
        self.out += '      <stop offset="0%%" stop-color="%s" />\n' % colorstr(maxc)
        self.out += '      <stop offset="100%%" stop-color="%s" />\n' % colorstr(minc)
        self.out += '    </linearGradient>\n</defs>\n'
        self.out += '  <rect fill="url(#MyGradient2)" stroke-width="0"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)
    def drawHueGradient(self, x1, y1, wid, hei, s, l):
        self.out += '  <defs>\n    <linearGradient id="HueGradient" x1="0%" y1="0%" x2="100%" y2="0%">\n'
        iterations = 20
        for i in range(iterations):
            color = hsl_to_rgb(360/iterations * i, s, l)
            colorstring = colorstr(color)
            self.out += '      <stop offset="%d%%" stop-color="%s" />\n' % (100/iterations * i, colorstring)
            color = hsl_to_rgb(360/iterations * (i + 1), s, l)
            colorstring = colorstr(color)
            self.out += '      <stop offset="%d%%" stop-color="%s" />\n' % (100/iterations * (i + 1), colorstring)
        self.out += '    </linearGradient>\n</defs>\n'
        self.out += '  <rect fill="url(#HueGradient)" stroke-width="1"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawOutRect(self, x1, y1, wid, hei, fill, outfill, lt=1, alpha=1.0, alpha2=1.0):
        self.out += '  <rect stroke="%s" stroke-width="%d" stroke-opacity="%f" stroke-alignment="inner"\n' % (colorstr(outfill), lt, alpha)
        self.out += '        fill="%s" fill-opacity="%f"\n' % (colorstr(fill), alpha2)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def create_pattern(self, id, fill, pattern, width, line_width):
        fill = colorstr(fill)
        if pattern == 'horizontal':
            self.out += '    <defs>\n'
            self.out += '      <pattern id="%s" width="%d" height="%d" patternUnits="userSpaceOnUse">\n' % (id, width, width)
            self.out += '        <line x1="0" y1="0" x2="%d" y2="0" style="stroke:%s; stroke-width:%d; fill:#FFFFFF" />\n' % (width, fill, line_width)
            self.out += '      </pattern>\n'
            self.out += '   </defs>\n'
        elif pattern == 'forward_diag':
            self.out += '    <defs>\n'
            self.out += '      <pattern id="%s" width="%d" height="%d" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">\n' % (id, width, width)
            self.out += '        <line x1="0" y1="0" x2="0" y2="%d" style="stroke:%s; stroke-width:%d; fill:#FFFFFF" />\n' % (width, fill, line_width)
            self.out += '      </pattern>\n'
            self.out += '   </defs>\n'
        elif pattern == 'reverse_diag':
            self.out += '    <defs>\n'
            self.out += '      <pattern id="%s" width="%d" height="%d" patternTransform="rotate(135 0 0)" patternUnits="userSpaceOnUse">\n' % (id, width, width)
            self.out += '        <line x1="0" y1="0" x2="0" y2="%d" style="stroke:%s; stroke-width:%d; fill:#FFFFFF" />\n' % (width, fill, line_width)
            self.out += '      </pattern>\n'
            self.out += '   </defs>\n'

    def drawPatternRect(self, x, y, width, height, id, fill, lt):
        fill = colorstr(fill)
        self.out += '  <rect style="fill:#FFFFFF; stroke: %s; stroke-width: %d; stroke-alignment: inner;"\n' % (fill, lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x, y, width, height)
        self.out += '  <rect style="fill:url(#%s); stroke: %s; stroke-width: %d; stroke-alignment: inner;"\n' % (id, fill, lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x, y, width, height)

    def drawRightFrame(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht/2
            y2 = y + ht * 3/8
            y3 = y + ht * 1/4
        elif frame == 2:
            y1 = y + ht * 3/8
            y2 = y + ht * 1/4
            y3 = y + ht * 1/8
        elif frame == 0:
            y1 = y + ht * 1/4
            y2 = y + ht * 1/8
            y3 = y + 1
        x1 = x
        x2 = x + wid - ht/8
        x3 = x + wid
        if wid > ht/8:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y1, x3, y2, x2, y3, x1, y3)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y1, x3, y2, x1, y3)

    def drawRightFrameRect(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht / 4
        elif frame == 2:
            y1 = y + ht /8
        elif frame == 0:
            y1 = y + 1
        hei = ht /4
        x1 = x
        self.out += '  <rect fill="%s" stroke-width="%d"\n' % (colorstr(fill), lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawLeftFrame(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht
            y2 = y + ht * 7/8
            y3 = y + ht * 3/4
        elif frame == 2:
            y1 = y + ht * 7/8
            y2 = y + ht * 3/4
            y3 = y + ht * 5/8
        elif frame == 0:
            y1 = y + ht * 3/4
            y2 = y + ht * 5/8
            y3 = y + ht / 2
        x1 = x + wid
        x2 = x + ht/8
        x3 = x
        if wid > ht/8:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y1, x3, y2, x2, y3, x1, y3)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y1, x3, y2, x1, y3)

    def drawLeftFrameRect(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht * 3/4
        elif frame == 2:
            y1 = y + ht * 5/8
        elif frame == 0:
            y1 = y + ht / 2
        hei = ht /4
        x1 = x
        self.out += '  <rect fill="%s" stroke-width="%d"\n' % (colorstr(fill), lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawPointer(self, x, y, ht, lt, fill):
        x1 = x - int(round(0.577350269 * ht/2))
        x2 = x + int(round(0.577350269 * ht/2))
        y1 = y + ht/2
        y2 = y + 1
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
        self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y2, x2, y2, x, y1)

    def drawDash(self, x1, y1, x2, y2, exont):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n' % (x1, y1, x2, y2)
        self.out += '       style="stroke-dasharray: 5, 3, 9, 3"\n'
        self.out += '       stroke="#000" stroke-width="%d" />\n' % exont

    def writeString(self, thestring, x, y, size, ital=False, bold=False, rotate=0, justify='left'):
        if rotate != 0:
            x, y = y, x
        self.out += '  <text\n'
        self.out += '    style="font-size:%dpx;font-style:normal;font-weight:normal;z-index:10\
;line-height:125%%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans"\n' % size
        if justify == 'right':
            self.out += '    text-anchor="end"\n'
        elif justify == 'middle':
            self.out += '    text-anchor="middle"\n'
        if rotate == 1:
            self.out += '    x="-%d"\n' % x
        else:
            self.out += '    x="%d"\n' % x
        if rotate == -1:
            self.out += '    y="-%d"\n' % y
        else:
            self.out += '    y="%d"\n' % y
        self.out += '    sodipodi:linespacing="125%"'
        if rotate == -1:
            self.out += '\n    transform="matrix(0,1,-1,0,0,0)"'
        if rotate == 1:
            self.out += '\n    transform="matrix(0,-1,1,0,0,0)"'
        self.out += '><tspan\n      sodipodi:role="line"\n'
        if rotate == 1:
            self.out += '      x="-%d"\n' % x
        else:
            self.out += '      x="%d"\n' % x
        if rotate == -1:
            self.out += '      y="-%d"' % y
        else:
            self.out += '      y="%d"' % y
        if ital and bold:
            self.out += '\nstyle="font-style:italic;font-weight:bold"'
        elif ital:
            self.out += '\nstyle="font-style:italic"'
        elif bold:
            self.out += '\nstyle="font-style:normal;font-weight:bold"'
        self.out += '>' + thestring + '</tspan></text>\n'

# class of blast hit data

class genome_line:
    def __init__(self, name):
        self.name = name
        self.contigs = []


def write_fasta_sibel(fasta_list, out_fasta, order_list=None):
    getfa = False
    getgb = False
    with open(out_fasta, 'w') as out:
        for num, fasta in enumerate(fasta_list):
            with open(fasta) as f:
                count = 0
                for line in f:
                    if line.startswith('>'):
                        out.write('>' + str(num) + '_' + str(count) + '\n')
                        count += 1
                        getfa = True
                    elif getfa:
                        out.write(line)
                    elif line.startswith('ORIGIN'):
                        out.write('>' + str(num) + '_' + str(count) + '\n')
                        count += 1
                        getgb = True
                    elif line.startswith('//'):
                        getgb = False
                    elif getgb:
                        out.write(''.join(line.split()[1:]) + '\n')

def run_sibel(in_fasta, sibel_dir, sibelia_path, sib_mode, min_block):
    subprocess.Popen(sibelia_path + ' -s ' + sib_mode + ' -m ' + str(min_block) + ' -o ' + sibel_dir + ' ' + in_fasta, shell=True).wait()


def get_genome_lines(sibel_file):
    with open(sibel_file) as f:
        f.readline()
        block_id = None
        is_core_dict = {}
        max_length_dict = {}
        seq_id_dict = {}
        get_block_id = 0
        no_of_chroms = 0
        genome_lines = {}
        len_dict = {}
        block_dict = {}
        for line in f:
            if line.startswith('-----'):
                if not block_id is None:
                    if len(chrom_set) == no_of_chroms and repeat:
                        is_core_dict[block_id] = 'repeat'
                    elif len(chrom_set) == no_of_chroms:
                        is_core_dict[block_id] = 'core'
                    else:
                        is_core_dict[block_id] = 'noncore'
                    max_length_dict[block_id] = max_len
                get_block_id = 1
                chrom_set = set()
                repeat = False
                max_len = 0

            elif get_block_id == 1:
                block_id = line.split()[1][1:]
                get_block_id = 2
            elif get_block_id == 2:
                get_block_id = 0
            elif not block_id is None:
                seq_id, strand, start, end, length = line.split()
                sample, chrom = seq_id_dict[seq_id]
                start, end, length = int(start), int(end), int(length)
                if sample in genome_lines and chrom in genome_lines[sample]:
                    genome_lines[sample][chrom].append((min([start, end]), strand, length, block_id))
                elif sample in genome_lines:
                    genome_lines[sample][chrom] = [(min([start, end]), strand, length, block_id)]
                else:
                    genome_lines[sample] = {chrom:[(min([start, end]), strand, length, block_id)]}
                if block_id in block_dict:
                    if sample in block_dict[block_id]:
                        block_dict[block_id][sample].append((start, end, chrom, strand))
                    else:
                        block_dict[block_id][sample] = [(start, end, chrom, strand)]
                else:
                    block_dict[block_id] = {sample:[(start, end, chrom, strand)]}
                if length > max_len:
                    max_len = length
                if seq_id_dict[seq_id][0] in chrom_set:
                    repeat = True
                chrom_set.add(seq_id_dict[seq_id][0])
            elif block_id is None:
                seq_id, size, desc = line.split()
                sample, contig = desc.split('_')
                if int(sample) + 1 > no_of_chroms:
                    no_of_chroms = int(sample) + 1
                seq_id_dict[seq_id] = (sample, contig)
                if sample in len_dict:
                    len_dict[sample][contig] = int(size)
                else:
                    len_dict[sample] = {contig:int(size)}
    new_genome_lines = {}
    for i in genome_lines:
        new_genome_lines[i] = {}
        for j in genome_lines[i]:
            new_genome_lines[i][j] = []
            blocks = genome_lines[i][j]
            blocks.sort()
            last_core_pos = 1
            non_core_list = []
            for k in blocks:
                pos, strand, length, block_id = k
                if is_core_dict[block_id] == 'core':
                    new_genome_lines[i][j].append([pos - last_core_pos, non_core_list])
                    new_genome_lines[i][j].append([length, 'core', block_id, strand, pos])
                    non_core_list = []
                    last_core_pos = pos + length
                else:
                    non_core_list.append((length, is_core_dict[block_id], block_id, strand, pos - last_core_pos))
            new_genome_lines[i][j].append([len_dict[i][j] - last_core_pos, non_core_list])
    out_lines = [[]]
    core_pos = {}
    contig_order = []
    for i in new_genome_lines['0']:
        size = 0
        for block in new_genome_lines['0'][i]:
            size += block[0]
        contig_order.append((size, i))
    contig_order.sort(reverse=True)
    num = 0
    for contig_size in contig_order: # create the reference line
        i = contig_size[1]
        for block in new_genome_lines['0'][i]:
            if block[1] == 'core':
                out_lines[0].append(block)
                core_pos[block[2]] = (num, block[3])
                max_core = num
            elif block[0] < 1:
                out_lines[0].append(None)
            elif num == 0:
                out_lines[0].append(block + ['right'])
            elif num == len(new_genome_lines['0'][i]) - 1:
                out_lines[0].append(block + ['left'])
            else:
                out_lines[0].append(block + ['centre'])
            num += 1
    def reverse_noncore(noncore_block):
        length = noncore_block[0]
        new_noncore_block = [length, []]
        for i in noncore_block[1][::-1]:
            new_noncore_block[-1].append((i[0], i[1], i[2], i[3], length - (i[4] + i[0])))
        return new_noncore_block
    for i in range(1, no_of_chroms): # place noncore blocks with only one position
        out_lines.append([None for x in range(max_core + 2)]) # create the line for the query genome
        for j in new_genome_lines[str(i)]:
            last_noncore = new_genome_lines[str(i)][j][-1]
            if len(new_genome_lines[str(i)][j]) == 1:
                out_lines[-1].append(last_noncore + ['centre']) # place contig with only noncore block
            else: # place last noncore block
                last_core = new_genome_lines[str(i)][j][-2]
                if last_core[3] == core_pos[last_core[2]][1]: # the core block is orientated the same way as the reference core block
                    if out_lines[-1][core_pos[last_core[2]][0] + 1] is None: # if noncore block is not already at location
                        out_lines[-1][core_pos[last_core[2]][0] + 1] = last_noncore + ['left'] # add noncore block
                    else:
                        out_lines[-1][core_pos[last_core[2]][0] + 1] = [last_noncore + ['left'], out_lines[-1][core_pos[last_core[2]][0] + 1]] # else keep block and pair with new block
                else:
                    if out_lines[-1][core_pos[last_core[2]][0] - 1] is None:
                        last_noncore = reverse_noncore(last_noncore)
                        out_lines[-1][core_pos[last_core[2]][0] - 1] = last_noncore + ['right']
                    else:
                        last_noncore = reverse_noncore(last_noncore)
                        out_lines[-1][core_pos[last_core[2]][0] - 1] = [out_lines[-1][core_pos[last_core[2]][0] - 1], last_noncore + ['right']]
                last_noncore = new_genome_lines[str(i)][j][0] # place first noncore block
                last_core = new_genome_lines[str(i)][j][1]
                if last_core[3] == core_pos[last_core[2]][1]:
                    if out_lines[-1][core_pos[last_core[2]][0] - 1] is None:
                        out_lines[-1][core_pos[last_core[2]][0] - 1] = last_noncore + ['right']
                    else:
                        out_lines[-1][core_pos[last_core[2]][0] - 1] = [out_lines[-1][core_pos[last_core[2]][0] - 1], last_noncore + ['right']]
                else:
                    if out_lines[-1][core_pos[last_core[2]][0] + 1] is None:
                        last_noncore = reverse_noncore(last_noncore)
                        out_lines[-1][core_pos[last_core[2]][0] + 1] = last_noncore + ['left']
                    else:
                        last_noncore = reverse_noncore(last_noncore)
                        out_lines[-1][core_pos[last_core[2]][0] + 1] = [last_noncore + ['left'], out_lines[-1][core_pos[last_core[2]][0] + 1]]
        for j in new_genome_lines[str(i)]:
            last_noncore = None
            for block in new_genome_lines[str(i)][j][1:]:
                if type(block[1]) is str:
                    out_lines[-1][core_pos[block[2]][0]] = block
                    if not last_noncore is None and last_noncore[0] > 1: # if there is a noncore block before current block
                        if block[3] == core_pos[block[2]][1] and out_lines[-1][core_pos[block[2]][0] - 1] is None: # if direction of current core block is same as ref and there is no block at noncore position
                            if last_core_dir and core_pos[last_core[2]][0] + 1 == core_pos[block[2]][0] - 1: # if last core block in same direction as reference core block and last_core and core are next to each other in reference
                                out_lines[-1][core_pos[block[2]][0] - 1] = last_noncore + ['centre']
                            else:
                                out_lines[-1][core_pos[block[2]][0] - 1] = last_noncore + ['right']
                        elif block[3] != core_pos[block[2]][1] and out_lines[-1][core_pos[block[2]][0] + 1] is None:
                            if not last_core_dir and core_pos[last_core[2]][0] - 1 == core_pos[block[2]][0] + 1:
                                last_noncore = reverse_noncore(last_noncore)
                                out_lines[-1][core_pos[block[2]][0] + 1] = last_noncore + ['centre']
                            else:
                                last_noncore = reverse_noncore(last_noncore)
                                out_lines[-1][core_pos[block[2]][0] + 1] = last_noncore + ['left']
                        elif last_core_dir and out_lines[-1][core_pos[last_core[2]][0] + 1] is None:
                            out_lines[-1][core_pos[last_core[2]][0] + 1] = last_noncore + ['left']
                        elif not last_core_dir and out_lines[-1][core_pos[last_core[2]][0] - 1] is None:
                            last_noncore = reverse_noncore(last_noncore)
                            out_lines[-1][core_pos[last_core[2]][0] - 1] = last_noncore + ['right']
                        elif block[3] == core_pos[block[2]][1]:
                            out_lines[-1][core_pos[block[2]][0] - 1] = [out_lines[-1][core_pos[block[2]][0] - 1], last_noncore + ['right']]
                        elif block[3] != core_pos[block[2]][1]:
                            last_noncore = reverse_noncore(last_noncore)
                            out_lines[-1][core_pos[block[2]][0] + 1] = [last_noncore + ['left'], out_lines[-1][core_pos[block[2]][0] + 1]]
                        else:
                            print 'asdfasdfa'
                    last_core = block
                    last_core_dir = block[3] == core_pos[block[2]][1]
                else:
                    last_noncore = block
    return out_lines, block_dict, is_core_dict

def draw_lines(in_lines, block_order_file, outfile, x_gap_size, y_gap_size, genome_height, figure_width, genome_line_width, core_sat, core_light, block_dict=None, is_core_dict=None):
    block_order = {}
    x_margin = 0
    core_set = set()
    for i in in_lines[0]:
        if not i is None and i[1] == 'core':
            core_set.add(i[2])
    with open(block_order_file) as f:
        for line in f:
            if line.startswith('>'):
                chrom_name = line.split('_')[0][1:]
                if not chrom_name in block_order:
                    block_order[chrom_name] = {}
                    count = 0
            else:
                for i in line.split():
                    the_block = i[1:]
                    if the_block in core_set:
                        block_order[chrom_name][the_block] = count
                        count += 1
    block_order_f2 = [[] for i in range(len(max(in_lines,key=len)))]
    block_sizes = [0 for i in range(len(max(in_lines,key=len)))]
    gotten_block = set()
    for i in in_lines:
        for num, j in enumerate(i):
            if not j is None and len(j) != 2:
                if type(j[1]) is list:
                    for k in j[1]:
                        if not k[2] in gotten_block:
                            block_order_f2[num].append(k[2])
                            gotten_block.add(k[2])
                if block_sizes[num] < j[0]:
                    block_sizes[num] = j[0]
            if not j is None and len(j) == 2:
                for k in j[0][1]:
                    if not k[2] in gotten_block:
                        block_order_f2[num].append(k[2])
                        gotten_block.add(k[2])
                for k in j[1][1]:
                    if not k[2] in gotten_block:
                        block_order_f2[num].append(k[2])
                        gotten_block.add(k[2])
                tot_size = j[0][0] + j[1][0]
                if block_sizes[num] < tot_size:
                    block_sizes[num] = tot_size
    new_block_order_f2 = []
    for i in block_order_f2:
        for j in i:
            new_block_order_f2.append(j)
    svg = scalableVectorGraphics(genome_height * len(in_lines) + y_gap_size * (len(in_lines) -1) + 500, figure_width + x_margin)
    scale = (figure_width - x_gap_size * (len(block_sizes) - 1)) * 1.0 / sum(block_sizes)
    curr_y = 0 # (genome_height + y_gap_size - 1) * len(in_lines)
    color_dict = {}
    color_no = 0
    core_block_order = []
    for line_num, i in enumerate(in_lines):
        curr_x = 0
        for num, j in enumerate(i):
            if j is None:
                curr_x += block_sizes[num] * scale + x_gap_size
            elif j[1] == 'core':
                length, core, block_id, strand, pos = j
                core_block_order.append(block_id)
                # print block_id, list(block_order[str(line_num)])
                hue = int(block_order[str(line_num)][block_id] * 1.0 / len(block_order[str(line_num)]) * 360)
                color = hsl_to_rgb(hue, core_sat, core_light)
                color_dict[block_id] = color
                out_color = hsl_to_rgb(hue, core_sat, max([core_light - 0.2, 0]))
                width = length * scale
                x1 = curr_x + (block_sizes[num] / 2 - length / 2) * scale
                svg.drawOutRect(x1, curr_y, width, genome_height, color, out_color)
                # print 'ding'
                curr_x += block_sizes[num] * scale
            elif len(j) == 2:
                x1 = curr_x
                x2 = x2 = x1 + j[0][0] * scale
                svg.drawLine(x1, curr_y + genome_height / 2, x2, curr_y + genome_height / 2, genome_line_width, (0, 0, 0))
                for k in j[0][1]:
                    if k[2] in color_dict:
                        color = color_dict[k[2]]
                    else:
                        color = color_list[color_no % len(color_list)]
                        color_dict[k[2]] = color
                        pattern = pattern_list[color_no % len(pattern_list)]
                        svg.create_pattern(k[2], color, pattern, 10, 10)
                        color_no += 1
                    blockx = x1 + k[4] * scale
                    block_width = k[0] * scale
                    svg.drawPatternRect(blockx, curr_y, block_width, genome_height, k[2], color, 1)
                x1 = block_sizes[num] * scale + x_gap_size + curr_x - j[1][0] * scale
                x2 = x1 + j[1][0] * scale
                svg.drawLine(x1, curr_y + genome_height / 2, x2, curr_y + genome_height / 2, genome_line_width, (0, 0, 0))
                for k in j[1][1]:
                    if k[2] in color_dict:
                        color = color_dict[k[2]]
                    else:
                        color = color_list[color_no % len(color_list)]
                        color_dict[k[2]] = color
                        pattern = pattern_list[color_no % len(pattern_list)]
                        svg.create_pattern(k[2], color, pattern, 10, 10)
                        color_no += 1
                    blockx = x1 + k[4] * scale
                    block_width = k[0] * scale
                    svg.drawPatternRect(blockx, curr_y, block_width, genome_height, k[2], color, 1)
                curr_x += block_sizes[num] * scale + x_gap_size
            else:
                if j[2] == 'left':
                    x1 = curr_x
                elif j[2] == 'right':
                    x1 = block_sizes[num] * scale + x_gap_size + curr_x - j[0] * scale
                elif j[2] == 'centre':
                    x1 = block_sizes[num] * scale * 0.5 + x_gap_size * 0.5 + curr_x - j[0] * scale * 0.5
                x2 = x1 + j[0] * scale
                svg.drawLine(x1, curr_y + genome_height / 2, x2, curr_y + genome_height / 2, genome_line_width, (0, 0, 0))
                for k in j[1]:
                    if k[2] in color_dict:
                        color = color_dict[k[2]]
                    else:
                        color = color_list[color_no % len(color_list)]
                        color_dict[k[2]] = color
                        pattern = pattern_list[color_no % len(pattern_list)]
                        svg.create_pattern(k[2], color, pattern, 10, 10)
                        color_no += 1
                    blockx = x1 + k[4] * scale
                    block_width = k[0] * scale
                    svg.drawPatternRect(blockx, curr_y, block_width, genome_height, k[2], color, 1)
                curr_x += block_sizes[num] * scale + x_gap_size

        curr_y += genome_height + y_gap_size
    curr_y += 40
    svg.drawLine(50, curr_y, 50 + 100000 * scale, curr_y, genome_line_width, (0, 0, 0))
    svg.drawLine(50, curr_y - 10, 50, curr_y + 10, genome_line_width, (0,0,0))
    svg.drawLine(50 + 100000 * scale, curr_y - 10, 50 + 100000 * scale, curr_y + 10, genome_line_width, (0,0,0))
    svg.writeString('100kbp', 50 + 50000 * scale, curr_y + 20, 12, justify='middle')
    curr_y += 50
    color = hsl_to_rgb(0, core_sat, core_light)
    out_color = hsl_to_rgb(0, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(50, curr_y, 100, genome_height, color, out_color)
    color = hsl_to_rgb(200, core_sat, core_light)
    out_color = hsl_to_rgb(200, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(170, curr_y, 60, genome_height, color, out_color)
    svg.writeString('Core blocks', 50, curr_y + genome_height + 15, 12)
    curr_y += 50
    svg.drawHueGradient(50, curr_y, 500, genome_height, core_sat, core_light)
    svg.writeString('start', 50, curr_y + genome_height + 15, 12)
    svg.writeString('Position of core block in genome', 300, curr_y + genome_height + 15, 12, justify='middle')
    svg.writeString('end', 550, curr_y + genome_height + 15, 12, justify='right')
    curr_y += 50
    color = color_list[0]
    pattern = pattern_list[0]
    svg.create_pattern('leg1', color, pattern, 10, 10)
    svg.drawPatternRect(170, curr_y, 60, genome_height, 'leg1', color, 1)
    color = color_list[1]
    pattern = pattern_list[1]
    svg.create_pattern('leg2', color, pattern, 10, 10)
    svg.drawPatternRect(50, curr_y, 100, genome_height, 'leg2', color, 1)
    svg.writesvg(outfile)
    svg.writeString('Non-core blocks', 50, curr_y + genome_height + 15, 12)
    curr_y += 50
    svg.drawLine(50, curr_y + genome_height/2, 150, curr_y + genome_height/2, genome_line_width)
    svg.drawLine(170, curr_y + genome_height/2, 230, curr_y + genome_height/2, genome_line_width)
    svg.writeString('Unaligned sequence', 50, curr_y + genome_height + 15, 12)
    curr_y += 50
    color = hsl_to_rgb(0, core_sat, core_light)
    out_color = hsl_to_rgb(0, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(50, curr_y, 100, genome_height, color, out_color)
    svg.drawLine(150, curr_y + genome_height/2, 330, curr_y + genome_height/2, genome_line_width)
    color = color_list[1]
    svg.drawPatternRect(150, curr_y, 100, genome_height, 'leg2', color, 1)
    color = color_list[0]
    svg.drawPatternRect(270, curr_y, 60, genome_height, 'leg1', color, 1)
    color = hsl_to_rgb(200, core_sat, core_light)
    out_color = hsl_to_rgb(200, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(330 + x_gap_size, curr_y, 100, genome_height, color, out_color)
    svg.writeString('Noncore region adjacent to left core block', 50, curr_y + genome_height + 15, 12)
    curr_y += 50
    color = hsl_to_rgb(0, core_sat, core_light)
    out_color = hsl_to_rgb(0, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(50, curr_y, 100, genome_height, color, out_color)
    svg.drawLine(150 + x_gap_size/2, curr_y + genome_height/2, 330 + x_gap_size/2, curr_y + genome_height/2, genome_line_width)
    color = color_list[1]
    svg.drawPatternRect(150 + x_gap_size/2, curr_y, 100, genome_height, 'leg2', color, 1)
    color = color_list[0]
    svg.drawPatternRect(270 + x_gap_size/2, curr_y, 60, genome_height, 'leg1', color, 1)
    color = hsl_to_rgb(200, core_sat, core_light)
    out_color = hsl_to_rgb(200, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(330 + x_gap_size, curr_y, 100, genome_height, color, out_color)
    svg.writeString('Noncore region adjacent to both core blocks', 50, curr_y + genome_height + 15, 12)
    curr_y += 50
    color = hsl_to_rgb(0, core_sat, core_light)
    out_color = hsl_to_rgb(0, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(50, curr_y, 100, genome_height, color, out_color)
    svg.drawLine(150 + x_gap_size, curr_y + genome_height/2, 330 + x_gap_size, curr_y + genome_height/2, genome_line_width)
    color = color_list[1]
    svg.drawPatternRect(150 + x_gap_size, curr_y, 100, genome_height, 'leg2', color, 1)
    color = color_list[0]
    svg.drawPatternRect(270 + x_gap_size, curr_y, 60, genome_height, 'leg1', color, 1)
    color = hsl_to_rgb(200, core_sat, core_light)
    out_color = hsl_to_rgb(200, core_sat, max([core_light - 0.2, 0]))
    svg.drawOutRect(330 + x_gap_size, curr_y, 100, genome_height, color, out_color)
    svg.writeString('Noncore region adjacent to right core block', 50, curr_y + genome_height + 15, 12)
    temp_new_block_order_f2 = []
    for i in new_block_order_f2:
        if len(block_dict[i]) != len(in_lines):
            temp_new_block_order_f2.append(i)
            print 'dong'
        else:
            print 'ding'
    new_block_order_f2 = temp_new_block_order_f2
    if not block_dict is None:
        curr_x = 0
        for num1, i in enumerate(new_block_order_f2):
            max_size = 0
            for num2 in range(len(in_lines)):
                if str(num2) in block_dict[i]:
                    start, stop, contig, strand = block_dict[i][str(num2)][0]
                    size = abs(start - stop)
                    svg.drawPatternRect(curr_x, curr_y + genome_height + 20 + num2 * (genome_height + 5), size / 100, genome_height, i, color_dict[i], 1)
                    if size > max_size:
                        max_size = size
            curr_x += max_size / 100 + 4

    svg.writesvg(outfile)
    return core_block_order + new_block_order_f2, color_dict[i]




#
parser = argparse.ArgumentParser(prog='Easyfig 3.0', formatter_class=argparse.RawDescriptionHelpFormatter, description='''
Chromatiblock.py: Even easier genome figures.

Version: 3.0.0
License: GPLv3

USAGE: python Chromatiblock.py



''', epilog="Thanks for using Easyfig")
parser.add_argument('-d', '--input_directory', action='store', help='fasta file of assembled contigs or scaffolds')
parser.add_argument('-r', '--reference_genome', action='store', help='fasta file in directory to use as reference')
parser.add_argument('-l', '--order_list', action='store', help='List of fasta files in desired order.')
parser.add_argument('-f', '--fasta_files', nargs='+', action='store', help='List of fasta/genbank files to use as input')
parser.add_argument('-cl', '--command_line', action='store_true', default=False, help='run easyfig in command-line mode')
parser.add_argument('-w', '--working_directory', action='store', help='Folder to write intermediate files.')
parser.add_argument('-s', '--sibelia_path', action='store', default='Sibelia', help='Specify path to sibelia '
                                                                                    '(does not need to be set if Sibelia binary is in path).')
parser.add_argument('-sm', '--sibelia_mode', action='store', default='fine', help='mode for running sibelia <loose|fine|far>')
parser.add_argument('-o', '--svg', action='store', help='Location to write svg output.')
parser.add_argument('-m', '--min_block_size', action='store', type=int, default=5000, help='Minimum size of syntenic block.')



args = parser.parse_args()


fasta_list = []
if args.command_line:
    if args.fasta_files is None and args.input_directory is None:
        sys.stderr.write('Please specify a list2 of fasta files to create figure (-f) or directory containing fasta files (-d)')
    elif not args.fasta_files is None and not args.input_directory is None:
        sys.stderr.write('Please use only one of the directory or fasta flags')
    elif not args.input_directory is None and args.reference_genome is None:
        sys.stderr.write('Please specify which fasta is the reference fasta')
    elif not args.input_directory is None:
        fasta_list.append(os.path.abspath(args.reference_genome))
        for i in os.listdir(args.input_directory):
            abspath = os.path.abspath(args.input_directory + '/' + i)
            if not abspath in fasta_list:
                if abspath.endswith('.fna') or abspath.endswith('.fa') or abspath.endswith('.fasta') or abspath.endswith('.gbk'):
                    fasta_list.append(abspath)
    elif not args.fasta_files is None:
        fasta_list = args.fasta_files
    if os.path.exists(args.working_directory):
        if not os.path.isdir(args.working_directory):
            sys.exit('Working directory is a file.')
    else:
        os.makedirs(args.working_directory)
    if not args.order_list is None:
        with open(args.order_list) as f:
            new_fasta_list = []
            for line in f:
                gotit = False
                for i in fasta_list:
                    if line.rstrip() in i:
                        new_fasta_list.append(i)
                        gotit = True
                        break
        fasta_list = new_fasta_list
        print len(fasta_list)
    write_fasta_sibel(fasta_list, args.working_directory + '/input.fasta')
    run_sibel(args.working_directory + '/input.fasta', args.working_directory,   args.sibelia_path, args.sibelia_mode, args.min_block_size)
    genome_lines, blocks, is_core_dict = get_genome_lines(args.working_directory + '/blocks_coords.txt')
    block_order, color_dict = draw_lines(genome_lines, args.working_directory + '/genomes_permutations.txt', args.svg, 10, 10, 20, 5000, 4, 0.3, 0.5, blocks, is_core_dict)