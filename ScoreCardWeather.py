import os
import weatherbench2
import xarray as xr
import math
from weatherbench2.regions import SliceRegion, ExtraTropicalRegion
from weatherbench2.evaluation import evaluate_in_memory
from weatherbench2 import config
import numpy as np
import sigkernel
import torch
#from einops import rearrange
#from itertools import product
import cython
#import matplotlib.pyplot  as plt
#import tqdm
#import Functions as fu
#import line_profiler
from datetime import datetime, timedelta
#from multiprocessing import Pool, cpu_count
import time
from weatherbench2.metrics import MSE, ACC
from weatherbench2.regions import SliceRegion
#import seaborn as sns
from dateutil.relativedelta import relativedelta
import ScorecardFunctions2 as SCF

obs_path = 'gs://weatherbench2/datasets/era5/1959-2023_01_10-6h-64x32_equiangular_conservative.zarr'

pathsIFS = config.Paths(
    forecast='gs://weatherbench2/datasets/ifs_ens/2018-2022-64x32_equiangular_conservative.zarr',
    obs=obs_path,
    output_dir='results/',   # Directory to save evaluation results
)
pathsgcm = config.Paths(
    forecast='gs://weatherbench2/datasets/neuralgcm_ens/2020-64x32_equiangular_conservative.zarr',
    obs=obs_path,
    output_dir='results/',   # Directory to save evaluation results
)

startdate = {0:'2020-01-01',1:'2020-02-01',2:'2020-03-01',3:'2020-04-01',4:'2020-05-01',5:'2020-06-01',6:'2020-07-01',7:'2020-08-01',8:'2020-09-01',9:'2020-10-01',10:'2020-11-01',11:'2020-12-01'}
enddate = {0:'2020-01-03',1:'2020-02-03',2:'2020-03-03',3:'2020-04-03',4:'2020-05-03',5:'2020-06-03',6:'2020-07-03',7:'2020-08-03',8:'2020-09-03',9:'2020-10-03',10:'2020-11-03',11:'2020-12-03'}

from weatherbench2.metrics import CRPS, CRPSSpread, CRPSSkill, EnergyScore
from weatherbench2.regions import SliceRegion

regions = {
    'northernhemisphere': SliceRegion(lat_slice=slice(20, 90)),
    'tropics': SliceRegion(lat_slice=slice(-20, 20)),
    'southernhemisphere': SliceRegion(lat_slice=slice(-90, -20)),
}


for i in range(12):
    eval_configs = {
    'ENSERAmonths'+str(i): config.Eval(
        metrics={
            'CRPS': CRPS(), 
            'CRPSSpread': CRPSSpread(),
            'CRPSSkill': CRPSSkill(),
            'EnergyScore': EnergyScore()
        },
        regions=regions
    )
    }

    selection = config.Selection(
    variables=[
        'geopotential',
        'temperature',
        'u_component_of_wind',
        'v_component_of_wind',
    ],
    levels=[500, 850],
    time_slice=slice(startdate[i], enddate[i])
    )
    data_config = config.Data(selection=selection, paths=pathsIFS)
    
    evaluate_in_memory(data_config, eval_configs) 


    for i in range(12):
        eval_configs = {
        'ENSERAmonthsgcm'+str(i): config.Eval(
            metrics={
                'CRPS': CRPS(), 
                'CRPSSpread': CRPSSpread(),
                'CRPSSkill': CRPSSkill(),
                'EnergyScore': EnergyScore()
            },
            regions=regions
        )
        }

        selection = config.Selection(
        variables=[
            'geopotential',
            'temperature',
            'u_component_of_wind',
            'v_component_of_wind',
        ],
        levels=[500, 850],
        time_slice=slice(startdate[i], enddate[i])
        )
        data_config = config.Data(selection=selection, paths=pathsgcm)

        evaluate_in_memory(data_config, eval_configs) 
