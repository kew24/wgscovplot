#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import exists
from pathlib import Path
from typer.testing import CliRunner
from wgscovplot.cli import app

runner = CliRunner()

dirpath = Path(__file__).parent
input_ref = dirpath/'data/nCoV-2019.reference.fasta'
input_genbank = dirpath/'data/sequence_sars_cov2.gb'
input_dir = dirpath/'tools'


def test_cli():
    assert input_ref.exists()
    assert input_genbank.exists()
    result = runner.invoke(app)
    assert result.exit_code != 0
    assert 'Error: Missing option' in result.output
    help_result = runner.invoke(app, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output
    with runner.isolated_filesystem():
        out_html = 'wgscovplot.html'
        test_result = runner.invoke(app, ['--input-dir', str(input_dir),
                                          '--ref-seq', str(input_ref.absolute()),
                                          '--genbank', str(input_genbank.absolute()),
                                          '--gene-feature'])
        assert test_result.exit_code == 0
        assert exists(out_html)
