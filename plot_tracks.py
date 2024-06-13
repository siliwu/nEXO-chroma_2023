
import pandas as pd
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

# Create a new plot, plot tracks
figure = plt.figure()
axes = mplot3d.Axes3D(figure)
# tracks = np.load('/home/chroma/chroma_fresh_start/results/testing/hd3_tracks_test_0.npy', allow_pickle = True)
# tracks = np.load('/home/chroma/chroma_fresh_start/results/testing/hd3_detrefl_tracks_test_0.npy', allow_pickle = True)
tracks = np.load('/home/chroma/chroma_fresh_start/results/testing/hd3_det_tracks_test_0.npy', allow_pickle = True)
# # tracks = np.load('/home/chroma/chroma_fresh_start/results/testing/hd3_filtered_scatter_tracks_test_0.npy', allow_pickle = True)
# # tracks = np.load('/home/chroma/chroma_fresh_start/results/testing/hd3_filtered_tracks_test_0.npy', allow_pickle = True)
# tracks = np.load('/home/chroma/chroma_fresh_start/results/testing/hd3_filtered_undetected_tracks_test_0.npy', allow_pickle = True)
print(np.shape(tracks))
print(len(tracks))

for i in range(len(tracks)):
	curr_positions = tracks[i]
	axes.plot(curr_positions[:, 0], curr_positions[:, 1], curr_positions[:, 2], color = 'k', linewidth = 1)

# #Reed's rewrite, sometimes work
# figure = plt.figure()
# axes = plt..axe(projection = '3d')
# tracks='track here'
# for i in range(len(tracks[0])):
# 	curr_positions=tracks
# 	axes.plot(curr_positions[:,i,0], curr_positions[:,i,1], curr_positions[:,1,2],color = 'k',linewidth = 1)

# Load the STL files and add the vectors to the plot

# geom_file = '/home/chroma/chroma_fresh_start/data_files/geometry_components.csv'
# geom_file = '/home/chroma/chroma_fresh_start/results/data/copperplates_06.23.2022/geometry_components _copper_plate.csv'
# geom_file = '/home/chroma/chroma_fresh_start/results/data/beam_direction_06.30.2022/geometry_components _copper_plate0630.csv'
# geom_file = '/home/chroma/chroma_fresh_start/results/data/silica_window_07.18.2022/geometry_components _silica_window_07182022.csv'
# geom_file = '/home/chroma/chroma_fresh_start/results/data/source_copperholder_08.16.2022/geometry_components _sourceCu_holder_08162022.csv'
# geom_file = '/home/chroma/chroma_fresh_start/results/data/copper_gasket_08.29.2022/geometry_components _coppergasket_08292022.csv'
# geom_file = '/home/chroma/chroma_fresh_start/results/data/Al_filler_02.07.2023/geometry_components __Alfiller_02072023.csv'
# geom_file = '/home/chroma/chroma_fresh_start/data_files/stl_files/Sebastian/STL 3/stl3.csv'
# geom_file = '/home/chroma/chroma_fresh_start/results/data/Sebastian_woteflon_05.12.2023/geometry_components __Sebastian_woteflon_0512.csv.csv'
# geom_file = '/home/chroma/chroma_fresh_start/results/data/Sebastian_teflon_05.12 .2023/geometry_components __Sebastian_teflon_0512.csv'
# geom_file ='/home/chroma/chroma_fresh_start/results/data/Sebastian_woteflon_05.23.2023/geometry_components __Sebastian_woteflon_0523.csv'
# geom_file ='/home/chroma/chroma_fresh_start/results/data/Sebastian_teflon_05.23.2023/geometry_components __Sebastian_teflon_0523.csv'
# geom_file = '/home/chroma/chroma_fresh_start/results/data/Sebastian_woteflon_upper_06.05.2023/geometry_components __Sebastian_woteflon_upper_0605.csv'
# geom_file = '/home/chroma/chroma_fresh_start/results/data/Sebastian_teflon_lowerlimit_06.05.2023/geometry_components __Sebastian_teflon__lower_0605.csv'
# geom_file = '/home/chroma/chroma_fresh_start/results/data/Sebastian_teflon_upperlimit_06.05.2023/geometry_components __Sebastian_teflon__upper_0605.csv'
geom_file = '/home/chroma/chroma_fresh_start/results/data/Sebastian_flippedsource_06.06.2023/geometry_components __Sebastian_teflon__FS_0606.csv'
geometry_df = pd.read_csv(geom_file)
stl_names = geometry_df['stl_filepath']
colors = geometry_df['color']
y_displacement = geometry_df['displacement y']
z_displacement = geometry_df['displacement z']

for curr_filename, curr_color, current_y_displacement, current_z_displacement in zip(stl_names, colors, y_displacement, z_displacement):
	your_mesh = mesh.Mesh.from_file(curr_filename)
	mesh_dimension = np.shape(your_mesh.vectors)
	for i in range(mesh_dimension[1]):
		your_mesh.vectors[:,i,1] += current_y_displacement
	for k in range(mesh_dimension[1]):
		your_mesh.vectors[:,i,2] += current_z_displacement
	poly3d = mplot3d.art3d.Poly3DCollection(your_mesh.vectors)
	poly3d.set_alpha(0.2)
	poly3d.set_edgecolor(None)
	poly3d.set_facecolor(curr_color)
	axes.add_collection3d(poly3d)
	# Auto scale to the mesh size
	scale = your_mesh.points.flatten()

	axes.auto_scale_xyz(scale, scale, scale)


# # plot specific geometry
# # find dimension of specific geometry in the simulation
# curr_filename = '/home/chroma/chroma_fresh_start/data_files/stl_files/Sebastian/2023_6_05_Assembly_N8_Teflon_FS/Updated measures Teflon FS - sourceflippedassem-1 sourcepart3-2.STL'
# your_mesh = mesh.Mesh.from_file(curr_filename)
# # print(current_y_displacement)
# mesh_dimension = np.shape(your_mesh.vectors)
# print(mesh_dimension)
# # print('the y component of mesh:',your_mesh.vectors[:,:,1])

# print('the minimum y is:',your_mesh.vectors[:,:,1].min())
# print('the maximum y is:',your_mesh.vectors[:,:,1].max())
# print('the minimum x is:',your_mesh.vectors[:,:,0].min())
# print('the maximum x is:',your_mesh.vectors[:,:,0].max())
# print('the minimum z is:',your_mesh.vectors[:,:,2].min())
# print('the maximum z is:',your_mesh.vectors[:,:,2].max())
                                                                                                                    
# poly3d = mplot3d.art3d.Poly3DCollection(your_mesh.vectors)
# poly3d.set_alpha(0.2)
# poly3d.set_edgecolor(None)
# poly3d.set_facecolor('grey')
# axes.add_collection3d(poly3d)



		# # # the below try to find the "hollow dimension" from a piece of gemetry
		# minx = your_mesh.vectors[:,:,0].min()
		# maxx = your_mesh.vectors[:,:,0].max()		
		# flatx = [item for sublist in your_mesh.vectors[:,:,0] for item in sublist]
		# # print('type flatx',type(flatx))
		# flatx_int = [int(i) for i in flatx]
		# # print('type flatx_int',type(flatx_int))

		# # for i in range(int(minx),int(maxx)):
		# # 	if i not in flatx_int:
		# # 		print(i)
		# # take a slice of mid-yz plane and ranging x value,(y = 48.412377,z = 91.27882)
		# miny = your_mesh.vectors[:,:,1].min()
		# maxy = your_mesh.vectors[:,:,1].max()
		# midy = str(round((miny + (maxy-miny)/2),2)) #need to turn the float into string for comparison
		# minz = your_mesh.vectors[:,:,2].min()
		# maxz = your_mesh.vectors[:,:,2].max()
		# midz = str(round((minz + (maxz-minz)/2),2))
		# print("middle y:",midy,"middle z:",midz)

		# flatz = [item for sublist in your_mesh.vectors[:,:,2] for item in sublist]
		# rounded_z = ['%.2f' %elem for elem in flatz]
		# # print('type of rounded_z',type(rounded_z[10]))


		# #find the value that is closet to the mid value
		# z_mid = float(midz)
		# for i in range(10):
		# 	z_mid_find = z_mid + 0.01*i
		# 	print(z_mid_find)
		# 	if str(z_mid_find) in rounded_z:
		# 		print('Cloest z_mid in the list',z_mid_find)
		# 		break

		# # print('the index of y in rounded flaty is',rounded_y.index(str(y_mid_find)) ,'which is 3 times the index of the original list')
		# # print(your_mesh.vectors[4331,2,2])
		# # print(type(z_mid_find))

		# # random_int = int(your_mesh.vectors[10,2,2])
		# # print(random_rounded)
		# # print(type(random_int))
		# # print(type(round(z_mid_find)))

		# index_listi = []
		# for i in range(len(your_mesh.vectors)):
		# 	for j in range(3):
		# 		# print(round(your_mesh.vectors[i,j,2],2))
		# 		# print(type(round(your_mesh.vectors[i,j,2],2)))
		# 		# print('type of z_mid_find',type(z_mid_find))
		# 		if int(your_mesh.vectors[i,j,2]) == int(z_mid_find):
		# 			index_listi.append(i)

		# index_listi = [*set(index_listi)]
		# print(len(index_listi))
		# wantedx_list = []
		# for k in range(len(index_listi)):
		# 	list_index = index_listi[k]
		# 	for j in range(3):
		# 		wantedx_list.append(your_mesh.vectors[list_index,j,0])

		# wantedx_list = [*set(wantedx_list)]
		# wantedx_list = sorted(wantedx_list,key = float)
		# # print(len(wantedx_list))
		# # print(wantedx_list[10])
		# xint_list =[]
		# # for w in range(len(wantedx_list)):
		# # 	if int(wantedx_list[w]) == 82:
		# # 		print('the index in list is',w)
		# # 		print(wantedx_list[w])
		# # 		break

		# # 	xint_list.append(x_int)

		# # xint_list = [*set(xint_list)]
		# # print(len(xint_list))
		# # print(xint_list)







axes.set_xlabel('x [mm]')
axes.set_ylabel('y [mm]')
axes.set_zlabel('z [mm]')
axes.set_xlim(0, 60)
axes.set_ylim(30, 75)
axes.set_zlim(0, 130)

# axes.set_xlim(50, 110)
# axes.set_ylim(20, 65)
# axes.set_zlim(30, 160)
# # Show the plot to the screen
plt.show()