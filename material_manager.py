#!/usr/bin/env python

from chroma.geometry import Material

import pandas as pd
import random

# read materials from database
# randomize functionality

class material_manager:
	def __init__(self,run_id):
		# self.material_data_path = '/home/chroma/chroma_fresh_start/data_files/bulk_materials.csv'
		# self.material_data_path = '/home/chroma/chroma_fresh_start/results/data/copperplates_06.23.2022/bulk_materials _copperplates_06232022.csv'
		# self.material_data_path = '/home/chroma/chroma_fresh_start/results/data/beam_direction_06.30.2022/bulk_materials _copperplates_06302022.csv'
		# self.material_data_path = '/home/chroma/chroma_fresh_start/results/data/silica_window_07.18.2022/bulk_materials _silica_window_07182022.csv'
		# self.material_data_path = '/home/chroma/chroma_fresh_start/results/data/source_copperholder_08.16.2022/bulk_materials __sourceCu_holder_08162022.csv'
		# self.material_data_path = '/home/chroma/chroma_fresh_start/results/data/copper_gasket_08.29.2022/bulk_materials _coppergasket_08292022.csv'
		# self.material_data_path = '/home/chroma/chroma_fresh_start/results/data/Al_filler_02.07.2023/bulk_materials _Alfiller_02072023.csv'
		# self.material_data_path = '/home/chroma/chroma_fresh_start/results/data/sourcepart_05.11.2023/bulk_materials _sourcepart_05112023.csv'
		# self.material_data_path ='/home/chroma/chroma_fresh_start/results/data/Sebastian_teflon_05.12 .2023/bulk_materials _Sebastian_teflon_0512.csv'
		# self.material_data_path = '/home/chroma/chroma_fresh_start/results/data/Sebastian_teflon_05.23.2023/bulk_materials _Sebastian_teflon_0523.csv'
		# self.material_data_path = '/home/chroma/chroma_fresh_start/results/data/Sebastian_teflon_upperlimit_06.05.2023/bulk_materials _Sebastian_teflon_upper_0605.csv'
		self.material_data_path = '/home/chroma/chroma_fresh_start/results/data/Sebastian_flippedsource_06.06.2023/bulk_materials _Sebastian_teflon_FS_0606.csv'
		self.run_id = run_id
		self.build_materials(run_id)
		self.global_material = self.materials['liquid xenon']

	def add_attributes(self,
				curr_material,
				refractive_index = None,
				absorption_length = None,
				scattering_length = None,
				density = 0.0):
		#set the optical index grabbed from csv file for simulation
		curr_material.set('refractive_index', refractive_index) 
		curr_material.set('absorption_length', absorption_length) 
		curr_material.set('scattering_length', scattering_length)
		curr_material.density = density

		# print(refractive_index)
		# return refractive_index

	def build_materials(self,run_id):
		# read in the csv file into dataframe
		self.materials_df = pd.read_csv(self.material_data_path)
		#print(self.materials_df)
		# iterate through all materials and create Material object, store into dictionary of materials
		self.materials = {}
		self.material_props = {}
		properties = self.materials_df.columns
		for index, row in self.materials_df.iterrows():
			curr_name = row['name'] #name of the material		
			self.materials[curr_name] = Material(name = curr_name)	
			# row['refractive_index'] = row['refractive_index'] + random.uniform(-row['abs(r_i_error)'],row['abs(r_i_error)'])
			# if curr_name == 'liquid xenon':
			# 	row['refractive_index'] = row['refractive_index']+0.01*run_id
			# 	print(row['refractive_index'])
			self.add_attributes(self.materials[curr_name],
								# refractive_index = r_i,
								# refractive_index = row['refractive_index']+random.uniform(-row['abs(r_i_error)'],row['abs(r_i_error)']), # only used when no surface model is defined
								refractive_index = row['refractive_index'],
								absorption_length = row['absorption_length'],
								scattering_length = row['scattering_length'],
								density = row['density'])

			self.material_props[curr_name] = dict(row)
			# print()
			# try to update the real refractive_index to the csv. file
		# print(self.materials)



	def get_material(self, material_name):
		# check to see if material exists. if not, throw exception
		if material_name in self.materials:
			return self.materials[material_name]
		else:
			raise Exception('Material does not exist: ' + material_name)