# Popsugar Code Quiz
My solution to the Popsugar code challenge. The code is written in python. You can run it from the project directory using:
 
 ```
./popsugar.py
```

You will need an internet connection to download the log file. You can also have the code print out plotable data by running:

```
./popsugar.py --plot
```

# Results

The code ignores malformed log lines (of which there are a few). For the rest it uses a regular expression to process the lines. The HTTP stats codes are in the table below:

| Code | Count |
| ------ | ----------- |
| 200 | 49410 |
| 304 | 2221 |
| 204 | 1886 |
| 499 | 1051 |
| 301 | 896 |
| 302 | 532 |
| 403 | 411 |
| 206 | 237 |
| 502 | 68 |
| 404 | 43 |
| 410 | 13 |
| 400 | 12 |
| 500 | 5 |
| 503 | 4 |

Here is a plot of these results.

![Status code histogram](https://github.com/mksachs/popsugar/blob/master/plot/http_status_codes.png "Status code histogram.")

The top 10 process times (in seconds) are listed below:

| Rank | Time (s) |
|---|---|
| 1 | 299.97 |
| 2 | 299.697 |
| 3 | 298.515 |
| 4 | 298.131 |
| 5 | 297.846 |
| 6 | 297.508 |
| 7 | 296.69 |
| 8 | 291.005 |
| 9 | 290.617 |
| 10 | 288.285 |

Also, below is a plot of the cumulative frequency of process times in the file. This type of frequency plot is useful for determining trends in complex data sets.

![Cumulative frequency process time](https://github.com/mksachs/popsugar/blob/master/plot/cumu_freq_proc_time.png "Cumulative frequency process time.")
