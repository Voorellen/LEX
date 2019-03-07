#This is a Nipype generator. Warning, here be dragons.
#!/usr/bin/env python

import sys
import nipype
import nipype.pipeline as pe

import nipype.interfaces.io as io
import nipype.interfaces.utility as utility

#Generic datagrabber module that wraps around glob in an
io_DataGrabber = pe.Node(io.DataGrabber(infields=["subj_id", "field_template"], outfields=["func", "struct"]), name = 'io_DataGrabber')
io_DataGrabber.inputs.template = '*'
io_DataGrabber.inputs.base_directory = '/project/3018028.06/LEX_ELLEN/data/'
io_DataGrabber.inputs.template_args =  dict(func=[['subj_id', 'subj_id']])
io_DataGrabber.inputs.field_template = dict(func='%d/func/%d_s1_r1.nii')

#Basic interface class generates identity mappings
utility_IdentityInterface = pe.Node(utility.IdentityInterface(fields=["subject", "session", "run_no"]), name='utility_IdentityInterface', iterfield = ['subject'])
utility_IdentityInterface.iterables = [('subject', [50, 99])]

#Create a workflow to connect all those nodes
analysisflow = nipype.Workflow('MyWorkflow')
analysisflow.connect(utility_IdentityInterface, "subject", io_DataGrabber, "subj_id")

#Run the workflow
plugin = 'MultiProc' #adjust your desired plugin here
plugin_args = {'n_procs': 1} #adjust to your number of cores
analysisflow.write_graph(graph2use='flat', format='png', simple_form=False)
analysisflow.run(plugin=plugin, plugin_args=plugin_args)
