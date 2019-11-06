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

parser=argparse.ArgumentParser(description='Histograms of the inversions', formatter_class=argparse.RawTextHelpFormatter)
#parser.add_argument("-op", "--opt-arg", type=str, dest='opcional', help="Algum argumento opcional no programa", default=False)
parser.add_argument("exp", type=str, help="Ano", default=0)
args=parser.parse_args()

exp = args.exp
exp = 'PanArctic_0.5d_CanHisto_NOCTEM_RUN'

def main(exp):    

    main_folder = "/home/cruman/projects/rrg-sushama-ab/teufel/{0}".format(exp)

    datai = 1976
    dataf = 2005
    
    deltaT_l = []

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

          deltaT[lats2d < 64] = np.nan
          aux = deltaT.flatten()
          deltaT_l.extent(aux[~np.isnan(aux)].tolist())
          print(deltaT_l)
          print(len(deltaT_l))
          
        
      print(deltaT_l)
      print(len(deltaT_l))
      sys.exit()
          

        #store the data to create the histogram at the end of the loop
    

if __name__ == "__main__":
    main(exp)
