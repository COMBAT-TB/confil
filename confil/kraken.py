import distutils.spawn
import os
import re
from shlex import split
from subprocess import PIPE, Popen

import click

from .report import parse_report

OUT_DIR = os.path.abspath(os.curdir)


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
    # test_file = "https://raw.githubusercontent.com/COMBAT-TB/confil/master/test/test_data/test_file.tab"
    # out_file = os.path.join(OUT_DIR, "{}.tab".format(seq_name))
    # mock_cmd = 'wget {} -O {}'.format(test_file, out_file)
    # cmd = mock_cmd
    # click.secho("Executing mock_cmd: \n{}\n".format(split(cmd)), fg='red')

    p = Popen(split(cmd), stdout=PIPE, stderr=PIPE, close_fds=True)
    (output, _) = p.communicate()
    if output:
        click.echo(output)
    returncode = p.wait()
    if returncode != 0:
        error = p.stderr.readline()
        raise OSError("Kraken2 launch error:\n{}\n".format(error))
    # parse kraken report
    report_file = os.path.join(OUT_DIR, "{}.tab".format(seq_name))
    parse_report(report_file=report_file, cutoff=cutoff)
    return returncode
