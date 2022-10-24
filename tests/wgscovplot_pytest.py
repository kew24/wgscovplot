#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import exists
from pathlib import Path
from typer.testing import CliRunner
from wgscovplot.cli import app

runner = CliRunner()

dirpath = Path(__file__).parent
input_ref = dirpath / 'data/nCoV-2019.reference.fasta'
input_genbank = dirpath / 'data/sequence_sars_cov2.gb'
input_dir1 = dirpath / 'data/non_segment_virus'
input_dir2 = dirpath / 'data/segment_virus'


def test_basic_cli():
    result = runner.invoke(app)
    assert result.exit_code != 0
    assert 'Error' in result.output
    assert "Missing argument" in result.output
    help_result = runner.invoke(app, ['--help'])
    assert help_result.exit_code == 0
    assert 'wgscovplot version' in help_result.output


def test_cli_non_segment_virus():
    assert input_ref.exists()
    assert input_genbank.exists()
    with runner.isolated_filesystem():
        out_html = 'wgscovplot_test1.html'
        test_result = runner.invoke(app, [str(input_dir1.resolve().absolute()),
                                          '--output-html', out_html,
                                          '--no-gene-feature',
                                          '--no-amplicon'])
        assert test_result.exit_code == 0
        assert exists(out_html)

    with runner.isolated_filesystem():
        out_html = 'wgscovplot_test2.html'
        test_result = runner.invoke(app, [str(input_dir1.resolve().absolute()),
                                          '--output-html', out_html,
                                          '--no-gene-feature',
                                          '--amplicon'])
        assert test_result.exit_code == 0
        assert exists(out_html)

    with runner.isolated_filesystem():
        out_html = 'wgscovplot_test3.html'
        test_result = runner.invoke(app, [str(input_dir1.resolve().absolute()),
                                          '--output-html', out_html,
                                          '--gene-feature',
                                          '--no-amplicon'])
        assert test_result.exit_code == 0
        assert exists(out_html)

    with runner.isolated_filesystem():
        test_result = runner.invoke(app, [str(input_dir1.resolve().absolute())])
        assert test_result.exit_code == 0
        assert exists('wgscovplot.html')


def test_cli_segment_virus():
    with runner.isolated_filesystem():
        out_html = 'wgscovplot_test_segment_virus.html'
        test_result = runner.invoke(app, [str(input_dir2.resolve().absolute()),
                                          '--segment-virus',
                                          '--output-html', out_html])
        assert test_result.exit_code == 0
        assert exists(out_html)