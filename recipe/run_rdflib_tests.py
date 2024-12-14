import sys
from subprocess import call

FAIL_UNDER = "83"
COV = ["coverage"]
RUN = ["run", "--source=rdflib", "--branch", "-m"]
PYTEST = ["pytest", "-vv", "--color=yes", "--tb=long"]
REPORT = ["report", "--show-missing", "--skip-covered", f"--fail-under={FAIL_UNDER}"]

SKIPS = [
    # https://github.com/conda-forge/rdflib-feedstock/pull/30   dep issues
    "definednamespace_creator",
    # https://github.com/conda-forge/rdflib-feedstock/pull/33   dep issues
    "berkeleydb",
    # https://github.com/conda-forge/rdflib-feedstock/pull/35   runtime pip install issues
    "test_plugins and (test_sparqleval or test_parser)",
]

SKIP_OR = " or ".join(SKIPS)
K = ["-k", f"not ({SKIP_OR})"]


if __name__ == "__main__":
    sys.exit(
        # run the tests
        call([*COV, *RUN, *PYTEST, *K])
        # maybe run coverage
        or call([*COV, *REPORT])
    )
