# simulates shotgun sequencing of a fasta file
# usage
# shotgun_fasta.py -i fastafile -l readlen -n num_reads -o outfile
import sys, os, random
from optparse import OptionParser

def make_option_parser():
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
    parser.add_option("-i", "--input_fasta",
                      default=None,
                      type='string',
                      help="Path to input fasta [required]")
    parser.add_option("-n", "--num_reads",
                      default=1000,
                      type='int',
                      help="Number of reads to generate [default %default]")
    parser.add_option("-l", "--read_length",
                      default=100,
                      type='int',
                      help="Length of reads to generate [default %default]")
    parser.add_option("-o","--output_fasta",
                      type="string",
                      default=None,
                      help="Path to output fasta",)
    return parser


if __name__ == '__main__':
	parser = make_option_parser()
	(options, args) = parser.parse_args()

	if options.output_fasta is None:
		options.output_fasta = os.path.splitext(os.path.split(options.input_fasta)[1])[0]
		options.output_fasta += '_shotgun'
		options.output_fasta += '_n' + str(options.num_reads)
		options.output_fasta += '_l' + str(options.read_length) + '.fasta'

	# read in seqs
	fin = open(options.input_fasta,'r')
	seqs = []
	seq_ids = []
	seq_lengths = []
	seq = ''
	seq_id = ''
	for line in fin:
		if line.startswith('>'):
			if len(seq) > 0:
				seqs.append(seq)
				seq_lengths.append(len(seq))
				seq_ids.append(seq_id)
			seq_id = line[1:].strip().split()[0]
			seq = ''
		else:
			seq += line.strip()
	
	nseqs = len(seqs)
	
	# simulate
	out_lines = []
	for i in xrange(options.num_reads):
		seq_ix = random.randint(0,nseqs-1)
		seq_start_max = seq_lengths[seq_ix] - options.read_length
		if seq_start_max < 0:
			print seq_ix
			print seq_lengths[seq_ix]
			print seq_start_max
			raise ValueError('Read ' + str(seq_ix) + ' with ID ' + seq_ids[seq_ix] + ' with length ' + str(seq_lengths[seq_ix]) + ' is shorter than seq_length.')
		if(seq_start_max == 0):
			seq_pos = 0
		else:
			seq_pos = random.randint(0,seq_start_max)
		out_lines.append('>' + seq_ids[seq_ix] + '_' + str(i))
		out_lines.append(seqs[seq_ix][seq_pos:(seq_pos + options.read_length)])
	
	fout = open(options.output_fasta,'w')
	fout.write('\n'.join(out_lines))
	fout.close()
