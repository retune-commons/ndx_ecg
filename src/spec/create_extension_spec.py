# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import (NWBNamespaceBuilder, export_spec,
                        NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec, NWBLinkSpec)


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""This extension is developed to extend NWB data standards to incorporate ECG recordings.""",
        name="""ndx-ecg""",
        version="""0.1.0""",
        author=list(map(str.strip, """Hamidreza Alimohammadi ([AT]DefenseCircuitsLab)""".split(','))),
        contact=list(map(str.strip, """alimohammadi.hamidreza@gmail.com""".split(',')))
    )

    # TODO: specify the neurodata_types that are used by the extension as well
    # as in which namespace they are found.
    # this is similar to specifying the Python modules that need to be imported
    # to use your new data types.
    # all types included or used by the types specified here will also be
    # included.
    ns_builder.include_type('TimeSeries', namespace='core')
    ns_builder.include_type('DynamicTable', namespace='hdmf-common')
    ns_builder.include_type('Device', namespace='core')
    ns_builder.include_type('NWBDataInterface', namespace='core')
    ns_builder.include_type('NWBContainer', namespace='core')


    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information
    cardiac_series = NWBGroupSpec(
        neurodata_type_def='CardiacSeries',
        neurodata_type_inc='TimeSeries',
        doc='A group to store standardized cardiac time-series, e.g., ECG and HeartRate, including '
            'acquisitions, processed cardiac series or auxiliary analysis.',
        attributes=[
            NWBAttributeSpec(
                name='process_level',
                doc='Indicate whether the time-series is a raw acquisition or '
                    'have already been processed; If processed, then describe the details.',
                dtype='text',
                required=False
            )
        ],
        datasets=[
            NWBDatasetSpec(
                name='data',
                dtype='numeric',
                doc='Associated cardiac-series data. Note that in general, this data could be a numerical array,'
                    'the columns of which corresponding to the recording channels, indexed similarly as the rows '
                    'of the dynamic table passed for the channels argument. Notice the difference between electrodes '
                    'table and the recording channels.',
                attributes=[
                    NWBAttributeSpec(
                        name='unit',
                        dtype='text',
                        doc='Default measurement unit of the corresponding cardiac-series.'
                    ),
                    NWBAttributeSpec(
                        name='conversion',
                        dtype='float32',
                        value=1,
                        doc='Global conversion factor for corresponding cardiac-series. See also channel_conversion. '
                            'finally, the stored data-set for each channel will be returned in default unit using '
                            'the scaling as: data-in-default-unit = data * conversion * channel_conversion.'
                    )
                ]
            ),
            NWBDatasetSpec(
                name='channel_conversion',
                dtype='float32',
                quantity='?',
                doc='Conventional NWB channel-specific conversion factor. Default value would be 1. '
                    'See also conversion. Finally, the stored data-set for each channel will be returned in '
                    'default unit using the scaling as: '
                    'data-in-default-unit = data * conversion * channel_conversion.',
                attributes=[
                    NWBAttributeSpec(
                        name='axis',
                        dtype='int32',
                        value=1,
                        doc='Zero-indexed axis of the data that the channel-specific conversion factor corresponds to.'
                    )
                ]
            )
        ],
        links=[
            NWBLinkSpec(
                name='ECG_channels_group',
                target_type='ECGChannelsGroup',
                doc='Link to the ECGChannelsGroup as a reference for recording channels, recording electrodes '
                    'and the recording device.'
            )
        ]
    )

    ecg_series = NWBGroupSpec(
        neurodata_type_def='ECG',
        neurodata_type_inc='NWBDataInterface',
        default_name='ECG',
        doc='Specific data interface for ElectroCardioGram time-series (raw/processed).',
        attributes=[
            NWBAttributeSpec(
                name='processing',
                doc='Explain how the time-series is processed or whether it is a raw acquisition.',
                dtype='text',
                required=False
            )
        ],
        groups=[
            NWBGroupSpec(
                neurodata_type_inc='CardiacSeries',
                doc='CardiacSeries object representing the ElectroCardioGram (ECG). Whether raw or processed.',
                quantity='+'
            )
        ]
    )

    hr_series = NWBGroupSpec(
        neurodata_type_def='HeartRate',
        neurodata_type_inc='NWBDataInterface',
        default_name='HeartRate',
        doc='Specific data interface for HeartRate.',
        attributes=[
            NWBAttributeSpec(
                name='processing',
                doc='Explain how the time-series is processed or whether it is a raw acquisition.',
                dtype='text',
                required=False
            )
        ],
        groups=[
            NWBGroupSpec(
                neurodata_type_inc='CardiacSeries',
                doc='CardiacSeries object representing the HearRate (HR). Whether raw or processed.',
                quantity='+'
            )
        ]
    )

    aux_analysis = NWBGroupSpec(
        neurodata_type_def='AuxiliaryAnalysis',
        neurodata_type_inc='NWBDataInterface',
        default_name='AuxiliaryAnalysis',
        doc='Specific data interface for whatever relevant auxiliary in-between analysis.',
        attributes=[
            NWBAttributeSpec(
                name='processing',
                doc='Explain how the analysis is processed.',
                dtype='text',
                required=False
            )
        ],
        groups=[
            NWBGroupSpec(
                neurodata_type_inc='CardiacSeries',
                doc='CardiacSeries object representing the auxiliary analysis.',
                quantity='+'
            )
        ]
    )

    ecg_recording_channels = NWBGroupSpec(
        neurodata_type_def='ECGChannelsGroup',
        neurodata_type_inc='NWBContainer',
        doc='Information of all channels from which the corresponding CardiacSeries is generated. Note that these '
            'channels can represent single recording electrodes or differential recordings.',
        attributes=[
            NWBAttributeSpec(
                name='group_description',
                doc='Describe the recording channels for this specific experiment session.',
                dtype='text',
                required=False
            )
        ],
        datasets=[
            NWBDatasetSpec(
                name='data',
                neurodata_type_inc='DynamicTable',
                doc='This would be the dynamic table of the recording channels, also including a reference '
                    'to the electrodes.',
                attributes=[
                    NWBAttributeSpec(
                        name='description',
                        dtype='text',
                        doc='Describe the dynamic table representing the channels being recorded.'
                    )
                ]
            )
        ],
        links=[
            NWBLinkSpec(
                name='ECG_recording_device',
                target_type='ECGRecDevice',
                doc='Link to the ECGRecDevice used to record cardiac signals.'
            )
        ]
    )

    ecg_recording_device = NWBGroupSpec(
        neurodata_type_def='ECGRecDevice',
        neurodata_type_inc='Device',
        doc='ECG recording device.',
        attributes=[
            NWBAttributeSpec(
                name='filtering',
                doc='Explain analogue frequency filtering of the ECG acquisition device, '
                    'if any is implemented.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='gain',
                doc='Explain the gain settings of the ECG acquisition device.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='offset',
                doc='Explain what the baseline of the ECG signal is set to.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='synchronization',
                doc='Explain the synchronization settings if the ECG recording device is separately connected to '
                    'another recording system.',
                dtype='text',
                required=False
            )
        ],
        links=[
            NWBLinkSpec(
                name='endpoint_recording_device',
                target_type='Device',
                doc='endpoint recording device to which the ECG recording device is connected.'
            )
        ]
    )


    # TODO: add all of your new data types to this list
    new_data_types = [cardiac_series, ecg_series, hr_series, aux_analysis,
                      ecg_recording_channels, ecg_recording_device]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)
    print('Spec files generated. Please make sure to rerun `pip install .` to load the changes.')


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()
