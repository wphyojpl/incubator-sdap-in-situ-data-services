# Benchmark Testing

## About

Run benchmark testing against a in-situ data service server and collect statistics/meta-data about the response. Currently, two benchmark tests are available: time and pagination.

Time benchmark test makes a single request to the server and collects the statistics such as  response size and duration. On the other hand, pagination benchmark test would traverse pagination link from response all the way to the end of the pagination, and collect statistics along the way.

## Execute Benchmark Testing

### Prerequisite

1. python 3.6.13 is installed available on the [path](http://www.linfo.org/path_env_var.html) (linfo.org)

### Examples

**Run pagintion test and save the statistics in a csv file**

```bash
python bench_mark.py \
    --output-file '~/pagination_test_depth_-10_10_bbox_-30_-20_-20_10.csv' \
    --benchmark 'pagination_benchmark' \
    --host 'doms.jpl.nasa.gov' --provider 'NCAR' --project 'ICOADS Release 3.0' --platform-code 30 41 42 \
    --date-time '2017-07-03T01:00:00Z' '2017-07-16T23:00:00Z' \
    --depth -10 10 \
    --bbox -30 -20 -20 -10
```

**Run 5x time test and save the statistics in a csv file**

```bash
for i in 1 2 3 4 5; do
    python bench_mark.py \
        --output-file "~/ncar_time_depth_-3_3_bbox_-30_-20_-20_-10_test_0$i.csv" \
        --benchmark'time_benchmark' \
        -host 'cdms.ucar.edu' --provider 'NCAR' --project 'ICOADS Release 3.0' --platform-code 30 41 42 \
        --date-time '2017-11-'$(echo $i | sed -e 's/^.\{1,1\}$/0&/')'T01:00:00Z' '2017-11-'$(echo $i | sed -e 's/^.\{1,1\}$/0&/')'T02:00:00Z' \
        --depth -3 3 \
        --bbox -30 -20 -20 -10
done
```
