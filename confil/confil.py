import os

import click

from kraken import kraken_installed, run_kraken

# TODO: Remove
KRAKEN2_DEFAULT_DB = "/tools/databases/kraken2/04092018/standard/"
OUT_DIR = os.path.abspath(os.curdir)
fastq_file_extensions = ['.fq', '.fastq']


@click.command()
@click.option('--db', default=OUT_DIR, required=True,
              help='Name for Kraken 2 DB', type=click.Path(exists=True),
              show_default=True)
@click.option('--threads', default=1, help='Number of threads',
              show_default=True)
@click.option('--cutoff', default=90, show_default=True,
              help='Percentage of fragments covered')
@click.option('--paired', is_flag=True,
              help='The filenames provided have paired-end reads')
@click.argument('seqfiles', nargs=-1, required=True)
def confil(db, threads, cutoff, paired, seqfiles):
    if kraken_installed():
        seqfiles = [os.path.abspath(seqfile) for seqfile in seqfiles]
        if len(seqfiles) > 2:
            raise ValueError(
                "Expecting no more than 2 FASTQ files. We got {}.\n{}".format(
                    len(seqfiles), seqfiles))
        click.secho('Using a cutoff of {}% for contamination!\n'.format(
            cutoff), fg='green')
        # run kraken and read/parse report
        run_kraken(db=db, threads=threads, cutoff=cutoff,
                   paired=paired, seqfiles=seqfiles)


if __name__ == '__main__':
    confil()
