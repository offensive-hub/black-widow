# Welcome to MkDocs

For full documentation visit [docs.black-widow.io](https://docs.black-widow.io).

## Commands


#### GUI
* `black-widow -g, --gui` - Run **black-widow** with **Web GUI**.


#### CMD

##### Sniffing
* `black-widow --pcap` - Starts packet sniffing
  * `--pcap-src FILE` - Input file to sniff
  * `--pcap-dest FILE` - Output .pcap file
  * `--pcap-int INTERFACES` - Interfaces to sniff (eg. `"eth0,wlan0"`)
  * `--pcap-limit INT` - Max packet field length
  * `--pcap-count INT` - Max packets to sniff

##### SQL Injection
* `black-widow --sql` - Starts sql injection
  * `--sql-url URL` - The url where search for forms
  * `--sql-deep` - Crawl the website in search for forms
  * `--sql-depth INT` - Max crawling depth



## Project layout
    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
