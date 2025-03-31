import unittest
from unittest.mock import MagicMock
from ipfilter import ipfilter_by_subnets_func

class TestIpFilterBySubnetsFunc(unittest.TestCase):
    def test_ips_in_and_outside_specific_subnets(self):
        # Predefined random subnets
        subnets = [
            '192.168.0.0/24', '10.0.0.0/8', '172.16.0.0/12', '192.168.1.0/24', '203.0.113.0/24',
            '198.51.100.0/24', '192.0.2.0/24', '8.8.8.0/24', '1.1.1.0/24', '100.64.0.0/10'
        ]
        print(f"Testing with subnets: {subnets}")  # Verbose message

        # Predefined random IPs inside the subnets
        inside_ips = [
            {"ip_column": "192.168.0.1"},  # Inside 192.168.0.0/24
            {"ip_column": "10.1.1.1"},     # Inside 10.0.0.0/8
            {"ip_column": "172.16.5.5"},   # Inside 172.16.0.0/12
            {"ip_column": "192.168.1.100"},  # Inside 192.168.1.0/24
            {"ip_column": "203.0.113.50"},  # Inside 203.0.113.0/24
            {"ip_column": "198.51.100.25"},  # Inside 198.51.100.0/24
            {"ip_column": "192.0.2.10"},    # Inside 192.0.2.0/24
            {"ip_column": "8.8.8.8"},       # Inside 8.8.8.0/24
            {"ip_column": "1.1.1.1"},       # Inside 1.1.1.0/24
            {"ip_column": "100.64.1.1"}     # Inside 100.64.0.0/10
        ]
        print(f"Inside IPs: {inside_ips}")  # Verbose message

        # Predefined random IPs outside the subnets
        outside_ips = [
            {"ip_column": "192.167.255.255"},  # Outside 192.168.0.0/24
            {"ip_column": "11.0.0.1"},         # Outside 10.0.0.0/8
            {"ip_column": "172.32.0.1"},       # Outside 172.16.0.0/12
            {"ip_column": "192.168.2.1"},      # Outside 192.168.1.0/24
            {"ip_column": "203.0.114.1"},      # Outside 203.0.113.0/24
            {"ip_column": "198.51.101.1"},     # Outside 198.51.100.0/24
            {"ip_column": "192.0.3.1"},        # Outside 192.0.2.0/24
            {"ip_column": "9.9.9.9"},          # Outside 8.8.8.0/24
            {"ip_column": "2.2.2.2"},          # Outside 1.1.1.0/24
            {"ip_column": "101.65.0.1"}        # Outside 100.64.0.0/10
        ]
        print(f"Outside IPs: {outside_ips}")  # Verbose message

        # Mock the Visidata sheet
        mock_sheet = MagicMock()
        mock_sheet.cursorCol.name = "ip_column"

        # Combine inside and outside IPs into rows
        rows = inside_ips + outside_ips

        # Generate the filter function using ipfilter_by_subnets_func
        filter_func = ipfilter_by_subnets_func(subnets)
        print("Filter function generated successfully.")  # Verbose message

        # Apply the filter function to each row and store the results
        selected_rows = {id(row): filter_func(row, mock_sheet) for row in rows}

        # Assert that the filter correctly selects rows with IPs inside the subnets
        for row in inside_ips:
            with self.subTest(ip=row["ip_column"]):
                self.assertTrue(
                    selected_rows[id(row)],
                    f"IP {row['ip_column']} should be selected."
                )
                print(f"PASS: IP {row['ip_column']} correctly selected.")  # Verbose message

        # Assert that the filter correctly deselects rows with IPs outside the subnets
        for row in outside_ips:
            with self.subTest(ip=row["ip_column"]):
                self.assertFalse(
                    selected_rows[id(row)],
                    f"IP {row['ip_column']} should not be selected."
                )
                print(f"PASS: IP {row['ip_column']} correctly not selected.")  # Verbose message


if __name__ == "__main__":
    unittest.main()
