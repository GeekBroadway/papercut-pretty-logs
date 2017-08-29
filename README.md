# Pretty Print Logs

This is a small python script to turn monthly .csv files into pretty html output. Included is the python script as well as a sample index.html file.


# Requirements
    Python 3.* (2.* will not work)
    
# Usage

Download this repo and place your log files into the rawLogs folder. Open up the script and replace the first line with the name of the log file, excluding .csv

```python
printer_in_file = "papercut-print-log-2017-08"
```

Then simply run the script. It will produce the output HTML in output/ as well as JSON files in processed.

