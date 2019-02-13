# confil

[![Build Status](https://travis-ci.org/COMBAT-TB/confil.svg?branch=master)](https://travis-ci.org/COMBAT-TB/confil)

:no_entry_sign: :construction: **for in-house use**

Contamination Filter

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
