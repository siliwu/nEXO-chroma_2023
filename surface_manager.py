#!/usr/bin/env python

from chroma.geometry import Surface
from chroma.geometry import DichroicProps
from chroma.geometry import SiPMEmpiricalProps # Sili: added on 0403/2023 to include the SiPM empirical package
import chroma.geometry
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
#Manage the surface optical model (of the SiPM and other)? Mainly using model 0 which is the standard Fresnel

		# sipm_name = 'FBK HD3'
		# sipm = Surface(sipm_name, model = 0)
		# sipm.set('detect', 1) #?

		# self.surfaces = {} #
		# self.surfaces[sipm_name] = sipm #
class surface_manager:
	def __init__(self, material_manager):
		# self.surface_data_path = '/home/chroma/chroma_fresh_start/data_files/surface_props.csv'
		# self.surface_data_path = '/home/chroma/chroma_fresh_start/results/data/copperplates_06.23.2022/surface_props_copperplates_06232022.csv'
		# self.surface_data_path = '/home/chroma/chroma_fresh_start/results/data/beam_direction_06.30.2022/surface_props_copperplates_06302022.csv'
		# self.surface_data_path = '/home/chroma/chroma_fresh_start/results/data/silica_window_07.18.2022/surface_props_silica_window_07182022.csv'
		# self.surface_data_path = '/home/chroma/chroma_fresh_start/results/data/source_copperholder_08.16.2022/surface_props_sourceCu_holder_08162022.csv'
		# self.surface_data_path = '/home/chroma/chroma_fresh_start/results/data/copper_gasket_08.29.2022/surface_props_coppergasket_08292022.csv'
		# self.surface_data_path = '/home/chroma/chroma_fresh_start/results/data/Al_filler_02.07.2023/surface_props__Alfiller_02072023.csv'
		# self.surface_data_path ='/home/chroma/chroma_fresh_start/results/data/sourcepart_05.11.2023/surface_props__sourcepart_05112023.csv'
		# self.surface_data_path ='/home/chroma/chroma_fresh_start/results/data/Sebastian_teflon_05.12 .2023/surface_props__Sebastian_teflon_0512.csv'
		# self.surface_data_path = '/home/chroma/chroma_fresh_start/results/data/Sebastian_teflon_05.23.2023/surface_props__Sebastian_teflon_0523.csv'
		# self.surface_data_path = '/home/chroma/chroma_fresh_start/results/data/Sebastian_teflon_upperlimit_06.05.2023/surface_props__Sebastian_teflon_upper_0605.csv'
		self.surface_data_path = '/home/chroma/chroma_fresh_start/results/data/Sebastian_flippedsource_06.06.2023/surface_props__Sebastian_teflon_FS_0606.csv'
		self.SiPMAOIref_path = '/home/chroma/chroma_fresh_start/data_files/FBK.csv'
		self.mat_manager = material_manager
		self.mat_manager = material_manager
		self.wavelengths = chroma.geometry.standard_wavelengths		
		self.num_wavelengths = len(self.wavelengths)
		#print(self.wavelengths)
		self.build_surfaces()

	def build_surfaces(self):
		self.surfaces_df = pd.read_csv(self.surface_data_path)

		self.surfaces = {}
		for index, row in self.surfaces_df.iterrows():
			curr_name = row['name']
			curr_inner_mat_name = row['inner_mat']
			curr_outer_mat_name = row['outer_mat']
			curr_model_id = row['model_id']
			# print('current id is', curr_model_id)
			curr_reflect_specular = row['reflect_specular']
			curr_reflect_diffuse = row['reflect_diffuse']

			if curr_model_id == 0:
				curr_surface = Surface(curr_name, model = curr_model_id)
				curr_surface.set('detect', 1.0)


			elif curr_model_id == 3:
				curr_surface = self.create_dichroic_surface(curr_name, curr_inner_mat_name, curr_outer_mat_name)
			elif curr_model_id == 4:
				curr_surface = self.create_dielectric_metal_surface(curr_name, curr_inner_mat_name)
				# print(curr_surface)
			#Sili: added on 11/17/2022 to build a killing surface
			elif curr_model_id == 8:
				curr_surface = Surface(curr_name, model = 0)
				# Photon will be killed(absorbed) when reaching the surface
				curr_surface.set('absorb', 1)
			#below try to include the SiPM empirical surface
			elif curr_model_id ==5:
				curr_surface = self.SiPMEmpirical_surface(curr_name)
			# for teflon
			elif curr_model_id ==9:
				curr_surface = Surface(curr_name, model = 0)
			else:
				curr_surface = None

			if curr_surface is not None:
				curr_surface.set('reflect_specular', curr_reflect_specular)
				curr_surface.set('reflect_diffuse', curr_reflect_diffuse)

			self.surfaces[curr_name] = curr_surface

	def get_surface(self, surface_name):
		if surface_name == 'None':
			return None
		elif surface_name in self.surfaces:
			return self.surfaces[surface_name]
		else:
			raise Exception('Surface does not exist: ' + surface_name)


	def create_dielectric_metal_surface(self, name, inner_mat):
		dielectric_metal_surface = Surface(name, model = 4)
		eta2 = self.mat_manager.material_props[inner_mat]['eta']
		k2 = self.mat_manager.material_props[inner_mat]['k']
		dielectric_metal_surface.set('eta', eta2)
		dielectric_metal_surface.set('k', k2)

		return dielectric_metal_surface

	def SiPMEmpirical_surface(self, name):
		# print('model 5')

		sipmEmpirical_surface = Surface(name, model = 5)

		self.SiPMreflctivity = pd.read_csv(self.SiPMAOIref_path)
		# num_angle = 90

		# inci_theta_deg = np.linspace(0,90,num_angle,dtype = np.float32)
		# inci_theta = np.radians(inci_theta_deg)

		ref = []
		rela_PDE = []
		inci_theta_csv = self.SiPMreflctivity['AOI'].tolist()
		inci_theta = np.radians(inci_theta_csv)
		ref_csv = self.SiPMreflctivity['reflectivity'].tolist()


		for i in range(0,len(inci_theta_csv)):
			r_SiPM = np.zeros((self.num_wavelengths, 2), dtype = np.float32)
			r_SiPM[:, 0] = self.wavelengths
			# r_SiPM[:, 1] = random.random()
			r_SiPM[:,1] = ref_csv[i]
			# print(r_SiPM[:,1])
			ref.append(r_SiPM)
			relative_PDE = np.zeros((self.num_wavelengths, 2), dtype = np.float32)
			relative_PDE[:, 0] = self.wavelengths
			relative_PDE[:, 1] =1.0			
			rela_PDE.append(relative_PDE)

		# for i in range(0,num_angle):
		# 	r_SiPM = np.zeros((self.num_wavelengths, 2), dtype = np.float32)
		# 	r_SiPM[:, 0] = self.wavelengths
		# 	# r_SiPM[:, 1] = random.random()
		# 	r_SiPM[:,1] = abs(0.02*i)
		# 	ref.append(r_SiPM)
		# 	relative_PDE = np.zeros((self.num_wavelengths, 2), dtype = np.float32)
		# 	relative_PDE[:, 0] = self.wavelengths
		# 	relative_PDE[:, 1] =1.0			
		# 	rela_PDE.append(relative_PDE)



		SiPM_props = SiPMEmpiricalProps(inci_theta,ref,rela_PDE)
		sipmEmpirical_surface.sipmEmpirical_props = SiPM_props

		return sipmEmpirical_surface

	def create_dichroic_surface(self, name, inner_mat, outer_mat):
		print('model 3 here')
		dichroic_surface = Surface(name, model = 3)
		n1 = self.mat_manager.material_props[outer_mat]['refractive_index']
		#Sili: the eta2 and k2 are randomize with some uncertainty
		eta2 = self.mat_manager.material_props[inner_mat]['eta']+random.uniform(-self.mat_manager.material_props[inner_mat]['abs(eta_error)'],self.mat_manager.material_props[inner_mat]['abs(eta_error)'])
		k2 = self.mat_manager.material_props[inner_mat]['k']+random.uniform(-self.mat_manager.material_props[inner_mat]['abs(k_error)'],self.mat_manager.material_props[inner_mat]['abs(k_error)'])
		# print(eta2,k2)
		#Sili
		self.get_eta2_k2(eta2, k2)
		theta, reflectance, transmittance = self.calc_R_T(n1, eta2, k2, num_angles = 500)
		R = []
		T = []
		for idx in range(len(theta)):
			curr_R = np.zeros((self.num_wavelengths, 2), dtype = np.float32)
			curr_R[:, 0] = self.wavelengths
			# curr_R[:, 1] = reflectance[idx]
			curr_R[:, 1] = 1
			R.append(curr_R)

			curr_T = np.zeros((self.num_wavelengths, 2), dtype = np.float32)
			curr_T[:, 0] = self.wavelengths
			curr_T[:, 1] = 0
			# curr_T[:, 1] = transmittance[idx]
			T.append(curr_T)
		# print('theta', len(theta))
		# print('reflectance',R)
		print('R list length',len(R))
		# print('transmittance',T)
		dichroic_props = DichroicProps(theta, R, T)
		dichroic_surface.dichroic_props = dichroic_props
		return dichroic_surface


	def calc_R_T(self, n1, eta2, k2, num_angles):
		n2 = np.complex(eta2, k2)
		theta_deg = np.linspace(0, 90, num_angles, dtype = np.float32)
		theta = np.radians(theta_deg)
		def r_s(theta):
			numerator   = n1 * np.cos(theta) - n2 * np.sqrt(1 - np.square(n1 * np.sin(theta) / n2))
			denominator = n1 * np.cos(theta) + n2 * np.sqrt(1 - np.square(n1 * np.sin(theta) / n2))
			return np.divide(numerator, denominator)

		def R_s(theta):
			rs = r_s(theta)
			return np.square(np.absolute(rs))

		def r_p(theta):
			numerator   = n1 * np.sqrt(1 - np.square(n1 * np.sin(theta) / n2)) - n2 * np.cos(theta)
			denominator = n1 * np.sqrt(1 - np.square(n1 * np.sin(theta) / n2)) + n2 * np.cos(theta)
			return np.divide(numerator, denominator)

		def R_p(theta):
			rp = r_p(theta)
			return np.square(np.absolute(rp))

		def R(theta):
			return 0.5 * (R_s(theta) + R_p(theta))

		reflectance = R(theta)
		transmittance = np.zeros(len(reflectance), dtype = np.float32)
		# absorption = 1 - reflectance
		# print('the reflectance and transmittance are', reflectance, transmittance)
		return (theta, reflectance, transmittance)
#Sili:
	def get_eta2_k2(self, eta2, k2):
		self.eta2 = eta2 
		self.k2 = k2
		# print('the updated eta2 and k2 are', self.eta2, self.k2)
		return (self.eta2, self.k2)
		