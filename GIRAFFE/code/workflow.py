#This is a Nipype generator. Warning, here be dragons.
#!/usr/bin/env python

import sys
import nipype
import nipype.pipeline as pe

import nipype.interfaces.io as io
import nipype.interfaces.utility as utility
import nipype.interfaces.fsl as fsl

#Generic datagrabber module that wraps around glob in an
io_DataGrabber = pe.Node(io.DataGrabber(infields=["subj_id", "field_template", "session", "run_no"], outfields=["func", "struct"]), name = 'io_DataGrabber')
io_DataGrabber.inputs.sort_filelist = True
io_DataGrabber.inputs.template = '*'
io_DataGrabber.inputs.base_directory = '/project/3018028.06/LEX_ELLEN/data/'
io_DataGrabber.inputs.template_args =  dict(func=[['subj_id', 'subj_id', 'session', 'run_no']],struct=[['subj_id']])
io_DataGrabber.inputs.field_template = dict(func='%02d/func/%02d_s%d_r%d.nii', struct='%02d/anat/ses-mri01_t1_mprage_*.nii')

#Basic interface class generates identity mappings
utility_IdentityInterface = pe.Node(utility.IdentityInterface(fields=["subject", "session", "run_no"]), name='utility_IdentityInterface', iterfield = ['subject','session','run_no'])
utility_IdentityInterface.iterables = [('subject', [50, 01]),('session', [1, 2]),('run_no', [1, 2, 3, 4])]

#Wraps the executable command ``bet``.
fsl_BET = pe.Node(interface = fsl.BET(), name='fsl_BET')

#Generic datasink module to store structured outputs
io_DataSink = pe.Node(interface = io.DataSink(), name='io_DataSink')
io_DataSink.inputs.base_directory = '/project/3018028.06/LEX_ELLEN/giraffe-results/'

#Wraps the executable command ``mcflirt``.
fsl_MCFLIRT = pe.Node(interface = fsl.MCFLIRT(), name='fsl_MCFLIRT')

#Create a workflow to connect all those nodes
analysisflow = nipype.Workflow('MyWorkflow')
analysisflow.connect(utility_IdentityInterface, "subject", io_DataGrabber, "subj_id")
analysisflow.connect(io_DataGrabber, "struct", fsl_BET, "in_file")
analysisflow.connect(fsl_BET, "out_file", io_DataSink, "brainextraction")
analysisflow.connect(fsl_BET, "mask_file", io_DataSink, "mask")
analysisflow.connect(utility_IdentityInterface, "session", io_DataGrabber, "session")
analysisflow.connect(utility_IdentityInterface, "run_no", io_DataGrabber, "run_no")
analysisflow.connect(io_DataGrabber, "func", fsl_MCFLIRT, "in_file")
analysisflow.connect(fsl_MCFLIRT, "out_file", io_DataSink, "McFlirt")
analysisflow.connect(fsl_MCFLIRT, "mean_img", io_DataSink, "McFlirt_mean")

#Run the workflow
plugin = 'MultiProc' #adjust your desired plugin here
plugin_args = {'n_procs': 1} #adjust to your number of cores
analysisflow.write_graph(graph2use='flat', format='png', simple_form=False)
analysisflow.run(plugin=plugin, plugin_args=plugin_args)
