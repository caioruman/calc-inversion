import numpy as np
import pandas as pd
import sys

from datetime import date, datetime, timedelta

from glob import glob
from rpn.rpn import RPN
from rpn.domains.rotated_lat_lon import RotatedLatLon
from rpn import level_kinds

from netCDF4 import Dataset
import time
import argparse

'''
    Using the
'''

#parser=argparse.ArgumentParser(description='Histograms of the inversions', formatter_class=argparse.RawTextHelpFormatter)
#parser.add_argument("-op", "--opt-arg", type=str, dest='opcional', help="Algum argumento opcional no programa", default=False)
#parser.add_argument("exp", type=str, help="Ano", default=0)
#args=parser.parse_args()

#exp = args.exp

'''
  to do: Get the land/ocean mask and do a histrogram for each
'''

def main():    

    
    exp = ['PanArctic_0.5d_CanHisto_NOCTEM_RUN', 'PanArctic_0.5d_CanHisto_NOCTEM_R2', 'PanArctic_0.5d_CanHisto_NOCTEM_R3',
       'PanArctic_0.5d_CanHisto_NOCTEM_R5', 'PanArctic_0.5d_CanHisto_NOCTEM_R4']

    datai = 1976
    dataf = 2005    

    arq_sea_mask = '/home/cruman/projects/rrg-sushama-ab/teufel/PanArctic_0.5d_ERAINT_NOCTEM_RUN/Analysis/anal_PanArctic_0.5d_ERAINT_NOCTEM_RUN_1980010100'

    with RPN(arq_sea_mask) as r:
      sea_mask = np.squeeze(r.variables["I6"][:])[13:-13, 13:-13] # values == 0 equals the sea
    
    sea_mask[sea_mask > 0] = 1
    

    main_folder = "/home/cruman/projects/rrg-sushama-ab/teufel/{0}".format(exp[0])
    deltaT_R1_l, deltaT_R1_s = calcInversions(exp[0], datai, dataf, main_folder, sea_mask)
    #deltaT_R2 = calcInversions(exp[1], datai, dataf, main_folder)
    #deltaT_R3 = calcInversions(exp[2], datai, dataf, main_folder)
    #deltaT_R4 = calcInversions(exp[3], datai, dataf, main_folder)
    #deltaT_R5 = calcInversions(exp[4], datai, dataf, main_folder)    

    fname = 'histogram_R1.png'

    bins = np.arange(-20,21,1)

    calc_histogram(deltaT_R1_l, bins)
    calc_histogram(deltaT_R1_s, bins)

    sys.exit()


def calc_histogram(data, bins):

  hist, bin_edges = np.histogram(data, bins)
  print(bin_edges)
  print(hist)

  # plot the histrogram
  

def calcInversions(exp, datai, dataf, main_folder, sea_mask):

  deltaT_l = []
  deltaT_s = []
  for year in range(datai, dataf+1):

      for month in range(1,13):

        # open dp file
        arq_dp = "{0}/Diagnostics/{1}_{2}{3:02d}/dp{1}_{2}{3:02d}_moyenne".format(main_folder, exp, year, month)

        print(arq_dp)

        #read the file, extract temperature from 2 levels and calculate the difference for the points where lat > 64
        with RPN(arq_dp) as r:

          t2m = np.squeeze(r.variables["TT"][:])
          t2 = r.variables["TT"]

          deltaT = t2m[-4,:,:] - t2m[-1,:,:]

          lons2d, lats2d = r.get_longitudes_and_latitudes_for_the_last_read_rec() 

          deltaT[lats2d < 64.] = np.nan
          deltaT_land = deltaT.copy()
          deltaT_sea = deltaT.copy()
          deltaT_land[sea_mask == 0] = np.nan
          deltaT_sea[sea_mask == 1] = np.nan

          aux = deltaT_land.flatten()
          deltaT_l.extend(aux[~np.isnan(aux)].tolist())

          aux = deltaT_sea.flatten()
          deltaT_s.extend(aux[~np.isnan(aux)].tolist())
          #print(deltaT_l)
          #print(len(deltaT_l))
                  
      #print(deltaT_l)
      #print(len(deltaT_l))

  return deltaT_l, deltaT_s
if __name__ == "__main__":
    main()
