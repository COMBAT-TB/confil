# confil

[![Build Status](https://travis-ci.org/COMBAT-TB/confil.svg?branch=master)](https://travis-ci.org/COMBAT-TB/confil)
[![Anaconda-Server Badge](https://anaconda.org/thoba/confil/badges/version.svg)](https://anaconda.org/thoba/confil)

:no_entry_sign: :construction: **For in-house use**

`confil` parses a [kraken2](https://ccb.jhu.edu/software/kraken2/) report and determines contamination based on a specified cutoff.

## Requirements

- kraken2

## Up and running

```sh
$ git clone https://github.com/COMBAT-TB/confil.git
...
$ cd confil
$ virtualenv envname
$ source envname/bin/activate
$ pip install -r requirements.txt
$ python setup.py install
$ confil --help
$ confil --threads 1 --paired --cutoff 80 fastq_1.fastq fastq_2.fastq
```
