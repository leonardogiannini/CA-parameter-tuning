from optimizer.mopso import MOPSO
import subprocess
from utils import get_metrics, write_csv
import numpy as np
import uproot
import argparse
import os

# parsing argument
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--continuing', type=int, action='store')
parser.add_argument('-d', '--default', action='store_true')
parser.add_argument('-p', '--num_particles', default=100, type=int, action='store')
parser.add_argument('-i', '--num_iterations', default=20, type=int, action='store')
parser.add_argument('-e', '--num_events', default=100, type=int, action='store')
args = parser.parse_args()

#process.initialStepTrackCandidatesMkFitConfig.validHitBonus = 4
#process.initialStepTrackCandidatesMkFitConfig.validHitSlope = 0.2
#process.initialStepTrackCandidatesMkFitConfig.overlapHitBonus = 0
#process.initialStepTrackCandidatesMkFitConfig.missingHitPenalty = 8
#process.initialStepTrackCandidatesMkFitConfig.tailMissingHitPenalty = 3

# define the lower and upper bounds
lb = [0.0, 0.0, 0.0, 0.0, 0.0]
ub = [10.0, 1.0, 1.0, 20.0, 10.0]

config = 'step3_RAW2DIGI_RECO_VALIDATION_forOpt.py'
input_file = '/ceph/cms/store/user/legianni/validate_1250_pre5_RelVal/ca71da18-4022-4ff7-b219-f346ff033299.root'

# run pixel reconstruction and simple validation
def reco_and_validate(params):
    if not os.path.exists('temp'):
        os.mkdir('temp')
    write_csv('temp/parameters.csv', params)
    validation_result = 'temp/simple_validation.root'
    subprocess.run(['cmsRun', config, 'inputFiles=file:' + input_file, 'nEvents=' + str(args.num_events),
                     'parametersFile=temp/parameters.csv', 'outputFile=' + validation_result])
    num_particles = len(params)
    with uproot.open(validation_result) as uproot_file:
        population_fitness = [get_metrics(uproot_file, i) for i in range(num_particles)]
    return population_fitness


# get default metrics
if args.default:
    default_params = [[4,0.2,0,8,3]]
    default_metrics = reco_and_validate(default_params)
    write_csv('checkpoint/default.csv', [np.concatenate([default_params[0], default_metrics[0]])])

        
# create the PSO object
if not args.continuing:
    os.system('rm history/*')
    pso = MOPSO(objective_functions=[reco_and_validate],lower_bounds=lb, upper_bounds=ub, 
                num_objectives=2, num_particles=args.num_particles, num_iterations=args.num_iterations, 
                inertia_weight=0.5, cognitive_coefficient=1, social_coefficient=1, 
                max_iter_no_improv=None, optimization_mode='global')
else:
    pso = MOPSO(objective_functions=[reco_and_validate],lower_bounds=lb, upper_bounds=ub, 
                num_iterations=args.continuing, checkpoint_dir='checkpoint')

# run the optimization algorithm
pso.optimize(history_dir='history', checkpoint_dir='checkpoint')

