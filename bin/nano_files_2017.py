import sys
import os
import subprocess
import readline
import string

data2017_samples = {}
mc2017_samples = {}
#data2017_samples ['DYM10to50'] = ['address', 'data/mc','dataset','year', 'run', 'cross section','lumi','Neventsraw']                        

mc2017_samples['2017_DYM10to50'] = [['/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv6-1-1_2017/200613_065556/0000/'], 'mc','','2017', '','18610','41.53','39521230'] ## '78,994,955' ## <-  is event number from miniaod, we must be missing an extension

mc2017_samples['2017_DYM50'] = [['/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/TopNanoAODv6-1-1_2017/200613_070408/0000/'], 'mc','','2017', '','5765.4','41.53','182217609'] ## '84,597,528' ## now we have ore events ?  182,217,609

## example nanoAOD datset on DAS where I got number of events from
## https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fphys03&input=dataset+%3D+%2FTTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8%2Fpalencia-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc%2FUSER
mc2017_samples['2017_TTTo2L2Nu'] = [['/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/palencia-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/group/phys_top/topNanoAOD/v6-1-1/2017/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2017/200610_154949/0000/'], 'mc','','2017', '','87.31','41.53', '9000000 ' ] ##'8926992'] what is going on with number of events?

mc2017_samples['2017_ST_tW'] = [['/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/palencia-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/group/phys_top/topNanoAOD/v6-1-1/2017/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2017/200610_154657/0000/'], 'mc','','2017', '','19.47','41.53','4955102']


mc2017_samples['2017_ST_atW'] = [['/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/palencia-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/group/phys_top/topNanoAOD/v6-1-1/2017/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2017/200610_154434/0000/'], 'mc','','2017', '','19.47','41.53','11271078']

mc2017_samples['2017_WWTo2L2Nu'] = [['/WWTo2L2Nu_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/WWTo2L2Nu_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2017/200615_072350/0000/'], 'mc','','2017', '','12.178','41.53','2000000']

mc2017_samples['2017_ZZTo2L2Nu'] = [['/ZZTo2L2Nu_13TeV_powheg_pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/ZZTo2L2Nu_13TeV_powheg_pythia8/TopNanoAODv6-1-1_2017/200615_073400/0000/'], 'mc','','2017', '','0.564','41.53','8744768']

mc2017_samples['2017_ZZTo4L'] = [['/ZZTo4L_13TeV_powheg_pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/ZZTo4L_13TeV_powheg_pythia8/TopNanoAODv6-1-1_2017/200615_073451/0000/'], 'mc','','2017', '','1.212','41.53','16075000']




mc2017_samples['2017_WZTo2L2Q'] = [['/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/TopNanoAODv6-1-1_2017/200615_072720/0000/'], 'mc','','2017', '','5.595','41.53','27582164']

mc2017_samples['2017_WZTo3LNu'] = [['/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TopNanoAODv6-1-1_2017/200615_072814/0000/'], 'mc','','2017', '','4.43','41.53','10987679]

mc2017_samples['2017_WJetsToLNu'] = [['/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv6-1-1_2017/200615_072257/0000/'], 'mc','','2017', '','61526.7','41.53','74635450']

mc2017_samples['2017_TTWJetsToQQ'] = [['/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/TopNanoAODv6-1-1_2017/200615_071451/0000/'], 'mc','','2017', '','0.4062','41.53','811306']

mc2017_samples['2017_TTWJetsToLNu'] = [['/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/TopNanoAODv6-1-1_2017/200615_071425/0000/'], 'mc','','2017', '','0.2043','41.53','4925829']

mc2017_samples['2017_TTZToLLNuNu'] = [['/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/TopNanoAODv6-1-1_2017/200615_071611/0000/'], 'mc','','2017', '','0.2529','41.53','7932650']

mc2017_samples['2017_TTZToQQ'] = [['/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/TopNanoAODv6-1-1_2017/200615_071706/0000/'], 'mc','','2017', '','0.5297','41.53','750000']



data2017_samples['2017_B_MuonEG'] = [['/MuonEG/piedavid-Run2017B-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/MuonEG/TopNanoAODv6-1-1_2017/200615_081001/0000/'], 'data','MuonEG','2017', 'B','1','1','1']
data2017_samples['2017_C_MuonEG'] = [['/MuonEG/piedavid-Run2017C-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/MuonEG/TopNanoAODv6-1-1_2017/200615_081027/0000/'], 'data','MuonEG','2017', 'C','1','1','1']


data2017_samples['2017_D_MuonEG'] = [['/MuonEG/piedavid-Run2017D-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/MuonEG/TopNanoAODv6-1-1_2017/200615_081058/0000/'], 'data','MuonEG','2017', 'D','1','1','1']
data2017_samples['2017_E_MuonEG'] = [['/MuonEG/piedavid-Run2017E-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/MuonEG/TopNanoAODv6-1-1_2017/200615_081126/0000/'], 'data','MuonEG','2017', 'E','1','1','1']
data2017_samples['2017_F_MuonEG'] = [['/MuonEG/piedavid-Run2017F-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/MuonEG/TopNanoAODv6-1-1_2017/200615_081152/0000/'], 'data','MuonEG','2017', 'F','1','1','1']




data2017_samples['2017_B_SingleMuon'] = [['/SingleMuon/piedavid-Run2017B-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleMuon/TopNanoAODv6-1-1_2017/200612_180815/0000/'], 'data','SingleMuon','2017', 'B','1','1','1']
data2017_samples['2017_C_SingleMuon'] = [['/SingleMuon/piedavid-Run2017C-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleMuon/TopNanoAODv6-1-1_2017/200612_180842/0000/'], 'data','SingleMuon','2017', 'C','1','1','1']
###past here conversion is NOT complete
data2017_samples['2017_D_SingleMuon'] = [['/SingleMuon/piedavid-Run2017D-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleMuon/TopNanoAODv6-1-1_2017/200612_180908/0000/'], 'data','SingleMuon','2017', 'D','1','1','1']
data2017_samples['2017_E_SingleMuon'] = [['/SingleMuon/piedavid-Run2017E-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleMuon/TopNanoAODv6-1-1_2017/200612_180934/0000/'], 'data','SingleMuon','2017', 'E','1','1','1']
data2017_samples['2017_F_SingleMuon'] = [['/SingleMuon/piedavid-Run2017F-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleMuon/TopNanoAODv6-1-1_2017/200612_181001/0000/'], 'data','SingleMuon','2017', 'F','1','1','1']

data2017_samples['2017_B_SingleElectron'] = [['/SingleElectron/piedavid-Run2017B-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleElectron/TopNanoAODv6-1-1_2017/200615_081218/0000/'], 'data','SingleElectron','2017', 'B','1','1','1']
data2017_samples['2017_C_SingleElectron'] = [['/SingleElectron/piedavid-Run2017C-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleElectron/TopNanoAODv6-1-1_2017/200615_081246/0000/'], 'data','SingleElectron','2017', 'C','1','1','1']
data2017_samples['2017_D_SingleElectron'] = [['/SingleElectron/piedavid-Run2017D-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleElectron/TopNanoAODv6-1-1_2017/200615_081311/0000/'], 'data','SingleElectron','2017', 'D','1','1','1']
data2017_samples['2017_E_SingleElectron'] = [['/SingleElectron/piedavid-Run2017E-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleElectron/TopNanoAODv6-1-1_2017/200615_081338/0000/'], 'data','SingleElectron','2017', 'E','1','1','1']
data2017_samples['2017_F_SingleElectron'] = [['/SingleElectron/piedavid-Run2017F-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleElectron/TopNanoAODv6-1-1_2017/200615_081411/0000/'], 'data','SingleElectron','2017', 'F','1','1','1']

data2017_samples['2017_B_DoubleEG'] = [['/DoubleEG/piedavid-Run2017B-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleEG/TopNanoAODv6-1-1_2017/200615_080330/0000/'], 'data','DoubleEG','2017', 'B','1','1','1']
data2017_samples['2017_C_DoubleEG'] = [['/DoubleEG/piedavid-Run2017C-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleEG/TopNanoAODv6-1-1_2017/200615_080356/0000/'], 'data','DoubleEG','2017', 'C','1','1','1']
data2017_samples['2017_D_DoubleEG'] = [['/DoubleEG/piedavid-Run2017D-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleEG/TopNanoAODv6-1-1_2017/200615_080422/0000/'], 'data','DoubleEG','2017', 'D','1','1','1']
data2017_samples['2017_E_DoubleEG'] = [['/DoubleEG/piedavid-Run2017E-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleEG/TopNanoAODv6-1-1_2017/200615_080448/0000/'], 'data','DoubleEG','2017', 'E','1','1','1']
data2017_samples['2017_F_DoubleEG'] = [['/DoubleEG/piedavid-Run2017F-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleEG/TopNanoAODv6-1-1_2017/200615_080514/0000/'], 'data','DoubleEG','2017', 'F','1','1','1']

data2017_samples['2017_B_DoubleMu'] = [['/DoubleMuon/piedavid-Run2017B-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleMuon/TopNanoAODv6-1-1_2017/200615_080544/0000/'], 'data','DoubleMu','2017', 'B','1','1','1']
data2017_samples['2017_C_DoubleMu'] = [['/DoubleMuon/piedavid-Run2017C-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleMuon/TopNanoAODv6-1-1_2017/200615_080609/0000/'], 'data','DoubleMu','2017', 'C','1','1','1']
data2017_samples['2017_D_DoubleMu'] = [['/DoubleMuon/piedavid-Run2017D-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleMuon/TopNanoAODv6-1-1_2017/200615_080634/0000/'], 'data','DoubleMu','2017', 'D','1','1','1']
data2017_samples['2017_E_DoubleMu'] = [['/DoubleMuon/piedavid-Run2017E-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleMuon/TopNanoAODv6-1-1_2017/200615_080700/0000/'], 'data','DoubleMu','2017', 'E','1','1','1']
data2017_samples['2017_F_DoubleMu'] = [['/DoubleMuon/piedavid-Run2017F-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleMuon/TopNanoAODv6-1-1_2017/200615_080726/0000/'], 'data','DoubleMu','2017', 'F','1','1','1']


#/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2017/IIHE_Ntuple/ntuple_SMEFTfr_ST_clequ3_emutu

mc2017_samples['2017_LFVStVecC'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_155453/0000/'], 'mc','','2017', '','0.04' ,'41.53','500000']
mc2017_samples['2017_LFVStVecU'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_155716/0000/'], 'mc','','2017', '','0.452' ,'41.53','494000']
mc2017_samples['2017_LFVTtVecC'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201008_025340/0000/'], 'mc','','2017', '','0.032'  ,'41.53','500000']
mc2017_samples['2017_LFVTtVecU'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201008_025758/0000/'], 'mc','','2017', '','0.032','41.53','498000']

#tensor interaction
mc2017_samples['2017_LFVStTensorC'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_150454/0000/'], 'mc','','2017', '','0.187' ,'41.53','500000']
mc2017_samples['2017_LFVStTensorU'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_150303/0000/'], 'mc','','2017', '','1.9' ,'41.53','500000']
mc2017_samples['2017_LFVTtTensorC'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_153218/0000/'], 'mc','','2017', '','0.1876','41.53','500000']
mc2017_samples['2017_LFVTtTensorU'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_152919/0000/'], 'mc','','2017', '','0.1876','41.53','500000']

#scalar interaction                                                                                                                                                                                                
mc2017_samples['2017_LFVStScalarC'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_133418/0000/'], 'mc','','2017', '','0.008' ,'41.53','500000']
mc2017_samples['2017_LFVStScalarU'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_145731/0000/'], 'mc','','2017', '','0.102' ,'41.53','500000']
mc2017_samples['2017_LFVTtScalarC'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_153437/0000/'], 'mc','','2017', '','0.004'  ,'41.53','500000']
mc2017_samples['2017_LFVTtScalarU'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201008_024659/0000/'], 'mc','','2017', '','0.004','41.53','500000']



#/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/
#201007_133418  201007_145731  201007_150303  201007_150454  201007_152919  201007_153218  201007_153437  201007_155453  201007_155716  201008_024659  201008_025340  201008_025758
