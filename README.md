# audioFingerprinting
Vasiliki Rentoula mtn2317

Ilias Alexandropoulos mtn2302

Audio fingerprinting tool using [Dejavu](https://github.com/worldveil/dejavu) library

## Description
This project uses Dejavu library to fingerprint, recognize and remove duplicates from a given directory.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)

## Installation

```bash
git clone https://github.com/IliasAlex/audioFingerprinting.git
```

Also you need to install [MySQL](https://www.mysql.com/downloads/)

or 

```bash
pip install mysqlclient
```

## Usage
```bash
cd audioFingerprinting
python3 -m venv audioF
source audioF/bin/activate
pip install -r requirements.txt
```

## Data
We used a well-known dataset for these tasks. 

Dataset: [FMA](https://github.com/mdeff/fma)

## How to use

- Fingerprinting
```bash
python3 dejavu-test.py -c dejavu.cnf.SAMPLE -f /path/to/dir wav
```
`-c`: Path to config file containing infor about MySQL db.

`-f`: Path to directory of files to fingerprint with extention wav.

- Recognizing
```bash
python3 dejavu-test.py -c dejavu.cnf.SAMPLE -r file /path/to/file 
```
`-c`: Path to config file containing infor about MySQL db.

`-r`: Path to file to recognize.

or instead of `-r` you can use `-yt` to regognize audio from youtube link:

```bash
python3 dejavu-test.py -c dejavu.cnf.SAMPLE -yt "www.youtube.com" 
```

- Find duplicates
```bash
python3 dejavu-test.py -c dejavu.cnf.SAMPLE -d /path/to/directory 
```

`-c`: Path to config file containing infor about MySQL db.

`-d`: Path to directory of files to find duplicates.
