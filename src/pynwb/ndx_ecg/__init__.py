import os
from pynwb import load_namespaces, get_class

# Set path of the namespace.yaml file to the expected install location
ndx_ecg_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-ecg.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_ecg_specpath):
    ndx_ecg_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-ecg.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_ecg_specpath)

# TODO: import your classes here or define your class using get_class to make
# them accessible at the package levels
CardiacSeries = get_class('CardiacSeries', 'ndx-ecg')
ECG = get_class('ECG', 'ndx-ecg')
HeartRate = get_class('HeartRate', 'ndx-ecg')
AuxiliaryAnalysis = get_class('AuxiliaryAnalysis', 'ndx-ecg')
ECGChannelsGroup = get_class('ECGChannelsGroup', 'ndx-ecg')
ECGRecDevice = get_class('ECGRecDevice', 'ndx-ecg')