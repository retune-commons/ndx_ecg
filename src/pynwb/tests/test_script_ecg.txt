from datetime import datetime
from uuid import uuid4
import numpy as np
from dateutil.tz import tzlocal
from pynwb import NWBHDF5IO, NWBFile

from hdmf.common import DynamicTable
from hdmf.common.table import DynamicTableRegion

from ndx_ecg import CardiacSeries, ECG, HeartRate, AuxiliaryAnalysis, ECGChannelsGroup, ECGRecDevice

nwb_file = NWBFile(
    session_description='ECG test-rec session',
    identifier=str(uuid4()),
    session_start_time=datetime.now(tzlocal()),
    experimenter='experimenter',
    lab='DCL',
    institution='UKW',
    experiment_description='',
    session_id='',
)

# define an endpoint global recording device
main_recording_device = nwb_file.create_device(
    name='name of the main_device',
    description='description of the main_device',
    manufacturer='manufacturer of the main_device'
)

# define an ECGRecDevice-type device for ecg recording
ecg_device = ECGRecDevice(
    name='ECGRecDevice',
    description='description of the ecg_rec_device',
    manufacturer='manufacturer of the ecg_rec_device',
    filtering='notch-60Hz-analog',
    gain='100',
    offset='0',
    synchronization='taken care of via ...',
    endpoint_recording_device=main_recording_device
)

'''
creating an ECG electrodes table
as a DynamicTable
'''
ecg_electrodes_table = DynamicTable(
    name='ecg_electrodes',
    description='info on ECG electrodes'
)

# add relevant columns
ecg_electrodes_table.add_column(
    name='electrode_name',
    description='reference name of the corresponding electrode'
)
ecg_electrodes_table.add_column(
    name='electrode_location',
    description='the location of the corresponding electrode on the body'
)
ecg_electrodes_table.add_column(
    name='electrode_info',
    description='descriptive information on the corresponding electrode'
)

# add electrodes
ecg_electrodes_table.add_row(
    electrode_name='el_0',
    electrode_location='right upper-chest',
    electrode_info='descriptive info'
)
ecg_electrodes_table.add_row(
    electrode_name='el_1',
    electrode_location='left lower-chest',
    electrode_info='descriptive info'
)
ecg_electrodes_table.add_row(
    electrode_name='reference',
    electrode_location='top of the head',
    electrode_info='descriptive info'
)

'''
creating an ECG recording channels table
as a DynamicTable
'''
recording_channels_table = DynamicTable(
    name='recording_channels',
    description='info on ecg recording channels'
)

# add relevant columns
recording_channels_table.add_column(
    name='channel_name',
    description='reference name of the corresponding recording channel'
)
recording_channels_table.add_column(
    name='channel_type',
    description='type of the recording, e.g., single electrode or differential'
)
recording_channels_table.add_column(
    name='electrodes',
    description='descriptive information the corresponding electrode(s)'
)

# add channels
recording_channels_table.add_row(
    channel_name='ch_0',
    channel_type='single',
    electrodes=DynamicTableRegion(
        name='',
        data=[0],
        table=ecg_electrodes_table,
        description=''
    )
)
recording_channels_table.add_row(
    channel_name='ch_1',
    channel_type='differential',
    electrodes=DynamicTableRegion(
        name='',
        data=[0, 1],
        table=ecg_electrodes_table,
        description=''
    )
)

ecg_channels_group = ECGChannelsGroup(
    name='',
    group_description='',
    data=recording_channels_table,
    ECG_recording_device=ecg_device
)

#
#
# an example of storing the ECG data
dum_data_ecg = np.random.randn(20, 2)
dum_time_ecg = np.linspace(0, 10, len(dum_data_ecg))
ecg_cardiac_series = CardiacSeries(
    name='ecg_raw',
    process_level='raw',
    data=dum_data_ecg,
    timestamps=dum_time_ecg,
    unit='volts',
    ECG_channels_group=ecg_channels_group
)

ecg_raw = ECG(cardiac_series=ecg_cardiac_series)
nwb_file.add_acquisition(ecg_raw)  # adding the raw acquisition of ECG to the nwb_file inside an 'ECG' container


# an example of storing the HeartRate data
dum_data_hr = np.random.randn(10, 2)
dum_time_hr = np.linspace(0, 10, len(dum_data_hr))
hr_cardiac_series = CardiacSeries(
    name='heart_rate',
    process_level='processed',
    data=dum_data_hr,
    timestamps=dum_time_hr,
    unit='bpm',
    ECG_channels_group=ecg_channels_group
)

# defining an ecg_module to store the processed cardiac data and analysis
ecg_module = nwb_file.create_processing_module(
    name='cardio_module',
    description='a module to store processed cardiac data'
)

hr = HeartRate(cardiac_series=hr_cardiac_series)
ecg_module.add(hr)  # adding the heart rate data to the nwb_file inside an 'HeartRate' container


# an example of storing the Auxiliary data
# An example could be the concept of ceiling that is being used in the literature published by DCL@UKW
dum_data_ceil = np.random.randn(10, 2)
dum_time_ceil = np.linspace(0, 10, len(dum_data_ceil))
ceil_cardiac_series = CardiacSeries(
    name='heart_rate',
    process_level='auxiliary analysis',
    data=dum_data_ceil,
    timestamps=dum_time_ceil,
    unit='bpm',
    ECG_channels_group=ecg_channels_group
)

ceil = AuxiliaryAnalysis(cardiac_series=ceil_cardiac_series)
ecg_module.add(ceil)  # adding the 'ceiling' auxiliary analysis to the nwb_file inside an 'AuxiliaryAnalysis' container

# an example of storing the processed heart rate
# An example could be the concept of HR2ceiling that is being used in the literature published by DCL@UKW
dum_data_hr2ceil = np.random.randn(10, 2)
dum_time_hr2ceil = np.linspace(0, 10, len(dum_data_hr2ceil))
hr2ceil_cardiac_series = CardiacSeries(
    name='heart_rate',
    process_level='processed',
    data=dum_data_hr2ceil,
    timestamps=dum_time_hr2ceil,
    unit='bpm',
    ECG_channels_group=ecg_channels_group
)

hr2ceil = HeartRate(name='HR2Ceil', cardiac_series=hr2ceil_cardiac_series)
ecg_module.add(hr2ceil)  # adding the 'HR2ceiling' processed HR to the nwb_file inside an 'HeartRate' container



