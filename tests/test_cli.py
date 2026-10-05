"""Tests for CLI interface."""

from typer.testing import CliRunner

from ui_sleuth.cli import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Reverse-engineer live web pages" in result.stdout


def test_cli_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.stdout


def test_cli_missing_url():
    result = runner.invoke(app, ["extract"])
    assert result.exit_code != 0
    assert "Missing target URL" in result.stdout
