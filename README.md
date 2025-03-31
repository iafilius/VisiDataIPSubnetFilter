# IP Subnet selection Filter Plugin for VisiData row selection based on specific IP in selected column

This implements:
- A Visidata plugin 'z| python expression'
- Uses the selected column with `ipaddress`
- Creates a dynamic function with a given list of CIDR network ranges
- Selects the rows which are inside the given network ranges

In case you have session/firewall logging and you want to know which IP destinations point to a specific site (with one or more CIDR address ranges hosted), you can do that exactly.
You can, of course, treat a CIDR as a string and then try to match it as a string, which quickly becomes inaccurate when CIDR isn't a class A, B, or C network. This solution is exact.

## Implements
- Implemented `ipfilter_by_subnets_func` function for filtering rows based on given IP subnets and column ipaddress.
- Added unit tests in `test_ipfilter.py` to test some ranges.

## Install

For general installation, see [Visidata plugin](https://www.visidata.org/docs/plugins/).

My method tested followed the manual installation:
- Make a plugins directory: ```mkdir -p ~/.visidata/plugins```
- Copy the plugin Python file there: ```cp ipfilter.py ~/.visidata/plugins/```
- Add a line to your ```~/.visidatarc``` to import the plugin: ```import plugins.ipfilter```
- Install the dependencies for the plugin (if any). (Use the same pip/python as VisiData is using.)

## Usage

Once installed:
- Start from the menu: System -> Python -> exec()... and execute to create a dynamically generated `filter_func`.
- The function generates a dynamic filter with given CIDRs as inside/outside selection criteria:
  - ```filter_func = plugins.ipfilter.ipfilter_by_subnets_func(['192.168.0.0/24', '10.0.0.0/8', '172.16.0.0/12', '203.0.113.0/24', '198.51.100.0/24'])```
  - With that, `filter_func()` is available for usage in `z| python expression`.
- Select the column that holds IP addresses where you want to make the selection based on.
- Perform: ```z| filter_func(row, sheet)```
  - This will result in selected rows, which you can work with for further (manual selection/analyzing).

## TODO
- Add more test cases for edge cases.
- Optimize performance for large datasets.
- Include shortcuts to prevent typing long paths to the methods.
- Consider more complex setups where you may want to use multiple columns.

