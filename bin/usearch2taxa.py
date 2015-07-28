#!/usr/bin/env python
# usage usearch2taxa usearchout.txt taxonmap output.txt
# expects usearch blast6 output
# if ref ID has an underscore, only takes the part before the underscore
#
# taxonmap is formatted like the greengenes taxonomy maps: "Refseqid\tTaxonomy"
# can also handle taxonmap that has species (e.g. Escherichia coli)
# 
import sys

# given two lists of taxonomic hierarchies,
# returns the deepest shared hierarchy
# or None if no intersection
def lca(tax1, tax2):
    if tax1 is None or tax2 is None:
        return None
    i = min(len(tax1), len(tax2)) - 1
    while i >= 0:
        if tax1[i] == tax2[i]:
            return tax1[:(i+1)]
        i -= 1
    return None

if __name__ == "__main__":

    usearch_fp = sys.argv[1]
    taxon_fp = sys.argv[2]
    out_fp = sys.argv[3]

    species_only = False

    ref_ids_missing_from_taxonomy = 0

    # load the taxon map
    print "Loading taxonomy map..."
    taxa = {}
    for line in open(taxon_fp,'r'):
        words = line.strip().split('\t')
        taxonomy = words[1].split(';')
        if len(taxonomy) == 1:
            species_only = True
            taxonomy = taxonomy[0].split(' ')
        taxa[words[0]] = taxonomy

    # parse one input seq at a time
    taxon_assignments = {}

    print "Determining consensus taxonomy assignments..."
    count = 1
    for line in open(usearch_fp,'r'):
        if count % 1000000 == 0:
            print count
        count += 1
        words = line.strip().split('\t')
        query_id = words[0]
        ref_id = words[1].split('_')[0]
        if not taxa.has_key(ref_id):
            ref_ids_missing_from_taxonomy += 1
        else:
            tax = taxa[ref_id]

            if not taxon_assignments.has_key(query_id):
                taxon_assignments[query_id] = tax
            else:
                intersection = lca(taxon_assignments[query_id], tax)
                taxon_assignments[query_id] = intersection

    # tabulate taxon counts
    print count, "hits processed. Tabulating taxa..."
    taxon_counts = {}
    for key in taxon_assignments:
        taxon = taxon_assignments[key]
        if taxon is not None:
            if species_only:
                taxon = ' '.join(taxon)
            else:
                taxon = ';'.join(taxon)
            if not taxon_counts.has_key(taxon):
                taxon_counts[taxon] = 1
            else:
                taxon_counts[taxon] += 1

    # print results
    print "Writing results..."
    outf = open(out_fp,'w')
    for key in sorted(taxon_counts):
        outf.write(key + '\t' + str(taxon_counts[key]) + '\n')
    outf.close()


                
