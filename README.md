# Chromatiblock.py

## Scalable, whole-genome visualisation of structural changes in prokaryotes

### Version: 0.2.0

License: GPLv3

### EXAMPLE USAGE: python Chromatiblock.py -d <fasta_directory> -r <reference.fasta> -o <image.svg>

### arguments:


```
USAGE: python Chromatiblock.py 

arguments:
  -h, --help            show help message and exit
  -d INPUT_DIRECTORY, --input_directory INPUT_DIRECTORY
                        fasta file of assembled contigs, scaffolds or finished
                        genomes.
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
  -o OUT, --out OUT     Location to write output (options *.svg/*.html/*.png
  -q PPI, --ppi PPI     pixels per inch (only used for png)
  -m MIN_BLOCK_SIZE, --min_block_size MIN_BLOCK_SIZE
                        Minimum size of syntenic block.
  -c CATEGORISE, --categorise CATEGORISE
                        color blocks by category
  -gb GENES_OF_INTEREST_BLAST, --genes_of_interest_blast GENES_OF_INTEREST_BLAST
                        mark genes of interest
  -gf GENES_OF_INTEREST_FILE, --genes_of_interest_file GENES_OF_INTEREST_FILE
                        mark genes of interest
  -gh GENOME_HEIGHT, --genome_height GENOME_HEIGHT
                        Height of genome blocks
  -vg GAP, --gap GAP    gap between genomes
  -ss, --skip_sibelia   Use sibelia output already in working directory
  -sb, --skip_blast     use existing BLASTx file for annotation

# Example output:

Chromatiblock outputs two figures. The first figure (top) shows the topology of core and noncore colinear blocks in each genome. Core co-linear blocks present in all isolate genomes are aligned vertically and shown as solid rectangles. They are colored according to the block location in each genome to highlight inversions (legend at bottom). Non-core regions, present in only a subset of genomes, are each represented with a unique striped fill pattern.

The second figure (bottom) shows the presence and absence of non-core colinear blocks. Non-core colinear blocks are enlarged and aligned on top of one another. Absense of a block indicates absense in the respective genome.
