# ndx-ecg Extension for NWB

This extension is developed to extend NWB data standards to incorporate ECG recordings. CardiacSeries, the base neurotype in this extension, in fact extends the basic type of NWB TimeSeries and can be stored in three specific data interfaces of ECG, HeartRate and AuxiliaryAnalysis. Also, the ECGChannelsGroup is another neurotype in this module which extends an NWB container and stores recording channels information along with the electrodes implementation and a link to another extended neurotype which extends the type Device -named ECGRecDevice. 

## Installation
simply navigate to the root directory and
```
pip install .

```

## Test
After the installation to test the integration to PyNWB, simply run a test_script provided in 
```
\src\pynwb\tests

```
