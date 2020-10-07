# Unix Domain Socket benchmark

**Hardware**:

* OS: macOS V10.15.6
* CPU: 2.6 GHz Intel Core i7
* Memory: 16 GB 2400 MHz DDR4
* Type: stream

| Number of Workers | Data | Epoch | Duration |
| --- | --- | --- | --- |
| 1 | 800 * 800 * 3 (uint8) | 1000 | 21.32s |
| 4 | 800 * 800 * 3 (uint8) | 1000 | 30.64s |
| 8 | 800 * 800 * 3 (uint8) | 1000 | 45.42s |