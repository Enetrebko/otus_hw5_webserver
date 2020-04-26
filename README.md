# Simple webserver based on threads

### Parameters

    -w  threads count, default=5
    -r  documents root, default=root

### Run example

    python httpd.py -w 5 -r root

### AB Testing Results

5 threads:

````
Concurrency Level:      100
Time taken for tests:   113.310 seconds  
Complete requests:      50000  
Failed requests:        4  
   (Connect: 2, Receive: 2, Length: 0, Exceptions: 0)  
Total transferred:      4649814 bytes  
HTML transferred:       0 bytes  
Requests per second:    441.27 [#/sec] (mean)  
Time per request:       226.621 [ms] (mean)  
Time per request:       2.266 [ms] (mean, across all concurrent requests)  
Transfer rate:          40.07 [Kbytes/sec] received  
  
Connection Times (ms)  
                min  mean[+/-sd] median   max  
Connect:        0    1  92.1      0   19553  
Processing:     0    1 164.4      0   26016  
Waiting:        0    0   5.6      0    1248  
Total:          0    2 188.5      0   26016  

Percentage of the requests served within a certain time (ms)
  50%      0
  66%      0
  75%      0
  80%      0
  90%      1
  95%      1
  98%      1
  99%      1
 100%  26016 (longest request)`
 ````
  
  
10 threads:

````
Concurrency Level:      100
Time taken for tests:   106.862 seconds
Complete requests:      50000
Failed requests:        2
   (Connect: 1, Receive: 1, Length: 0, Exceptions: 0)
Total transferred:      4649907 bytes
HTML transferred:       0 bytes
Requests per second:    467.90 [#/sec] (mean)
Time per request:       213.723 [ms] (mean)
Time per request:       2.137 [ms] (mean, across all concurrent requests)
Transfer rate:          42.49 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1 126.7      0   20459
Processing:     0    1 116.9      0   25957
Waiting:        0    0  14.2      0    2245
Total:          0    2 172.4      0   25957

Percentage of the requests served within a certain time (ms)
  50%      0
  66%      0
  75%      0
  80%      1
  90%      1
  95%      1
  98%      1
  99%      1
 100%  25957 (longest request)
````