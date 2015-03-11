# vsc-module-dependencies

Utilities to check dependencies and reverse dependencies of module files.

Usage
-----
Add the `bin` directory to your `PATH` variable.

Execute dep_graph, e.g.,
```bash
$ dep_graph  --dir module_dir  zlib/1.2.8-foss-2015a  
```
This will compute the dependencies of this particular zlib module.  Here, `module_dir` is
the directory that contains the module directories.

```bash
$ dep_graph  --dir module_dir  --reverse  zlib/1.2.8-foss-2015a
```
This will compute the reverse dependencies, i.e., all modules that depend on this `zlib` module.
