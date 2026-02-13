import shutil
import sys

from subprocess import call
from pathlib import Path


FAIL_UNDER = 45
SKIP_MARKERS = [
    # https://github.com/conda-forge/rdflib-feedstock/pull/42
    "webtest",  # flakes out most days
    "testcontainer",  # needs docker
]
SKIPS = [
    # https://github.com/conda-forge/rdflib-feedstock/pull/30
    "definednamespace_creator",  # dep issues
    # https://github.com/conda-forge/rdflib-feedstock/pull/33
    "berkeleydb",  # dep issues
    # https://github.com/conda-forge/rdflib-feedstock/pull/35
    "test_plugins and (test_sparqleval or test_parser)",  # runtime pip install issues
    # https://github.com/conda-forge/rdflib-feedstock/pull/42
    "test_rdf4j",  # uses weird fixtures
]

SRC_DIR = Path(__file__).parent / "src"

UNLINKS = [
    # https://github.com/conda-forge/rdflib-feedstock/pull/43
    ## needs docker, apparently
    "test/test_graphdb/",
]

COV = ["coverage"]
RUN = ["run", "--source=rdflib", "--branch", "-m"]
PYTEST = ["pytest", "-vv", "--color=yes", "--tb=long"]
REPORT = ["report", "--show-missing", "--skip-covered", f"--fail-under={FAIL_UNDER}"]


SKIP_OR = " or ".join(SKIPS)
K = ["-k", f"not ({SKIP_OR})"]

if SKIP_MARKERS:
    M_OR = " or ".join(SKIP_MARKERS) if len(SKIP_MARKERS) > 1 else SKIP_MARKERS[0]
    M = ["-m", M_OR]


def do(*args: str) -> int:
    print("\t".join(args), flush=True)
    return call(args, cwd="src")


def unlink() -> int:
    rc = 0
    for filename in sorted(UNLINKS):
        path = SRC_DIR / filename
        sys.stderr.write(f"... removing {path}\n")
        if path.is_dir():
            sys.stderr.write(f"""  ... and {len([*path.rglob("*")])} children\n""")
            shutil.rmtree(path)
        elif path.is_file():
            path.unlink()
        else:
            sys.stderr.write(f"!!! not found: {path}\n")
            rc += 1
    return rc


if __name__ == "__main__":
    sys.exit(
        # clean up undiscoverable test files
        unlink()
        # run the tests
        or do(*COV, *RUN, *PYTEST, *K, *M, "test")
        # ... then maybe run coverage
        or do(*COV, *REPORT)
    )
