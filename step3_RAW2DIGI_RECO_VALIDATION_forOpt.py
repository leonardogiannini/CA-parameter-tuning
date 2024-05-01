# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 --conditions auto:phase1_2022_realistic -s RAW2DIGI,RECO:reconstruction_trackingOnly,VALIDATION:@trackingOnlyValidation --datatier DQMIO -n 1000 --geometry DB:Extended --era Run3 --eventcontent DQM --no_exec --filein file:/ceph/cms/store/user/legianni/validate_1250_pre5_RelVal/ca71da18-4022-4ff7-b219-f346ff033299.root --fileout step3_mkFit_TTbarPU.root

# with command line options: step3 -s RAW2DIGI:RawToDigi_pixelOnly,RECO:reconstruction_pixelTrackingOnly,VALIDATION:@pixelTrackingOnlyValidation,DQM:@pixelTrackingOnlyDQM --conditions auto:phase1_2022_realistic --datatier GEN-SIM-RECO,DQMIO -n 100 --eventcontent RECOSIM,DQM --geometry DB:Extended --era Run3 --procModifiers pixelNtupletFit,gpu --filein file:step2.root --fileout file:step3.root --nThreads 8

import FWCore.ParameterSet.Config as cms
from utils import read_csv

from Configuration.Eras.Era_Run3_cff import Run3

# import VarParsing
from FWCore.ParameterSet.VarParsing import VarParsing

## VarParsing instance
options = VarParsing('analysis')

# Custom options
options.register('parametersFile',
              'default/default_params.csv',
              VarParsing.multiplicity.singleton,
              VarParsing.varType.string,
              'Name of parameters file')

options.register('nEvents',
              100,
              VarParsing.multiplicity.singleton,
              VarParsing.varType.int,
              'Number of events')

options.parseArguments()

process = cms.Process('RECO',Run3)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.Validation_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load( 'HLTrigger.Timer.FastTimerService_cfi' )

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.nEvents),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step3 nevts:1000'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# Additional output definition

# Other statements
process.mix.playback = True
process.mix.digitizers = cms.PSet()
for a in process.aliases: delattr(process, a)
process.RandomNumberGeneratorService.restoreStateLabel=cms.untracked.string("randomEngineStateProducer")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2022_realistic', '')
process.FastTimerService.writeJSONSummary = cms.untracked.bool(True)
process.FastTimerService.jsonFileName = cms.untracked.string('temp/times.json')
process.TFileService = cms.Service('TFileService', fileName=cms.string(options.outputFile)
                                   if cms.string(options.outputFile) else 'default.root')

params = read_csv(options.parametersFile)
totalTasks = len(params)
for i, row in enumerate(params):
    setattr(process, 'initialStepTrackCandidatesMkFitSeeds' + str(i), cms.EDProducer("MkFitSeedConverter",
        maxNSeeds = cms.uint32(500000),
        mightGet = cms.optional.untracked.vstring,
        seeds = cms.InputTag("initialStepSeeds"),
        ttrhBuilder = cms.ESInputTag("","WithTrackAngle")
        )
    )
    setattr(process, 'initialStepTrackCandidatesMkFitConfig' + str(i), cms.ESProducer("MkFitIterationConfigESProducer",
        ComponentName = cms.string('initialStepTrackCandidatesMkFitConfig'+ str(i)),
        appendToDataLabel = cms.string(''),
        config = cms.FileInPath('RecoTracker/MkFit/data/mkfit-phase1-initialStep.json'),
        maxClusterSize = cms.uint32(8),
        minPt = cms.double(0),
        missingHitPenalty = cms.double(row[0]),
        overlapHitBonus = cms.double(row[1]),
        tailMissingHitPenalty = cms.double(row[2]),
        validHitBonus = cms.double(row[3]),
        validHitSlope = cms.double(row[4])
        )
    )
    setattr(process, 'initialStepTrackCandidatesMkFit' + str(i), cms.EDProducer("MkFitProducer",
        backwardFitInCMSSW = cms.bool(False),
        buildingRoutine = cms.string('cloneEngine'),
        clustersToSkip = cms.InputTag(""),
        config = cms.ESInputTag("","initialStepTrackCandidatesMkFitConfig" + str(i)),
        eventOfHits = cms.InputTag("mkFitEventOfHits"),
        limitConcurrency = cms.untracked.bool(False),
        mightGet = cms.optional.untracked.vstring,
        minGoodStripCharge = cms.PSet(
            refToPSet_ = cms.string('SiStripClusterChargeCutLoose')
        ),
        mkFitSilent = cms.untracked.bool(True),
        pixelHits = cms.InputTag("mkFitSiPixelHits"),
        removeDuplicates = cms.bool(True),
        seedCleaning = cms.bool(True),
        seeds = cms.InputTag("initialStepTrackCandidatesMkFitSeeds" + str(i)),
        stripHits = cms.InputTag("mkFitSiStripHits")
        )
    )
    setattr(process, 'initialStepTrackCandidates' + str(i), cms.EDProducer("MkFitOutputConverter",
        batchSize = cms.int32(16),
        candMVASel = cms.bool(False),
        candWP = cms.double(0),
        doErrorRescale = cms.bool(True),
        mightGet = cms.optional.untracked.vstring,
        mkFitEventOfHits = cms.InputTag("mkFitEventOfHits"),
        mkFitPixelHits = cms.InputTag("mkFitSiPixelHits"),
        mkFitSeeds = cms.InputTag("initialStepTrackCandidatesMkFitSeeds" + str(i)),
        mkFitStripHits = cms.InputTag("mkFitSiStripHits"),
        propagatorAlong = cms.ESInputTag("","PropagatorWithMaterial"),
        propagatorOpposite = cms.ESInputTag("","PropagatorWithMaterialOpposite"),
        qualityMaxInvPt = cms.double(100),
        qualityMaxPosErr = cms.double(100),
        qualityMaxR = cms.double(120),
        qualityMaxZ = cms.double(280),
        qualityMinTheta = cms.double(0.01),
        qualitySignPt = cms.bool(True),
        seeds = cms.InputTag("initialStepSeeds"),
        tfDnnLabel = cms.string('trackSelectionTf'),
        tracks = cms.InputTag("initialStepTrackCandidatesMkFit" + str(i)),
        ttrhBuilder = cms.ESInputTag("","WithTrackAngle")
        )
    )
    setattr(process, 'initialStepTracks' + str(i), cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('initialStep' + str(i)),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        GeometricInnerState = cms.bool(False),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        Propagator = cms.string('PropagatorWithMaterialParabolicMf'),
        SimpleMagneticField = cms.string('ParabolicMf'),
        TTRHBuilder = cms.string('WithAngleAndTemplateWithoutProbQ'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("initialStepTrackCandidates" + str(i)),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(True)
        )
    )
    setattr(process, 'simpleValidation' + str(i), cms.EDAnalyzer('SimpleValidation',
            chargedOnlyTP = cms.bool(True),
            intimeOnlyTP = cms.bool(False),
            invertRapidityCutTP = cms.bool(False),
            lipTP = cms.double(30.0),
            maxPhi = cms.double(3.2),
            maxRapidityTP = cms.double(2.5),
            minHitTP = cms.int32(0),
            minPhi = cms.double(-3.2),
            minRapidityTP = cms.double(-2.5),
            pdgIdTP = cms.vint32(),
            ptMaxTP = cms.double(1e+100),
            ptMinTP = cms.double(0.9),
            signalOnlyTP = cms.bool(True),
            stableOnlyTP = cms.bool(False),
            tipTP = cms.double(3.5),
            trackLabels = cms.VInputTag('initialStepTracks' + str(i)),
            trackAssociator = cms.untracked.InputTag('quickTrackAssociatorByHits'),
            trackingParticles = cms.InputTag('mix', 'MergedTrackTruth')
        )
    )

##process.simpleValidation1=cms.EDAnalyzer('SimpleValidation',
    ##chargedOnlyTP = cms.bool(True),
    ##intimeOnlyTP = cms.bool(False),
    ##invertRapidityCutTP = cms.bool(False),
    ##lipTP = cms.double(30.0),
    ##maxPhi = cms.double(3.2),
    ##maxRapidityTP = cms.double(2.5),
    ##minHitTP = cms.int32(0),
    ##minPhi = cms.double(-3.2),
    ##minRapidityTP = cms.double(-2.5),
    ##pdgIdTP = cms.vint32(),
    ##ptMaxTP = cms.double(1e+100),
    ##ptMinTP = cms.double(0.9),
    ##signalOnlyTP = cms.bool(True),
    ##stableOnlyTP = cms.bool(False),
    ##tipTP = cms.double(3.5),
    ##trackLabels = cms.VInputTag('highPtTripletStepTracks'),
    ##trackAssociator = cms.untracked.InputTag('quickTrackAssociatorByHits'),
    ##trackingParticles = cms.InputTag('mix', 'MergedTrackTruth')
##)
##process.simpleValidation2=cms.EDAnalyzer('SimpleValidation',
    ##chargedOnlyTP = cms.bool(True),
    ##intimeOnlyTP = cms.bool(False),
    ##invertRapidityCutTP = cms.bool(False),
    ##lipTP = cms.double(30.0),
    ##maxPhi = cms.double(3.2),
    ##maxRapidityTP = cms.double(2.5),
    ##minHitTP = cms.int32(0),
    ##minPhi = cms.double(-3.2),
    ##minRapidityTP = cms.double(-2.5),
    ##pdgIdTP = cms.vint32(),
    ##ptMaxTP = cms.double(1e+100),
    ##ptMinTP = cms.double(0.9),
    ##signalOnlyTP = cms.bool(True),
    ##stableOnlyTP = cms.bool(False),
    ##tipTP = cms.double(3.5),
    ##trackLabels = cms.VInputTag('detachedQuadStepTracks'),
    ##trackAssociator = cms.untracked.InputTag('quickTrackAssociatorByHits'),
    ##trackingParticles = cms.InputTag('mix', 'MergedTrackTruth')
##)
##process.simpleValidation3=cms.EDAnalyzer('SimpleValidation',
    ##chargedOnlyTP = cms.bool(True),
    ##intimeOnlyTP = cms.bool(False),
    ##invertRapidityCutTP = cms.bool(False),
    ##lipTP = cms.double(30.0),
    ##maxPhi = cms.double(3.2),
    ##maxRapidityTP = cms.double(2.5),
    ##minHitTP = cms.int32(0),
    ##minPhi = cms.double(-3.2),
    ##minRapidityTP = cms.double(-2.5),
    ##pdgIdTP = cms.vint32(),
    ##ptMaxTP = cms.double(1e+100),
    ##ptMinTP = cms.double(0.9),
    ##signalOnlyTP = cms.bool(True),
    ##stableOnlyTP = cms.bool(False),
    ##tipTP = cms.double(3.5),
    ##trackLabels = cms.VInputTag('detachedTripletStepTracks'),
    ##trackAssociator = cms.untracked.InputTag('quickTrackAssociatorByHits'),
    ##trackingParticles = cms.InputTag('mix', 'MergedTrackTruth')
##)
##process.simpleValidation4=cms.EDAnalyzer('SimpleValidation',
    ##chargedOnlyTP = cms.bool(True),
    ##intimeOnlyTP = cms.bool(False),
    ##invertRapidityCutTP = cms.bool(False),
    ##lipTP = cms.double(30.0),
    ##maxPhi = cms.double(3.2),
    ##maxRapidityTP = cms.double(2.5),
    ##minHitTP = cms.int32(0),
    ##minPhi = cms.double(-3.2),
    ##minRapidityTP = cms.double(-2.5),
    ##pdgIdTP = cms.vint32(),
    ##ptMaxTP = cms.double(1e+100),
    ##ptMinTP = cms.double(0.9),
    ##signalOnlyTP = cms.bool(True),
    ##stableOnlyTP = cms.bool(False),
    ##tipTP = cms.double(3.5),
    ##trackLabels = cms.VInputTag('pixelLessStepTracks'),
    ##trackAssociator = cms.untracked.InputTag('quickTrackAssociatorByHits'),
    ##trackingParticles = cms.InputTag('mix', 'MergedTrackTruth')
##)


# Prevalidation
process.tpClusterProducer = cms.EDProducer('ClusterTPAssociationProducer',
    mightGet = cms.optional.untracked.vstring,
    phase2OTClusterSrc = cms.InputTag('siPhase2Clusters'),
    phase2OTSimLinkSrc = cms.InputTag('simSiPixelDigis','Tracker'),
    pixelClusterSrc = cms.InputTag('siPixelClusters'),
    pixelSimLinkSrc = cms.InputTag('simSiPixelDigis'),
    simTrackSrc = cms.InputTag('g4SimHits'),
    stripClusterSrc = cms.InputTag('siStripClusters'),
    stripSimLinkSrc = cms.InputTag('simSiStripDigis'),
    throwOnMissingCollections = cms.bool(True),
    trackingParticleSrc = cms.InputTag('mix','MergedTrackTruth')
)

process.quickTrackAssociatorByHits = cms.EDProducer('QuickTrackAssociatorByHitsProducer',
    AbsoluteNumberOfHits = cms.bool(False),
    Cut_RecoToSim = cms.double(0.75),
    PixelHitWeight = cms.double(1.0),
    Purity_SimToReco = cms.double(0.75),
    Quality_SimToReco = cms.double(0.5),
    SimToRecoDenominator = cms.string('reco'),
    ThreeHitTracksAreSpecial = cms.bool(True),
    cluster2TPSrc = cms.InputTag('tpClusterProducer'),
    useClusterTPAssociation = cms.bool(True)
)


# Lists of tasks
taskListSeed = [getattr(process, 'initialStepTrackCandidatesMkFitSeeds'+str(i)) for i in range(totalTasks)]
taskListCfg = [getattr(process, 'initialStepTrackCandidatesMkFitConfig'+str(i)) for i in range(totalTasks)]
taskListMkCand = [getattr(process, 'initialStepTrackCandidatesMkFit'+str(i)) for i in range(totalTasks)]
taskListCand = [getattr(process, 'initialStepTrackCandidates'+str(i)) for i in range(totalTasks)]
taskList = [getattr(process, 'initialStepTracks'+str(i)) for i in range(totalTasks)]
taskListVal = [getattr(process, 'simpleValidation'+str(i)) for i in range(totalTasks)]

# Tasks and sequences
process.initTracksTask = cms.Task(*taskListSeed, *taskListCfg, *taskListMkCand, *taskListCand, *taskList)
#process.initTracksSeq = cms.Sequence(process.initTracksTask)
process.preValidation = cms.Sequence(process.tpClusterProducer + process.quickTrackAssociatorByHits)
process.simpleValSeq = cms.Sequence(sum(taskListVal[1:],taskListVal[0]))



process.preValidation = cms.Sequence(process.tpClusterProducer + process.quickTrackAssociatorByHits)
#process.simpleValSeq = cms.Sequence(process.simpleValidation0 + process.simpleValidation1 + process.simpleValidation2 + process.simpleValidation3 + process.simpleValidation4)
process.simpleValSeq = cms.Sequence(sum(taskListVal[1:],taskListVal[0]))
process.consumer = cms.EDAnalyzer('GenericConsumer', eventProducts = cms.untracked.vstring('tracksValidation'))

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.reconstruction_trackingOnly)
#process.prevalidation_step = cms.Path(process.globalPrevalidationTrackingOnly)
process.inittracks_step = cms.Path(process.initTracksTask)
process.prevalidation_step = cms.Path(process.preValidation)
#process.validation_step = cms.EndPath(process.globalValidationTrackingOnly)
process.validation_step = cms.Path(process.simpleValSeq)
process.consume_step = cms.EndPath(process.consumer)


# Schedule definition
process.schedule = cms.Schedule(
    process.raw2digi_step,
    process.reconstruction_step,
    process.inittracks_step,
    process.prevalidation_step,
    process.validation_step,
    process.consume_step
    )


# customisation of the process.

# Automatic addition of the customisation function from SimGeneral.MixingModule.fullMixCustomize_cff
from SimGeneral.MixingModule.fullMixCustomize_cff import setCrossingFrameOn 

#Setup FWK for multithreaded
process.options.numberOfThreads = 8
process.options.numberOfStreams = 0

#call to customisation function setCrossingFrameOn imported from SimGeneral.MixingModule.fullMixCustomize_cff
process = setCrossingFrameOn(process)

# End of customisation functions


# Customisation from command line

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
