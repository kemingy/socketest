# Unix Domain Socket benchmark

**Hardware**:

* OS: Ubuntu 16.04
* CPU: Intel(R) Xeon(R) E5-2620 v3 @ 2.40GHz
* Memory: 16 GB 2133 MHz DDR4
* Type: stream

| Number of Workers | Number of socket | Data | Epoch | Serialize | Duration |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 800 * 800 * 3 (uint8) | 1000 | False | 20.69s |
| 2 | 1 | 800 * 800 * 3 (uint8) | 1000 | False | 22.75s |
| 2 | 2 | 800 * 800 * 3 (uint8) | 1000 | False | 20.56s |
| 4 | 1 | 800 * 800 * 3 (uint8) | 1000 | False | 23.02s |
| 8 | 1 | 800 * 800 * 3 (uint8) | 1000 | False | 25.79s |
