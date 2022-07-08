# WComm
Python API for wireless transmission and reception of data. Currently,
this allows sending data through the following channels:
 - Sound (`SoundChannel`)

Also, the following types of baseband modulations are implemented:
 - 256-FSK (`FSK256`)
 - 16-FSK (`FSK16`)

# How to run
## Main program
In order to run the main program, starting from the base directory (`wcomm-py`) navigate to the `src` directory and run
```
py -m wcomm [-E/-R] <FILENAME> <PARAMETERS>
```

In order to run as emitter, use the `-E` flag, where `<FILENAME>` will
be the file that is sent; for the receiver, use the `-R` flag, where
`<FILENAME>` will be the output file.

## Examples
To run the examples, starting from the base directory navigate to `src`
and run
```
py -m wcomm -e <EXAMPLE_NAME>
```

More examples can be added by throwing them into the `examples` submodule,
where each example should have the following structure:
```
wcomm
|- examples
|  |- new_example
|  |  |- __init__.py
|  |  |- main.py
```

The file `main.py` should contain a function `main()`, which will be 
called when running the example.
