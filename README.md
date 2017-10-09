# Chromatiblock.py

## Large scale whole genome visualisation using colinear blocks.

### Version: 0.1.0

License: GPLv3

### EXAMPLE USAGE: python Chromatiblock.py -d <fasta_directory> -r <reference.fasta> -o <image.svg>

### arguments:
```  -h, --help            show this help message and exit
  -d INPUT_DIRECTORY, --input_directory INPUT_DIRECTORY
                        fasta file of assembled contigs, scaffolds or finished
                        genomes.
  -r REFERENCE_GENOME, --reference_genome REFERENCE_GENOME
                        fasta file in directory to use as reference
  -l ORDER_LIST, --order_list ORDER_LIST
                        List of fasta files in desired order.
  -f FASTA_FILES [FASTA_FILES ...], --fasta_files FASTA_FILES [FASTA_FILES ...]
                        List of fasta/genbank files to use as input
  -w WORKING_DIRECTORY, --working_directory WORKING_DIRECTORY
                        Folder to write intermediate files.
  -s SIBELIA_PATH, --sibelia_path SIBELIA_PATH
                        Specify path to sibelia (does not need to be set if
                        Sibelia binary is in path).
  -sm SIBELIA_MODE, --sibelia_mode SIBELIA_MODE
                        mode for running sibelia <loose|fine|far>
  -o SVG, --svg SVG     Location to write svg output.
  -m MIN_BLOCK_SIZE, --min_block_size MIN_BLOCK_SIZE
                        Minimum size of syntenic block.
```
# Example output:

Chromatiblock outputs two images. The first figure (top) shows the topology of core and noncore colinear blocks in each genome. Core co-linear blocks present in all isolate genomes are aligned vertically and shown as solid rectangles. They are colored according to the block location in each genome to highlight inversions (legend at bottom). Non-core regions, present in only a subset of genomes, are each represented with a unique striped fill pattern.

The second figure (bottom) shows the presence and absence of non-core colinear blocks. Non-core colinear blocks are enlarged and aligned on top of one another. Absense of a block indicates absense in the respective genome.

![chromatiblock](https://raw.githubusercontent.com/mjsull/chromatiblock/gh-pages/images/chromatiblock_main.gif)

Example of chromatiblock output. 
