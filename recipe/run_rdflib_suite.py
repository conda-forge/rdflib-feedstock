import sys
from subprocess import call

FAIL_UNDER = 81
SKIP_MARKERS = [
    # https://github.com/conda-forge/rdflib-feedstock/pull/42   flakes out most days
    "webtest",
]
SKIPS = [
    # https://github.com/conda-forge/rdflib-feedstock/pull/30   dep issues
    "definednamespace_creator",
    # https://github.com/conda-forge/rdflib-feedstock/pull/33   dep issues
    "berkeleydb",
    # https://github.com/conda-forge/rdflib-feedstock/pull/35   runtime pip install issues
    "test_plugins and (test_sparqleval or test_parser)",
    # https://github.com/conda-forge/rdflib-feedstock/pull/42   needs docker
    "test_rdf4j",
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
