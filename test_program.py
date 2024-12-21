import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
from pathlib import Path
import subprocess
from io import StringIO
from main import *


class TestGitDependencyGraph(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_git_commit_dependencies_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="commit_hash1\nfile1.txt\nfile2.txt\ncommit_hash2\nfolder1\n", stderr="")

        repo_path = 'git_repo'
       

    @patch('subprocess.run')
    def test_get_git_commit_dependencies_fail(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stderr="git error")

        with self.assertRaises(RuntimeError):
            get_git_commit_dependencies('git_repo')

    def test_generate_graphviz_code(self):
        dependencies = {
            "commit1": {"file1", "folder1"},
            "commit2": {"file2"}
        }
        graph_code = generate_graphviz_code(dependencies)


    @patch('builtins.open', new_callable=MagicMock)
    def test_save_graph_to_file(self, mock_open):
        graph_code = "digraph G { commit1 -> file1 }"
        temp_output_path = Path(tempfile.mktemp())

        save_graph_to_file(graph_code, temp_output_path)

        mock_open.assert_called_once_with(temp_output_path, 'w')

    @patch('subprocess.run')
    def test_main_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="commit_hash1\nfile1.txt\ncommit2\nfolder1\n", stderr="")

        with patch('sys.argv', ['main.py', '--repo-path', '/some/repo/path', '--graphviz-path', '/usr/bin/dot', '--output-path', 'output.dot']):
            with patch('builtins.print') as mock_print:
                main()


    @patch('subprocess.run')
    def test_main_fail(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stderr="git error")

        with patch('sys.argv', ['main.py', '--repo-path', '/some/repo/path', '--graphviz-path', '/usr/bin/dot', '--output-path', 'output.dot']):
            with patch('builtins.print') as mock_print:
                main()



if __name__ == '__main__':
    unittest.main()
#python -m unittest test_program.py