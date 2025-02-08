import unittest
from unittest.mock import patch, MagicMock
import subprocess
from malware_attacks import malware_attack  # Ensure the filename matches your actual script

class TestWeaponization(unittest.TestCase):
    
    def setUp(self):
        self.weapon = malware_attack.Weaponization()

    @patch('subprocess.check_output')
    def test_run_command_success(self, mock_subproc):
        """Test successful command execution."""
        mock_subproc.return_value = b'Command executed successfully'
        result = self.weapon.run_command("echo test")
        self.assertEqual(result, 'Command executed successfully')

    @patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(1, 'echo test'))
    def test_run_command_failure(self, mock_subproc):
        """Test command execution failure."""
        result = self.weapon.run_command("echo test")
        self.assertIsNone(result)

    @patch('subprocess.run')
    def test_execute_script_success(self, mock_subproc):
        """Test successful script execution."""
        mock_subproc.return_value = MagicMock(returncode=0)
        success = self.weapon.execute_script("scripts/keylogger.py")
        self.assertTrue(success)

    @patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, ['python', 'scripts/keylogger.py']))
    def test_execute_script_failure(self, mock_subproc):
        """Test script execution failure after retries."""
        success = self.weapon.execute_script("scripts/keylogger.py")
        self.assertFalse(success)

    @patch.object(malware_attack.Weaponization, 'execute_script', return_value=True)
    def test_deploy_malware_success(self, mock_execute):
        """Test malware deployment when execution succeeds."""
        self.weapon.deploy_malware("keylogger")
        mock_execute.assert_called_once_with("scripts/keylogger.py")

    @patch.object(malware_attack.Weaponization, 'execute_script', return_value=False)
    def test_deploy_malware_failure(self, mock_execute):
        """Test malware deployment failure logging."""
        self.weapon.deploy_malware("keylogger")
        mock_execute.assert_called_once_with("scripts/keylogger.py")

    def test_deploy_malware_invalid_type(self):
        """Test deployment with an invalid attack type."""
        with self.assertLogs(level='ERROR') as log:
            self.weapon.deploy_malware("invalid_type")
        self.assertIn("Attack type 'invalid_type' not recognized.", log.output[-1])

if __name__ == '__main__':
    unittest.main()