import distutils.spawn
import os
from shlex import split
from subprocess import PIPE, Popen

import click

from report import parse_report

OUT_DIR = os.path.abspath(os.curdir)


def kraken_installed():
    # check if `kraken2` is in path
    # TODO remove python
    installed = distutils.spawn.find_executable("python")
    if not installed:
        raise OSError("kraken2 is not installed.")
    return installed


def run_kraken(db, threads, cutoff, paired, seqfiles):
    # Using the sample name to track report
    seq_name = [os.path.splitext(os.path.basename(seq))[0]
                for seq in seqfiles][0]
    # building cmd
    cmd = "kraken2 --threads {threads} --db {db} --output {seq_name}.out --report {seq_name}.report ".format(
        threads=threads, db=db, seq_name=seq_name)
    if paired:
        cmd += "--paired --classified-out {}_cseqs#.fq ".format(seq_name)
    cmd += "{seqfiles}".format(seqfiles=' '.join(seqfiles))
    click.secho("Executing kraken2: \n{}\n".format(
        split(cmd)), fg='bright_yellow')

    # TODO: remove
    test_file = "https://raw.githubusercontent.com/COMBAT-TB/confil/master/test/test_data/test_file.report"
    out_file = os.path.join(OUT_DIR, "{}.report".format(seq_name))
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
    report_file = os.path.join(OUT_DIR, "{}.report".format(seq_name))
    parse_report(report_file=report_file, cutoff=cutoff)
    return returncode
