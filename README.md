# ReTomb

ReTomb is an automated approach to reproducing tombstones from native crash reports for Android applications.

## 1. Introduction 

ReTomb takes a native crash report as input and returns the result of reproducing tombstones as output. We introduce the dataset and source code for the ReTomb.

## 2. Details of the Dataset

The `DataSet` directory  includes our experimental data:

- **Project information**: 66 projects from top-180 Android open-source projects in GitHub.
- **Native crash report**: 34 native crash reports from randomly selected 400 reports.
- **Training dataset**: 1816 out of 2216 native crash reports.
- **Test dataset**: 34 native crash reports.

## 3. Requirements

- Windows 10

- Android Studio Giraffe | 2022.3.1 Patch 1

- Android emulator (Android 7.0-12.0)

- Android Debug Bridge (ADB)

- Python 3.10.9

  - uiautomator=1.0.2

  - gensim=4.3.1

  - scikit-learn=1.3.0

  - spacy=3.7.2

  - request=2.28.2

  - beautifulsoup4=4.12.2
## 4. Run ReTomb on Windows
- Launch Android Studio and Android emulator

- Connect ADB service

- In the `Crash Reports Analysis` directory, including several scripts to preprocess native crash reports and get activity:

  - `getNativeCrash.py`: get native crash reports from GitHub.
  
  - `GetMainActivity.py`: get MainActivity for each apk file.
  
  - `ExtractingS2R.py`: extract S2Rs from native crash reports.
  
- In the `API Mapping` directory, including several scripts to map preprocessed S2Rs into API sequences:

  - `getTrainData.py`: get train dataset (1816 native crash reports).
  - `APISim2vec_model.py`: get APISim2vec model.
  - `Steps_APIs.py`: map steps into API sequences.
  
- In the `Script Generation` directory, including several scripts to select APIs the generated API sequences that can be successfully reproduced:

  - `Select APIs.py`: select the commands that can successfully reproduce the tombstone.

  - `evaluation_matrix.py`: evaluate generated tombstone form error signal, error code, abort message, and backtrace.

## 5. Artifact Evaluation

This is the artifact for the paper: ReTomb: Reproducing Tombstones from Native Crash Reports for
Android Applications.

**Result Evaluation**: In the `Artifact-Evaluation`directory. For example, In `Brave_Issue#20268` directory consists of several files:

  - `automatic script template.txt`:  Retomb selected APIs template.
  - `automatic script.bat`: Retomb generates APIs sequence  that can successfully reproduce the tombstone. run the script, and we can get a `tombstone_00`.
  - `tombstone_00`: The output of the script `automatic script.bat`.
  - `readme.txt` The file consists of the environments, APK version, and S2R of  reproducing tombstone.

