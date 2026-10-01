"""End-to-End CLI tests using Click CliRunner."""

from click.testing import CliRunner

from app.cli.main import cli


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "gst-reconciler" in result.output


def test_cli_reconcile():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "reconcile",
            "--source-a",
            "demo/data/gstr2b_sample.xlsx",
            "--source-b",
            "demo/data/purchase_register_sample.xlsx",
        ],
    )
    assert result.exit_code == 0
    assert "RECONCILIATION SUMMARY" in result.output
    assert "Total Processed" in result.output
    assert "Matched (Within Tolerance)" in result.output
