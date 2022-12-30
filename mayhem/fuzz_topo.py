#!/usr/bin/env python3


import atheris
import sys
import fuzz_helpers
import json
import io
from contextlib import contextmanager
import random

with atheris.instrument_imports(include=['topojson']):
    import topojson

from json import JSONDecodeError
@contextmanager
def nostdout():
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    yield
    sys.stdout = save_stdout
    sys.stderr = save_stderr

@atheris.instrument_func
def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        with nostdout():
            data = json.loads(fdp.ConsumeRemainingString())
            topojson.Topology(data)
    except (JSONDecodeError):
        return -1
    except TypeError as e:
        if 'object must be' in str(e):
            return -1
        raise
    except AttributeError:
        if random.random() > .99:
            raise
        return -1

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
