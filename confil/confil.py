import distutils.spawn
import os
import re
from shlex import split
from subprocess import PIPE, Popen

import click

# TODO: Remove
KRAKEN2_DEFAULT_DB = "/tools/databases/kraken2/04092018/standard/"
OUT_DIR = os.path.abspath(os.curdir)


def db_path():
    # Checking DB path
    if os.path.exists(KRAKEN2_DEFAULT_DB):
        return KRAKEN2_DEFAULT_DB
    else:
        return OUT_DIR


def kraken_installed():
    # check if `kraken2` is in path
    installed = distutils.spawn.find_executable("kraken2")
    if not installed:
        raise OSError("kraken2 is not installed.")
    return installed


def run_kraken(db, threads, cutoff, paired, seqfiles):
    # Using the sample name to track report
    seq_name = [os.path.splitext(os.path.basename(seq))[0]
                for seq in seqfiles][0]
    # remove _ and numbers
    seq_name = re.sub('_[0-9]+$', '', seq_name)
    # building cmd
    cmd = "kraken2 --threads {threads} --db {db} --output {seq_name}.out --report {seq_name}.tab ".format(
        threads=threads, db=db, seq_name=seq_name)
    if paired:
        cmd += "--paired --classified-out {}_cseqs#.fq ".format(seq_name)
    cmd += "{seqfiles}".format(seqfiles=' '.join(seqfiles))
    click.secho("Executing kraken2: \n{}\n".format(
        split(cmd)), fg='bright_yellow')

    # TODO: remove
    test_file = "https://raw.githubusercontent.com/COMBAT-TB/confil/master/test/test_data/test_file.tab"
    out_file = os.path.join(OUT_DIR, "{}.tab".format(seq_name))
    mock_cmd = 'wget {} -O {}'.format(test_file, out_file)
    cmd = mock_cmd
    click.secho("Executing mock_cmd: \n{}\n".format(split(cmd)), fg='red')

    p = Popen(split(cmd), stdout=PIPE, stderr=PIPE, close_fds=True)
    while True:
        output = p.stdout.readline()
        if output == '' and p.poll() is not None:
            break
        if output:
            click.echo(output)
    returncode = p.poll()
    if returncode != 0:
        error = p.stderr.readline()
        raise OSError("Kraken2 launch error:\n{}\n".format(error))
    # parse kraken report
    report_file = os.path.join(OUT_DIR, "{}.tab".format(seq_name))
    parse_report(report_file=report_file, cutoff=cutoff)
    return returncode


def parse_report(report_file, cutoff):
    file_name = os.path.splitext(os.path.basename(report_file))[0]
    hit = None
    if os.stat(report_file).st_size > 0 and report_file.endswith(".tab"):
        click.secho("Processing {} with cutoff of {}...\n".format(
            report_file, cutoff), fg='green')
        with open(report_file, 'r') as report:
            for line in report:
                line = [str(e).strip() for e in line.split('\t')]
                if len(line) > 1:
                    click.secho('{}'.format(line), fg='green')
                    # Percentage of fragments covered by the clade rooted at this taxon
                    percentage = int(float(line[0]))
                    # Number of fragments covered by the clade rooted at this taxon
                    # num_covered = int(float(line[1]))
                    # Number of fragments assigned directly to this taxon
                    # num_assigned = int(float(line[2]))
                    # NCBI taxonomic ID number
                    # ncbi_tax = int(float(line[3]))
                    # Indented scientific name (Mycobacterium\n)
                    name = str(line[5]).strip()
                    if percentage < cutoff and 'Mycobacterium' in name:
                        click.secho('\n{}%: {} is contaminated!\n'.format(
                            percentage, file_name), fg='red')
                        raise SystemExit('{}%: {} is contaminated!\n'.format(
                            percentage, file_name))
                    if percentage >= cutoff and 'Mycobacterium' in name:
                        click.secho('\n{}%: {} is not contaminated!\n'.format(
                            percentage, file_name), fg='green')
                        hit = line
                        break
    click.secho('Hit: {}'.format(hit), fg='green')
    return hit


@click.command()
@click.option('--db', default=db_path(), required=True,
              help='Name for Kraken 2 DB', type=click.Path(exists=True),
              show_default=True)
@click.option('--threads', default=1, help='Number of threads',
              show_default=True)
@click.option('--cutoff', default=50, show_default=True,
              help='Percentage of fragments covered')
@click.option('--paired', is_flag=True,
              help='The filenames provided have paired-end reads')
@click.argument('seqfiles', nargs=-1, required=True)
def confil(db, threads, cutoff, paired, seqfiles):
    """
    Checks sequence for contamination using specified cutoff.
    """
    if kraken_installed():
        seqfiles = [os.path.abspath(seqfile) for seqfile in seqfiles]
        if len(seqfiles) > 2 and not paired:
            raise ValueError(
                "Expecting no more than 2 FASTQ files. We got {}.\n{}".format(
                    len(seqfiles), seqfiles))
        if paired and len(seqfiles) < 2:
            raise ValueError(
                "Expecting 2 paired FASTQ files. We got {}.\n{}".format(
                    len(seqfiles), seqfiles))
        click.secho('Using a cutoff of {}% for contamination!\n'.format(
            cutoff), fg='green')
        # run kraken and read/parse report
        run_kraken(db=db, threads=threads, cutoff=cutoff,
                   paired=paired, seqfiles=seqfiles)


if __name__ == '__main__':
    confil()
