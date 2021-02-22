import sys
import os
import subprocess
import readline
import string

data2018_samples = {}
mc2018_samples = {}
#data2017_samples ['DYM10to50'] = ['address', 'data/mc','dataset','year', 'run', 'cross section','lumi','Neventsraw']
mc2018_samples['2018_DYM10to50'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-10to50_v15_v2/191201_145133/0000/'], 'mc','','2018', '','18610','59.97','39360792']
mc2018_samples['2018_DYM50'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_amcatnlo_v15_v1/200311_151257/0000/','/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_amcatnlo_v15_ext2_v1/200311_150842/0000/','/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_amcatnlo_v15_ext2_v1/200311_150842/0001/','/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_amcatnlo_v15_ext2_v1/200311_150842/0002/'], 'mc','','2018', '','5765.4','59.97','131615987']
mc2018_samples['2018_TTTo2L2Nu'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_TTTo2L2Nu_3/191215_182557/0000/'], 'mc','','2018', '','87.31','59.97','63791484']
mc2018_samples['2018_ST_tW'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/crab_ST_tW_top_v15_ext1-v2/191201_151723/0000/'], 'mc','','2018', '','19.47','59.97','1080939']
mc2018_samples['2018_ST_atW'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/crab_ST_tW_antitop_v15_ext1-v2/191201_152039/0000/'], 'mc','','2018', '','19.47','59.97','1081535']
mc2018_samples['2018_WWTo2L2Nu'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/crab_WWTo2L2Nu/191201_145426/0000/'], 'mc','','2018', '','12.178','59.97','7729266']
mc2018_samples['2018_ZZTo2L2Nu'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/crab_ZZTo2L2Nu_v15_ext2-v2/191201_151518/0000/'], 'mc','','2018', '','0.564','59.97','47984296']
mc2018_samples['2018_ZZTo4L'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_ZZTo4L_v15_ext1-v2/191201_151326/0000/'], 'mc','','2018', '','1.212','59.97','6622242']
mc2018_samples['2018_WZTo2L2Q'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/crab_WZTo2L2Q_v15_v1/191201_150857/0000/'], 'mc','','2018', '','5.595','59.97','17048434']
mc2018_samples['2018_WZTo3LNu'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_WZTo3LNu_v15-v1/191201_145614/0000/'], 'mc','','2018', '','4.43','59.97','6739437']
mc2018_samples['2018_WJetsToLNu'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/crab_WJetsToLNu/191201_153344/0000/'], 'mc','','2018', '','61526.7','59.97','70966439']
mc2018_samples['2018_TTWJetsToQQ'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_TTWJetsToQQ_v15_v1/191201_152701/0000/'], 'mc','','2018', '','0.4062','59.97','458226']
mc2018_samples['2018_TTWJetsToLNu'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_TTWJetsToLNu_v15_ext1-v2/191201_152347/0000/'], 'mc','','2018', '','0.2043','59.97','2686095']
mc2018_samples['2018_TTZToLLNuNu'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_TTZToLLNuNu_v15_ext1-v2/191201_152847/0000/'], 'mc','','2018', '','0.2529','59.97','6274046']
mc2018_samples['2018_TTZToQQ'] = [['/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/crab_TTZToQQ_v15_ext1-v1/191201_153157/0000/'], 'mc','','2018', '','0.5297','59.97','4221534']

mc2018_samples['2018_LFVStVecC'] = [['/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2018/IIHE_Ntuple/ntuple_SMEFTfr_ST_vector_emutc/'], 'mc','','2018', '','0.0512' ,'59.97','500000']
mc2018_samples['2018_LFVStVecU'] = [['/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2018/IIHE_Ntuple/ntuple_SMEFTfr_ST_vector_emutu/'], 'mc','','2018', '','0.515' ,'59.97','500000']
mc2018_samples['2018_LFVTtVecC'] = [['/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2018/IIHE_Ntuple/ntuple_SMEFTfr_TT_vector_emutc/'], 'mc','','2018', '','0.032'  ,'59.97','500000']
mc2018_samples['2018_LFVTtVecU'] = [['/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2018/IIHE_Ntuple/ntuple_SMEFTfr_TT_vector_emutu/'], 'mc','','2018', '','0.032','59.97','500000']

mc2018_samples['2018_LFVStScalarC'] = [['/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2018/IIHE_Ntuple/ntuple_SMEFTfr_ST_clequ1_emutc/'], 'mc','','2018', '','0.008' ,'59.97','500000']
mc2018_samples['2018_LFVStScalarU'] = [['/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2018/IIHE_Ntuple/ntuple_SMEFTfr_ST_clequ1_emutu/'], 'mc','','2018', '','0.102' ,'59.97','500000']
mc2018_samples['2018_LFVTtScalarC'] = [['/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2018/IIHE_Ntuple/ntuple_SMEFTfr_TT_clequ1_emutc/'], 'mc','','2018', '','0.004' ,'59.97','500000']
mc2018_samples['2018_LFVTtScalarU'] = [['/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2018/IIHE_Ntuple/ntuple_SMEFTfr_TT_clequ1_emutu/'], 'mc','','2018', '','0.004' ,'59.97','500000']

mc2018_samples['2018_LFVStTensorC'] = [['/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2018/IIHE_Ntuple/ntuple_SMEFTfr_ST_clequ3_emutc/'], 'mc','','2018', '','0.187' ,'59.97','500000']
mc2018_samples['2018_LFVStTensorU'] = [['/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2018/IIHE_Ntuple/ntuple_SMEFTfr_ST_clequ3_emutu/'], 'mc','','2018', '','1.900' ,'59.97','500000']
mc2018_samples['2018_LFVTtTensorC'] = [['/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2018/IIHE_Ntuple/ntuple_SMEFTfr_TT_clequ3_emutc/'], 'mc','','2018', '','0.1876','59.97','500000']
mc2018_samples['2018_LFVTtTensorU'] = [['/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2018/IIHE_Ntuple/ntuple_SMEFTfr_TT_clequ3_emutu/'], 'mc','','2018', '','0.1876','59.97','500000']
###############################################

data2018_samples['2018_A_MuonEG'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/MuonEG/crab_MuonEG_RunA/191204_073252/0000/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/MuonEG/crab_MuonEG_RunA/191204_073252/0001/'], 'data','MuonEG','2018', 'A','1','1','1']
data2018_samples['2018_B_MuonEG'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/MuonEG/crab_MuonEG_RunB/191204_073311/0000/'], 'data','MuonEG','2018', 'B','1','1','1']
data2018_samples['2018_C_MuonEG'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/MuonEG/crab_MuonEG_RunC/191204_073329/0000/'], 'data','MuonEG','2018', 'C','1','1','1']
data2018_samples['2018_D_MuonEG'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/MuonEG/crab_MuonEG_RunD/191206_094619/0000/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/MuonEG/crab_MuonEG_RunD/191206_094619/0001/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/MuonEG/crab_MuonEG_RunD/191206_094619/0002/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/MuonEG/crab_MuonEG_RunD/191206_094619/0003/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/MuonEG/crab_MuonEG_RunD/191206_094619/0004/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/MuonEG/crab_MuonEG_RunD/191206_094619/0005/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/MuonEG/crab_MuonEG_RunD/191206_094619/0006/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/MuonEG/crab_MuonEG_RunD/191206_094619/0007/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/MuonEG/crab_MuonEG_RunD/191206_094619/0008/'], 'data','MuonEG','2018', 'D','1','1','1']

data2018_samples['2018_A_SingleMuon'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/SingleMuon/crab_SingleMuon_RunA/191204_073350/0000/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/SingleMuon/crab_SingleMuon_RunA/191204_073350/0001/'], 'data','SingleMuon','2018', 'A','1','1','1']
data2018_samples['2018_B_SingleMuon'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/SingleMuon/crab_SingleMuon_RunB/191204_073409/0000/'], 'data','SingleMuon','2018', 'B','1','1','1']
data2018_samples['2018_C_SingleMuon'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/SingleMuon/crab_SingleMuon_RunC/191204_073428/0000/'], 'data','SingleMuon','2018', 'C','1','1','1']
data2018_samples['2018_D_SingleMuon'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/SingleMuon/crab_SingleMuon_RunD/191206_094638/0000/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/SingleMuon/crab_SingleMuon_RunD/191206_094638/0001/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/SingleMuon/crab_SingleMuon_RunD/191206_094638/0002/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/SingleMuon/crab_SingleMuon_RunD/191206_094638/0003/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/SingleMuon/crab_SingleMuon_RunD/191206_094638/0004/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/SingleMuon/crab_SingleMuon_RunD/191206_094638/0005/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/SingleMuon/crab_SingleMuon_RunD/191206_094638/0006/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/SingleMuon/crab_SingleMuon_RunD/191206_094638/0007/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/SingleMuon/crab_SingleMuon_RunD/191206_094638/0008/'], 'data','SingleMuon','2018', 'D','1','1','1']


data2018_samples['2018_A_EGamma'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/EGamma/crab_EGamma_RunA/191204_073447/0000/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/EGamma/crab_EGamma_RunA/191204_073447/0001/'], 'data','EGamma','2018', 'A','1','1','1']
data2018_samples['2018_B_EGamma'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/EGamma/crab_EGamma_RunB/191204_073507/0000/'], 'data','EGamma','2018', 'B','1','1','1']
data2018_samples['2018_C_EGamma'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/EGamma/crab_EGamma_RunC/191204_073525/0000/'], 'data','EGamma','2018', 'C','1','1','1']
data2018_samples['2018_D_EGamma'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/EGamma/crab_EGamma_RunD/191206_094657/0000/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/EGamma/crab_EGamma_RunD/191206_094657/0001/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/EGamma/crab_EGamma_RunD/191206_094657/0002/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/EGamma/crab_EGamma_RunD/191206_094657/0003/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/EGamma/crab_EGamma_RunD/191206_094657/0004/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/EGamma/crab_EGamma_RunD/191206_094657/0005/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/EGamma/crab_EGamma_RunD/191206_094657/0006/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/EGamma/crab_EGamma_RunD/191206_094657/0007/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/EGamma/crab_EGamma_RunD/191206_094657/0008/'], 'data','EGamma','2018', 'D','1','1','1']

data2018_samples['2018_A_DoubleMu'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/DoubleMuon/crab_DoubleMuon_RunA-v3/200306_135843/0000/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/DoubleMuon/crab_DoubleMuon_RunA-v3/200306_135843/0001/'], 'data','DoubleMu','2018', 'A','1','1','1']
data2018_samples['2018_B_DoubleMu'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/DoubleMuon/crab_DoubleMuon_RunB-v3/200306_135859/0000/'], 'data','DoubleMu','2018', 'B','1','1','1']
data2018_samples['2018_C_DoubleMu'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/DoubleMuon/crab_DoubleMuon_RunC-v3/200306_135916/0000/'], 'data','DoubleMu','2018', 'C','1','1','1']
data2018_samples['2018_D_DoubleMu'] = [['/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/DoubleMuon/crab_DoubleMuon_RunD-v4/200306_135947/0000/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/DoubleMuon/crab_DoubleMuon_RunD-v4/200306_135947/0001/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/DoubleMuon/crab_DoubleMuon_RunD-v4/200306_135947/0002/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/DoubleMuon/crab_DoubleMuon_RunD-v4/200306_135947/0003/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/DoubleMuon/crab_DoubleMuon_RunD-v4/200306_135947/0004/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/DoubleMuon/crab_DoubleMuon_RunD-v4/200306_135947/0005/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/DoubleMuon/crab_DoubleMuon_RunD-v4/200306_135947/0006/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/DoubleMuon/crab_DoubleMuon_RunD-v4/200306_135947/0007/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2018/DoubleMuon/crab_DoubleMuon_RunD-v4/200306_135947/0008/'], 'data','DoubleMu','2018', 'D','1','1','1']


