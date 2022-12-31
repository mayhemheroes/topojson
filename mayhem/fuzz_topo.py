#!/usr/bin/env python3


import atheris
import sys
import fuzz_helpers
import json
import random

with atheris.instrument_imports(include=['topojson']):
    import topojson

from json import JSONDecodeError

@atheris.instrument_func
def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        with fdp.ConsumeMemoryFile(all_data=True, as_bytes=False) as f:
            data = json.load(f)
            topojson.Topology(data)
    except (JSONDecodeError, ImportError):
        return -1
    except AttributeError:
        if random.random() > .99:
            raise
        return -1

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
