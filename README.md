# Project Title

Local backup is a simple script to backup desired directories and files to a secondary local location. Given desired directories, non-desired directories, non-desired files and a backup location, the script is systemetically check if these files are present and remove or copy those of interest.

## Getting Started

### Installing

Clone repository with the following command:
```
git clone https://github.com/finnhittson/local_backup.git
```

### Executing program

* How to run the program
* Step-by-step bullets
Once cloned, open the `backup.py` file under `src` and edit lines 9, 10, and 11 to your liking. Once modified, backup your files with the following command.
```
python backup.py --backup-loc="E"
```
`--backup-loc` is the name of the backup location. In this instances it is an external thumb drive named `E`.

