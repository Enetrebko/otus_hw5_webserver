# Simple webserver based on threads

### Parameters

    -w  threads count, default=5
    -r  documents root, default=root

### Run example

    python httpd.py -w 5 -r root

### AB Testing Results

10 threads:

````
Concurrency Level:      100
Time taken for tests:   147.180 seconds
Complete requests:      50000
Failed requests:        0
Total transferred:      4650000 bytes
HTML transferred:       0 bytes
Requests per second:    339.72 [#/sec] (mean)
Time per request:       294.361 [ms] (mean)
Time per request:       2.944 [ms] (mean, across all concurrent requests)
Transfer rate:          30.85 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1  93.7      0   19581
Processing:     1    2  16.9      1    2483
Waiting:        1    2  16.9      1    2483
Total:          1    3  95.2      2   19584

Percentage of the requests served within a certain time (ms)
  50%      2
  66%      2
  75%      2
  80%      2
  90%      3
  95%      3
  98%      4
  99%      4
 100%  19584 (longest request)
 ````
  
  
50 threads:

````
Concurrency Level:      100
Time taken for tests:   135.323 seconds
Complete requests:      50000
Failed requests:        0
Total transferred:      4650000 bytes
HTML transferred:       0 bytes
Requests per second:    369.49 [#/sec] (mean)
Time per request:       270.645 [ms] (mean)
Time per request:       2.706 [ms] (mean, across all concurrent requests)
Transfer rate:          33.56 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1  61.2      0   13189
Processing:     1    2  15.7      1    1682
Waiting:        1    2  15.6      1    1682
Total:          1    3  63.2      2   13192

Percentage of the requests served within a certain time (ms)
  50%      2
  66%      2
  75%      2
  80%      2
  90%      3
  95%      3
  98%      4
  99%      5
 100%  13192 (longest request)
````