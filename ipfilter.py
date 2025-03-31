#!/usr/bin/env python3

"""
This script provides a function to filter rows in a Visidata sheet based on IP subnets.

Usage in Visidata:
1. Import the script:
   :py from ipfilter import filter_by_subnet

2. Apply the filter as a selection:
   :select filter_by_subnet(['192.168.1.0/24', '10.0.0.0/8'])
   This will select rows where the currently selected column contains an IP in the specified subnets.

3. Save the filtered data if needed:
   :w filtered_output.csv
"""

import ipaddress
from visidata import vd  # Import Visidata's debug/logging functionality

__author__ = "Arjan Filius"
__version__ = "1.0.0"
__license__ = "MIT"

vd.debug(f"Plugin 'ipfilter' version {__version__} by {__author__} loaded.")  # Startup message


def ipfilter_by_subnets_func(subnets):
    """
    Returns a callable filter function for use with the 'z|' method in Visidata.
    The function checks if the IP in the currently selected column belongs to any of the given subnets.

    Args:
        subnets (list): A list of subnets in CIDR notation (e.g., ['192.168.1.0/24', '10.0.0.0/8']).

    Returns:
        A callable filter function that evaluates to True or False for each row.

    Usage:
        1. Import the function in Visidata:
           :py from ipfilter import ipfilter_by_subnets_func

        2. Generate the filter function for the desired subnets:
           :py filter_func = ipfilter_by_subnets_func(['192.168.1.0/24', '10.0.0.0/8'])

        3. Apply the filter using the 'z|' method:
           :z| filter_func(row, sheet)

        4. The rows where the IP in the selected column belongs to the specified subnets will be selected.

    Workflow Example:
        1. Open a dataset in Visidata (e.g., a CSV file with an IP address column):
           $ vd dataset.csv

        2. Navigate to the column containing IP addresses.

        3. Run the following commands in Visidata:
           a. Import the function:
              :py from ipfilter import ipfilter_by_subnets_func

           b. Generate the filter function for the desired subnets:
              :py filter_func = ipfilter_by_subnets_func(['192.168.1.0/24', '10.0.0.0/8'])

           c. Apply the filter using the 'z|' method:
              :z| filter_func(row, sheet)

        4. The rows where the IP in the selected column belongs to the specified subnets will now be selected.

        5. Optionally, save the filtered rows to a new file:
           :w filtered_output.csv
    """
    try:
        # Parse the subnets into ipaddress network objects, and only once
        networks = [ipaddress.ip_network(subnet) for subnet in subnets]
        vd.debug(f"Parsed networks for z| filter: {networks}")  # Debug information for Visidata
    except ValueError as e:
        raise ValueError(f"Invalid subnet in list: {subnets}") from e

    def filter_function(row, sheet):
        try:
            # Extract the IP address from the selected column
            ip = row[sheet.cursorCol.name]
            ip_obj = ipaddress.ip_address(ip)
            # Check if the IP belongs to any of the networks
            return any(ip_obj in network for network in networks)
        except (ValueError, KeyError, AttributeError) as e:
            vd.debug(f"Error processing row: {e}")  # Debug information for Visidata
            return False

    vd.debug(f"Filter function created for subnets: {subnets}")  # Debug information for Visidata
    return filter_function