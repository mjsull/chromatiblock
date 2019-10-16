# chromatiblock.py

## Scalable, whole-genome visualisation of structural changes in prokaryotes

### Version: 0.3.1

### License: GPLv3

### Installation via conda:

conda -c bioconda install chromatiblock

#### Direct download:

Alternatively you can download and run the script from [here](https://github.com/mjsull/chromatiblock/releases/download/v0.3.1/chromatiblock.py).
#### requirements:
(these will be installed automatically if chromatiblock is installed with conda)

While chromatiblock will run fine without these programs, they are needed for certain tasks.

Sibelia - for autmoatic generation of colinear blocks

cairosvg - for creating PNG and PDF images (svg and html supported natively) 

ncbi-blast+ - for automatic annotation of genes

svg-pan-zoom.min.js - by default the html output uses an online javascript library for zoom functionality,
the -pz flag can be used to point to an offline location of svg-pan-zoom.

### Example usage: 
`python chromatiblock.py -f genome1.fasta genome2.fasta .... genomeN.fasta -w cb_working_dir -o image.svg` 

or
     
`python chromatiblock.py -d /path/to/fasta_directory/ -w cb_working_dir -o image.svg`


# Example output:

![chromatiblock](https://raw.githubusercontent.com/mjsull/chromatiblock/gh-pages/images/chromatiblock_main.gif)

chromatiblock outputs two figures. The first figure (top) shows the topology of core and noncore colinear blocks in each genome. Core co-linear blocks present in all isolate genomes are aligned vertically and shown as solid rectangles. They are colored according to the block location in each genome to highlight inversions (legend at bottom). Non-core regions, present in only a subset of genomes, are each represented with a unique striped fill pattern.

The second figure (bottom) shows the presence and absence of non-core colinear blocks. Non-core colinear blocks are enlarged and aligned on top of one another. Absence of a block indicates absence in the respective genome.

A HTML example can be found [here](https://mjsull.github.com/chromatiblock)


# Demo:
Example files can be found [here](https://github.com/mjsull/chromatiblock/releases/download/v0.3.0/chromatiblock_example.zip)

To run: extract files to your current directory and then use the command

`chromatiblock.py -d chromatiblock_example -w cb_working_dir -o example.html -gb chromatiblock_example/toxins.faa -c chromatiblock_example/categories.tsv`

Then open example.html with your favourite browser.

### Arguments:



``-h``, ``--help``
------------------
show this help message and exit



``-d``, ``--input_directory </path/to/fastas/>``
-----------------
Directory of fasta or genbank files to use as input (will ignore files without .fasta, .fa, .fna, .gb or .gbk suffixes).


``-l``, ``--order_list <list_of_filenames.txt>``
------------------------
file containing list of filenames (one per line) in desired order


``-f``, ``--fasta_files <genome_1.fasta> <genome_2.fasta> .... <genome_x.fasta> ``
-------------------------
List of fasta/genbank files to use as input

``-w``, ``--working_directory <working_dir>``
-------------------------------
Folder to write intermediate files.

``-s``, ``--sibelia_path </path/to/sibelia/>``
---------------------------
Specify path to sibelia (does not need to be set if Sibelia binary is in path)

``-sm``, ``--sibelia_mode <loose>``
---------------------------
mode for running sibelia <loose|fine|far>

**default: loose**

``-o``, ``--out <outfile.svg>``
--------------------
Location to write output (options \*.svg/\*.html/\*.png/\*.pdf) will default to svg (and add extension). (n.b. PDF does not work particularly well all the time)




``-q``, ``--ppi <integer>``
-------
pixels per inch (only used for png, figure width is 8 inches)

**default: 50**

``-m``, ``--min_block_size <integer>``
----
Minimum size of syntenic block to display.

**default: 1000bp**

``-c``, ``--categorise <categories.txt>``
-----------
color blocks by category

provide a file where each line contains


```<genome.fasta>    <fasta_header>    <category_name>   <start>   <stop>```

e.g.

```
genome_1.fasta    contig_1    phage    50000 100000
genome_2.fasta    contig_1    phage    80000    120000
genome_2.fasta    contig_2    plasmid
genome_3.fasta    contig_2    plasmid
genome_3.fasta    contig_1    transposon 100000 105000
```


non-core blocks in panel B will be colored according to category if at least 50% falls within a specified range. Start and stop columns are optional.


``-gb``, ``--genes_of_interest_blast <genes.faa>``
----

Uses BLASTx to find genes in chromosome and then marks them in panel a and b with a triangle

``-gf``, ``--genes_of_interest_file <genes.txt>``
---
mark genes of interest using a list


provide a file where each line contains


```<genome.fasta>    <fasta_header>    <gene_name>   <start>```

e.g.
```
genome_1.fasta    contig_1    mrcA    50000
genome_2.fasta    contig_1    mrcA    80000
genome_2.fasta    contig_2    hlb    20000
```

``-gh``, ``--genome_height <int>``
------
Height of genome blocks in pixels

**default: 280**

``-vg``, ``--gap <int>``
----
gap between genomes

**default: 20**

``-ss``, ``--skip_sibelia``
----
Use sibelia output already in working directory



``-sb``, ``--skip_blast``
----
use existing BLASTx file for annotation (must use with -gb flag)

``-maf``, ``--maf_alignment <alignment.maf>``
-----
use a maf file for multiple alignment instead of Sibelia. MAF files can be produced by SibeliaZ and Mugsy.


``-pz``, ``--svg_pan_zoom_location``
----
Location of the svg-pan-zoom javascript library, this can be set to an offline location, or a directory relative to the html.

**default: http://ariutta.github.io/svg-pan-zoom/dist/svg-pan-zoom.min.js**

``-v``, ``--version``
-----
print version and exit.