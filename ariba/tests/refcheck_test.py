import unittest
import os
import filecmp
import pyfastaq
from ariba import refcheck

modules_dir = os.path.dirname(os.path.abspath(refcheck.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data')


class TestRefcheck(unittest.TestCase):
    def test_check_pass(self):
        '''test check file OK'''
        infile = os.path.join(data_dir, 'refcheck_test_check_ok.fa')
        c = refcheck.Checker(infile)
        self.assertEqual(c.run(), (True, None, None))


    def test_check_file_fail_not_gene(self):
        '''test check file fail not a gene'''
        infile = os.path.join(data_dir, 'refcheck_test_check_not_gene.fa')
        c = refcheck.Checker(infile)
        seq = pyfastaq.sequences.Fasta('gene1', 'TTGTGATGA')
        self.assertEqual(c.run(), (False, 'Not a gene', seq))


    def test_check_file_fail_too_short(self):
        '''test check file fail short gene'''
        infile = os.path.join(data_dir, 'refcheck_test_check_too_short.fa')
        c = refcheck.Checker(infile, min_length=10)
        seq = pyfastaq.sequences.Fasta('gene1', 'TTGTGGTGA')
        self.assertEqual(c.run(), (False, 'Too short', seq))


    def test_check_file_fail_too_long(self):
        '''test check file fail long gene'''
        infile = os.path.join(data_dir, 'refcheck_test_check_too_long.fa')
        c = refcheck.Checker(infile, max_length=6)
        seq = pyfastaq.sequences.Fasta('gene1', 'TTGTGGTGA')
        self.assertEqual(c.run(), (False, 'Too long', seq))


    def test_check_file_fail_spades_in_name(self):
        '''test check file with sequence that has spaces in its name'''
        infile = os.path.join(data_dir, 'refcheck_test_check_spaces_in_name.fa')
        c = refcheck.Checker(infile, min_length=3)
        seq = pyfastaq.sequences.Fasta('gene foo', 'TTGTGGTGA')
        self.assertEqual(c.run(), (False, 'Name has spaces', seq))


    def test_check_file_fail_duplicate_name(self):
        '''test check file with sequence that has two genes with the same name'''
        infile = os.path.join(data_dir, 'refcheck_test_check_duplicate_name.fa')
        c = refcheck.Checker(infile, min_length=3)
        seq = pyfastaq.sequences.Fasta('gene1', 'TTGTGGTGA')
        self.assertEqual(c.run(), (False, 'Duplicate name', seq))


    def test_check_run_with_outfiles(self):
        '''test run when making output files'''
        infile = os.path.join(data_dir, 'refcheck_test_fix_in.fa')
        tmp_prefix = 'tmp.refcheck_test_fix.out'
        c = refcheck.Checker(infile, min_length=10, max_length=25, outprefix=tmp_prefix)
        c.run()
        for x in ['fa', 'log', 'rename', 'removed.fa']:
            expected = os.path.join(data_dir, 'refcheck_test_fix_out.' + x)
            got = tmp_prefix + '.' + x
            self.assertTrue(filecmp.cmp(expected, got, shallow=False))
            os.unlink(got)
