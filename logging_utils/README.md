# Utility Parser for SONIC-2 Baseline.
The primary purpose of the logging infrastructure is to track SONIC-2
builds and log references to `git`, `wget` and `pip` operations.  This is
done by instrumenting the SONIC-2 Baseline:

1. `/etc/pip.conf` is updated in `sonic-slave-stretch` to log all `pip`
operations.
2. Wrappers are placed around `git` and `wget` to log all their operations.

There are two modes of logging:

1. Generation of `sonic-slave-stretch`, where the logs are stored in
`/sonic_logs`, and must be copied out after the container is built.
2. During a build of `target/sonic-broadcom.bin`, where they are
written directly to the `~/sonic` directory.

There are 6 different logfiles generated:

1. `db_git_log.txt` - `git` log during Docker build of `<sonic-slave-stretch>`
2. `db_wget_log.txt` - `wget` log during Docker build of `<sonic-slave-stretch>`
3. `db_pip_install_log.txt` - `pip` log during Docker build of `<sonic-slave-stretch>`
4. `rt_git_log.txt` - `git` log during Docker build of `~/target/sonic-broadcom`
5. `rt_wget_log.txt` - `wget` log during Docker build of `~/target/sonic-braodcom`
6. `rt_pip_install_log.txt` - `pip` log during Docker build of `~/target/sonic-broadcom`

Typically, after running the builds, a good practice would be placing all logs in
a directory such as `<sonic-buildimage/logs>` in prepartion for the parser utility
to process them.

## Log Parser

The log parser is a simple utility which parses the logs generated during the
build process, as well as allows some basic search options of the SONIC-2 
source tree to find these references.  This is designed to help make changes
to the baseline to remove external references to source modules being built,
migrating them into stable, internal storage.

The basic options are as follows:

```
parse_sonic_logs.py  -h

Help Options:
 
(-t:) treeRoot: <None>
(-s:) searchTreeRoot: <None>
(-l:) logFileRoot: <logs>
(-g) gitReport: False
(-w) wgetReport: False
(-p) pipReport: False
(-n) humanReadable False
(-i:) inFile <None>
(-f) Use Full (https://xx.xx/component> path in search <False>
(-b) Only search Docker.* *.mk and *akefile* [False]
```

Some examples of how this is used are:

```
#  Generate a list of all 'git' references.
#
parse_sonic_logs.py -t ./sonic-buildimage -g  > git_ref.txt

#  Generate a list of all 'wget' references.
#
parse_sonic_logs.py -t ./sonic-buildimage -w  > wget_ref.txt

#  Search the tree for all 'get' references, specifyig the
#  entire path minues the 'https://' (-f) in the search string.
#  and only search '*akefile', 'Dockerfile*' and '*.mk' (-b)
#  files in the search.
#
#  Note that <git_ref.txt> was generated from command shown
#  above.
#
parse_sonic_logs.py -t ./sonic-buildimage/src -b -f -g -i git_ref.txt 
```
