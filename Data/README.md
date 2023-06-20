## Data Folder Instructions

Go to this Data folder in the terminal. Download the Tesla data from the [Link](https://drive.google.com/u/0/uc?id=1LKPKo0b5XxPOK8GQNgwwnWsw9uzftyxR&export=download)

To Unzip and store data in the `Tesla_raw` folder, use the two commands mentioned below.

```
zip -FF P3Data.zip --out Tesla_raw.zip -fz
```
```
unzip Tesla_raw.zip
```
```
rm P3Data.zip Tesla_raw.zip
```

Ensure you are inside the Data folder and run the following script to convert Tesla raw video data to frames. The processed files will be stored to `Tesla_proc` folder.
```
python3 generate_frames_tesla.py
```