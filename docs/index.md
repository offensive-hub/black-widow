# Welcome to black-widow Documentation

For full documentation visit [docs.black-widow.io](https://docs.black-widow.io).

## Commands


> #### GUI
>> * `black-widow -g, --gui` - Run **black-widow** with **Web GUI**.


> #### CMD
> **Sniffing**
>> * `black-widow --pcap` - Starts packet sniffing
>>  * `--pcap-src FILE` - Input file to sniff
>>  * `--pcap-dest FILE` - Output .pcap file
>>  * `--pcap-int INTERFACES` - Interfaces to sniff (eg. `"eth0,wlan0"`)
>>  * `--pcap-limit INT` - Max packet field length
>>  * `--pcap-count INT` - Max packets to sniff
>
> **SQL Injection**
>> * `black-widow --sql` - Starts sql injection
>>  * `--sql-url URL` - The url where search for forms
>>  * `--sql-deep` - Crawl the website in search for forms
>>  * `--sql-depth INT` - Max crawling depth



## Project layout
```
[root]
  |
  |-- app/              # Main application package
  |    |
  |    |-- arguments/       # User input arguments parser (100%)
  |    |
  |    |-- attack/          # Attack modality package (0%)
  |    |-- defense/         # Defense modality package (0%)
  |    |
  |    |-- gui/             # Graphical User Interface package (100%)
  |    |
  |    |-- helpers/         # Helper methods package (100%)
  |    |
  |    |-- managers/        # Managers package
  |    |    |
  |    |    |-- cluster/        # Cluster managers package (0%)
  |    |    |-- crypto/         # Encryption managers package (70%)
  |    |    |-- injection/      # Injection managers package (60%)
  |    |    |-- parser/         # Parser managers package (100%)
  |    |    |-- request/        # Request managers package (70%)
  |    |    |-- sniffer/        # Sniffer managers package (95%)
  |    |
  |    |-- services/        # Services package
  |    |    |
  |    |    |-- logger.py       # Logger service (100%)
  |    |    |-- multitask.py    # MultiTask service (100%)
  |    |    |-- serializer.py   # PickleSerializer and JsonSerializer serivces (100%)
  |    |
  |    |-- storage/         # Storage directory
  |    |
  |    |-- env.py           # Environment variables management
  |
  |-- .env              # Environment variables
  |
  |-- black-widow.py    # Main executable
```
