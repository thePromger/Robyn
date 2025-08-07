import sys

import nox


@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13"])
def tests(session: nox.Session):
    # print(session.python)
    # return
    session.install("uv", "maturin", "-U")
    # uv_export = "uv export --no-hashes --group dev --group test -o deps.txt --no-install-project"
    uv_export = "uv export --no-hashes --group dev --group test -o deps.txt --no-install-project"
    uv_pip_install = "uv pip sync deps.txt"

    session.run(*uv_export.split(" "))
    session.run(*uv_pip_install.split(" "))

    # maturin_build = "maturin develop"
    maturin_build = "maturin pep517 build-wheel --editable -o dist"

    if sys.platform == "darwin":
        session.run("rustup", "target", "add", "x86_64-apple-darwin")
        session.run("rustup", "target", "add", "aarch64-apple-darwin")
        maturin_build += " --target universal2-apple-darwin"

    session.run(*maturin_build.split(" "))
    session.run("uv", "pip", "install", "--no-index", "--find-links=dist/", "robyn")
    session.run("pytest")


@nox.session(python=["3.11"])
def lint(session):
    session.run("uv", "pip", "install", "black", "ruff")
    session.run("black", "robyn/", "integration_tests/")
