import math
import sys
import ROOT
from ROOT import THStack
from ROOT import TGaxis
from ROOT import TColor
from array import array
import numpy as np
import os
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1;")
ROOT.TH1.AddDirectory(ROOT.kFALSE)
ROOT.gStyle.SetOptStat(0)
import argparse
TGaxis.SetMaxDigits(2)


def cutFlowTable(hists, lepIDs, samples, regions):
    table = "\n"
    for ilep in range(0,len(lepIDs)):
    #    table += '\\begin{sidewaystable*}' + "\n"
        table += '\\begin{table}' + "\n"
        table += '\\centering' + "\n"
        table += '\\caption{' +lepIDs[ilep] + "}\n"
        table += '\\resizebox{\\textwidth}{!}{ \n'
        table += '\\begin{tabular}{|l|' + ''.join([('' if False else 'l|') for c in regions]).strip() + '}' + "\n"
        table += '\\hline' + "\n"
        table += 'Samples ' + ''.join([('' if False else ' & '+c) for c in regions]).strip() + '\\\\' + "\n"
        table += '\\hline' + "\n"

        for ids, s in enumerate(samples):
            table += s
            for idr, r in enumerate(regions):
                table += (' & ' + str(round(hists[ids][0][idr].GetBinContent(ilep+1), 2)))
            table += '\\\\' + "\n"
        table += '\\hline' + "\n"
        table += '\\end{tabular}}' + "\n"
        table += '\\end{table}' + "\n"
    #    table += '\\end{sidewaystable*}' + "\n"
        # table += '\\\\' + "\n"
    return table


year = ['2017']
regions = ["lll", "lllOffZ", "lllOffZMetg20", "lllOffZMetg20Jetgeq1Bleq1"]
channels = ["eee", "emul", "mumumu"]
channels = ["emul"]

# set up an argument parser
parser = argparse.ArgumentParser()

parser.add_argument('--v', dest='VERBOSE', default=True)
parser.add_argument('--l', dest='LOCATION',default='/eos/user/b/bharikri/NTuples/TopLFV/NanoAOD_Results/NanoPosttest_Feb28_test2_2017_LFVTtVecU/')

ARGS = parser.parse_args()

verbose = ARGS.VERBOSE
HistAddress = ARGS.LOCATION

Samples = ["NanoPosttest_Feb28_test2_2017_LFVTtVecU.root"]
SamplesName = ['LFVTtVecU']
SamplesNameLatex = ['LFVTtVecU']
lepIDs = ["Electron\_CutBased(tight) + Muon\_mvaId(medium) + Muon\_mediumId","Electron\_mvaFall17V2Iso\_WP80 + Muon\_mvaId(medium) + Muon\_mediumId","Electron\_mvaFall17V2Iso\_WP90 + Muon\_mvaId(medium) + Muon\_mediumId","Electron\_mvaFall17V2Iso\_WPL + Muon\_mvaId(medium) + Muon\_mediumId","Electron\_mvaTOP(medium) + Muon\_mvaId(medium) + Muon\_mediumId","Electron\_mvaTTH(medium 0.65) + Muon\_mvaId(medium) + Muon\_mediumId","Electron\_CutBased(tight) + Muon\_mvaId(medium)","Electron\_CutBased(tight) + Muon\_mvaId(tight)","Electron\_CutBased(tight) + Muon\_mvaTOP(medium)","Electron\_CutBased(tight) + Muon\_mvaTTH(medium 0.65)"]

Hists = []

Files = []
for f in range(len(Samples)):
    l0=[]
    Files.append(ROOT.TFile.Open(HistAddress +Samples[f]))
    print(HistAddress +Samples[f])
    for numch, namech in enumerate(channels):
        l1=[]
        for numreg, namereg in enumerate(regions):
            #print(namech + '_' + namereg)
            h= Files[f].Get(namech + '_' + namereg)
            l1.append(h)
        l0.append(l1)
    Hists.append(l0)  


le = '\\documentclass{article}' + "\n"
le += '\\usepackage[margin = 0.9 in , top = 15mm, left = 25mm, right = 15mm]{geometry}' + "\n"
le += '\\usepackage{rotating}' + "\n"
le += '\\begin{document}' + "\n"

le += cutFlowTable(Hists, lepIDs, SamplesNameLatex, regions)

le += '\\end{document}' + "\n"

print(le)

with open('Cutflow.tex', 'w') as fout:
    for i in range(len(le)):
        fout.write(le[i])
