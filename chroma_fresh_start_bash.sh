#!/bin/bash

count=1
max_count=20

# below run different run id
while [ $count -le $max_count ]
do
  singularity exec --nv ~/Downloads/Chroma.sif python ~/chroma_fresh_start/main.py -n 1000000 -s 18271 -r $count
  ((count++))
done


for ((i=count; i<=$max_count ; i++))
do
   # filename=/home/chroma/chroma_fresh_start/results/data/copperplates_06.23.2022/datapoints/hd3_data_test_$i.csv
   # filename=/home/chroma/chroma_fresh_start/results/data/beam_direction_06.30.2022/datapoints/hd3_data_test_$i.csv
   # filename=/home/chroma/chroma_fresh_start/results/data/source_copperholder_08.16.2022/datapoints/hd3_data_test_$i.csv
   # filename=/home/chroma/chroma_fresh_start/results/data/source_copperholder_08.16.2022/datapoints/hd3_data_test_$i.csv
   # filename=/home/chroma/chroma_fresh_start/results/data/copper_gasket_08.29.2022/datapoints/hd3_data_test_$i.csv
   # filename=/home/chroma/chroma_fresh_start/results/data/aluminum_disk_11.28.2022/datapoints/hd3_data_test_$i.csv
   filename=/home/chroma/chroma_fresh_start/results/data/Al_filler_02.07.2023/datapoints/hd3_data_test_$i.csv
   echo "Hi"
   OLDIFS=$IFS
   IFS=','
   # sed -n '3{p;q}' $filename >> /home/chroma/chroma_fresh_start/results/data/copperplates_06.23.2022/VariedLXe_1_64_0629.csv
   # sed -n '3{p;q}' $filename >> /home/chroma/chroma_fresh_start/results/data/beam_direction_06.30.2022/datapoints/beam_angle_data_0712.csv
   # sed -n '3{p;q}' $filename >> /home/chroma/chroma_fresh_start/results/data/source_copperholder_08.16.2022/datapoints/sourceSiPMholder_data_0824.csv
   # sed -n '2{p;q}' $filename >> /home/chroma/chroma_fresh_start/results/data/source_copperholder_08.16.2022/datapoints/sourceSiPMholder_data_0826.csv
   # sed -n '2{p;q}' $filename >> /home/chroma/chroma_fresh_start/results/data/copper_gasket_08.29.2022/datapoints/coppergasket_data_0831.csv
   # sed -n '2{p;q}' $filename >> /home/chroma/chroma_fresh_start/results/data/aluminum_disk_11.28.2022/datapoints/aluminumdisk_data_1201.csv
   sed -n '2{p;q}' $filename >> /home/chroma/chroma_fresh_start/results/data/Al_filler_02.07.2023/datapoints/aluminum_filler_0207.csv
   IFS=$OLDIFS

done
