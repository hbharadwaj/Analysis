import argparse
from ROOT import THStack
from ROOT import TGaxis
from ROOT import TColor
from array import array
import math
import gc
import sys
import ROOT
import numpy as np
import copy
import os
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1;")
ROOT.TH1.AddDirectory(ROOT.kFALSE)
ROOT.gStyle.SetOptStat(0)
TGaxis.SetMaxDigits(2)


def stackPlots(hists, Fnames, ch="channel", reg="region", year='2017', var="sample", varname="v"):
    if not os.path.exists(year):
       os.makedirs(year)
    if not os.path.exists(year + '/' + ch):
       os.makedirs(year + '/' + ch)
    if not os.path.exists(year + '/' + ch + '/'+reg):
       os.makedirs(year + '/' + ch + '/'+reg)
    hs = ROOT.THStack("hs", "")
    for num in range(len(hists)):
        hists[num].SetBinContent(hists[num].GetXaxis().GetNbins(), hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()) + hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()+1))

    canvas = ROOT.TCanvas(year+ch+reg+var, year+ch+reg+var, 50, 50, 865, 780)
    canvas.SetGrid()
    canvas.SetBottomMargin(0.17)
    canvas.cd()

    legend = ROOT.TLegend(0.7, 0.55, 0.9, 0.88)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)

    pad1=ROOT.TPad("pad1", "pad1", 0, 0.315, 1, 0.99 , 0)#used for the hist plot
    pad1.Draw()
    pad1.SetBottomMargin(0.1)
    pad1.SetLeftMargin(0.14)
    pad1.SetRightMargin(0.05)
    pad1.SetFillStyle(0)
    pad1.cd()
    pad1.SetLogx(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kFALSE)

    y_min = 0
    y_max = 1.1*hists[0].GetMaximum()
    hists[0].GetYaxis().SetTitle('Events')
    hists[0].GetXaxis().SetLabelSize(0)
    hists[0].GetYaxis().SetTitleOffset(0.8)
    hists[0].GetYaxis().SetTitleSize(0.07)
    hists[0].GetYaxis().SetLabelSize(0.04)
    hists[0].GetYaxis().SetRangeUser(y_min, y_max)

    hists[0].GetXaxis().SetTitle(varname)
    hists[0].GetXaxis().SetMoreLogLabels()
    hists[0].GetXaxis().SetNoExponent()
    # hists[0].GetXaxis().SetTitleSize(0.04/0.3)
    hists[0].GetXaxis().SetTitleFont(42)
    hists[0].GetXaxis().SetTickLength(0.05)
    # hists[0].GetXaxis().SetLabelSize(0.115)
    # hists[0].GetXaxis().SetLabelOffset(0.02)
    hists[0].GetXaxis().SetTitleOffset(1.1)
    
    for num in range(0, len(hists)):
        # hists[num].Draw("same")
        hs.Add(hists[num])

    hs.Draw("nostack")
    hs.GetYaxis().SetRangeUser(y_min, y_max)
    hs.GetXaxis().SetTitle(varname)
    hs.GetXaxis().SetNoExponent()
    hs.GetYaxis().SetTitle('Events')

    Lumi = '137.42'
    if (year == '2016'):
        Lumi = '35.92'
    if (year == '2017'):
        Lumi = '41.53'
    if (year == '2018'):
        Lumi = '59.97'
    label_cms = "CMS Preliminary"
    Label_cms = ROOT.TLatex(0.2, 0.92, label_cms)
    Label_cms.SetNDC()
    Label_cms.SetTextFont(61)
    Label_cms.Draw()
    Label_lumi = ROOT.TLatex(0.71, 0.92, Lumi+" fb^{-1} (13 TeV)")
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.Draw("same")
    Label_channel = ROOT.TLatex(0.2, 0.8, year + " / "+ch+" ("+reg+")")
    Label_channel.SetNDC()
    Label_channel.SetTextFont(42)
    Label_channel.Draw("same")

    for H in range(len(hists)):
        legend.AddEntry(hists[H], Fnames[H], 'L')
    legend.Draw("same")

    pad1.Update()
    canvas.Print(year + '/' + ch + '/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()



#year=['2016','2017','2018','All']
year=['2017']
regions = ["lll"]
regions = ["lll", "lllOnZ", "lllOffZ", "lllB0", "lllB1", "lllBgeq2", "lllMetl20", "lllMetg20", "lllMetg20B1", "lllMetg20Jetleq2B1", "lllMetg20Jetgeq1B0", "lllMetg20Jet1B1", "lllMetg20Jet2B1", "lllMetg20Jetgeq3B1", "lllMetg20Jetgeq2B2", "lllDphil1p6", "lllMetg20OnZB0", "lllMetg20Jetgeq1Bleq1", "lllBleq1", "lllMetg20Jetgeq1B1", "lllMetg20Jetgeq2Bleq1", "lllMetg20Jetgeq2B1", "lllMVAoutput", "lllOffzMVAoutput", "lllMetg20MVAoutput", "lllMetg20B1MVAoutput", "lllMetg20Jetgeq2Bleq1MVAoutput"]
channels = ["emul"]
# channels=["eee", "emul", "mumumu"]
variables = ["lep1Pt", "Topmass", "llM", "BDT"]
# variables = ["lep1Pt", "lep1Eta", "lep1Phi", "lep2Pt", "lep2Eta", "lep2Phi", "lep3Pt", "lep3Eta", "lep3Phi","LFVePt", "LFVeEta", "LFVePhi", "LFVmuPt", "LFVmuEta", "LFVmuPhi", "balPt", "balEta", "balPhi", "Topmass","llM", "llPt", "llDr", "llDphi", "jet1Pt", "jet1Eta", "jet1Phi", "njet", "nbjet", "Met", "MetPhi", "nVtx", "llMZw", "LFVTopmass", "BDT"]
variablesName = ["Leading lepton p_{T} [GeV]", "Standard top mass [GeV]", "M(ll) [GeV]", "BDT"]
# variablesName = ["Leading lepton p_{T} [GeV]", "Leading lepton #eta", "Leading lepton #varphi", "2nd-Leading lepton p_{T} [GeV]", "2nd-Leading lepton #eta", "2nd-Leading lepton #varphi", "3rd-Leading lepton p_{T} [GeV]", "3rd-Leading lepton #eta", "3rd-Leading lepton #varphi", "cLFV electron p_{T} [GeV]", "cLFV electron #eta", "cLFV electron #varphi", "cLFV muon p_{T} [GeV]", "cLFV muon #eta","cLFV muon #varphi", "Bachelor lepton p_{T} [GeV]", "Bachelor lepton #eta", "Bachelor lepton #varphi", "Standard top mass [GeV]", "M(ll) [GeV]", "p_{T}(ll) [GeV]", "#Delta R(ll)", "#Delta #varphi(ll)", "Leading jet p_{T} [GeV]", "Leading jet #eta", "Leading jet #varphi", "Number of jets", "Number of b-tagged jets", "MET [GeV]", "#varphi(MET)", "Number of vertices", "M(ll) (OSSF) [GeV]", "cLFV top mass [GeV]", "BDT"]


# set up an argument parser
parser = argparse.ArgumentParser()

parser.add_argument('--v', dest='VERBOSE', default=True)
parser.add_argument('--l', dest = 'LOCATION', default= '/afs/cern.ch/user/b/bharikri/Projects/TopLFV/Updated_BDT/hists/')

ARGS = parser.parse_args()

verbose = ARGS.VERBOSE
HistAddress = ARGS.LOCATION

# Samples = ['TTbar.root', 'SMEFTfr_TT_vector_emutc.root', 'SMEFTfr_TT_vector_emutu.root']
# SamplesName = ['t#bar{t}', 'TT\_vector\_emutc', 'TT\_vector\_emutu']

Samples = ['TTbar.root', 'TTWJetsToLNu.root', 'WZTo3LNu.root', 'SMEFTfr_TT_vector_emutc.root', 'SMEFTfr_TT_vector_emutu.root', 'SMEFTfr_ST_vector_emutc.root', 'SMEFTfr_ST_vector_emutu.root']
SamplesName = ['t#bar{t}', 'TTWJetsToLNu', 'WZTo3LNu', 'TT\_vector\_emutc', 'TT\_vector\_emutu', 'ST\_vector\_emutc', 'ST\_vector\_emutu']

colors = [ROOT.kBlack, ROOT.kBlue+2, ROOT.kMagenta+2, ROOT.kGreen-2, ROOT.kRed-3, ROOT.kOrange+7, ROOT.kCyan+2]


Hists = []
for numyear, nameyear in enumerate(year):
    l0 = []
    Files = []
    for f in range(len(Samples)):
        l1 = []
        Files.append(ROOT.TFile.Open(
            HistAddress + nameyear + '_' + Samples[f]))
        for numch, namech in enumerate(channels):
            l2 = []
            for numreg, namereg in enumerate(regions):
                l3 = []
                for numvar, namevar in enumerate(variables):
                    # print(namech + '_' + namereg + '_' + namevar)
                    h = Files[f].Get(namech + '_' + namereg + '_' + namevar)
                    h.SetFillColor(colors[f])
                    h.SetLineColor(colors[f])
                    # h.SetLineWidth(5)
                    h.GetXaxis().SetNoExponent()
                    h.GetYaxis().SetNoExponent()
                    h.GetYaxis().SetTitle('Events')
                    h.GetXaxis().SetLabelSize(0)
                    h.GetYaxis().SetTitleOffset(0.8)
                    h.GetYaxis().SetTitleSize(0.07)
                    h.GetYaxis().SetLabelSize(0.04)
                    l3.append(h)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    Hists.append(l0)

for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                HH=[]
                for f in range(len(Samples)):
                    HH.append(Hists[numyear][f][numch][numreg][numvar])
                stackPlots(HH, SamplesName, namech, namereg, nameyear,namevar,variablesName[numvar])
