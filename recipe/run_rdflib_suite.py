import sys
from subprocess import call

FAIL_UNDER = 48
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


if __name__ == "__main__":
    sys.exit(
        # run the tests
        do(*COV, *RUN, *PYTEST, *K, *M, "test")
        # ... then maybe run coverage
        or do(*COV, *REPORT)
    )
