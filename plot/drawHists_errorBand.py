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
from array import array
from ROOT import TColor
from ROOT import TGaxis
from ROOT import THStack
import gc
from operator import truediv
import copy
import argparse
TGaxis.SetMaxDigits(2)

def draw(hists, sys, ch = "channel", reg = "region", year='2017', var="sample", varname="v"):
    canvas = ROOT.TCanvas(year+ch+reg+var,year+ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.cd()
    hists.Draw()
    canvas.Print('sys/'+ year + '/' + ch +'/'+reg+'/'+ sys +var + ".png")
#    del legend
#    del mg
    del canvas
    gc.collect()

def compareError(histsup,histsdown, sys, ch = "channel", reg = "region", year='2017', var="sample", varname="v"):
    if not os.path.exists('sys/'+year):
       os.makedirs('sys/'+ year)
    if not os.path.exists('sys/'+year + '/' + ch):
       os.makedirs('sys/'+year + '/' + ch)
    if not os.path.exists('sys/'+year + '/' + ch +'/'+reg):
       os.makedirs('sys/'+year + '/' + ch +'/'+reg)

    canvas = ROOT.TCanvas(year+ch+reg+var,year+ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.cd()

    legend = ROOT.TLegend(0.1,0.3,1,0.8)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.22)

    pad1=ROOT.TPad("pad1", "pad1", 0, 0., 0.1, 0.99 , 0)#used for the hist plot
    pad2=ROOT.TPad("pad2", "pad2", 0.1, 0.0, 1, 1 , 0)#used for the ratio plot
    pad1.Draw()
    pad2.Draw()
#    pad2.SetGridy()
#    pad2.SetGridx()
    pad2.SetTickx()
    pad1.SetBottomMargin(0.1)
    pad1.SetLeftMargin(0.01)
    pad1.SetRightMargin(0.01)
    pad2.SetBottomMargin(0.1)
    pad2.SetLeftMargin(0.11)
    pad2.SetRightMargin(0.1)
    pad2.SetFillStyle(0)
    pad1.SetFillStyle(0)
    pad1.SetLogx(ROOT.kFALSE)
    pad2.SetLogx(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kFALSE)

    pad2.cd()
    maxi=0
    for n,G in enumerate(histsup):
        histsup[n].SetLineColor(n+1)
        histsup[n].SetLineWidth(2)
        histsup[n].SetFillColor(0)
        legend.AddEntry(histsup[n],sys[n],'L')
        if(histsup[n].GetMaximum()>maxi):
            maxi=G.GetMaximum()
        histsdown[n].SetLineColor(n+1)
        histsdown[n].SetFillColor(0)
        histsdown[n].SetLineWidth(2)
        if n==4:
            histsup[n].SetLineColor(ROOT.kOrange)
            histsdown[n].SetLineColor(ROOT.kOrange)
    histsup[0].SetTitle( '' )
    histsup[0].GetYaxis().SetTitle( 'Uncertainty (%)' )
    histsup[0].GetXaxis().SetTitle(varname)
    histsup[0].GetXaxis().SetLabelSize(0.04)
    histsup[0].GetYaxis().SetLabelSize(0.04)
    histsup[0].GetXaxis().SetTitleSize(0.04)
    histsup[0].GetYaxis().SetTitleSize(0.04)
    histsup[0].GetXaxis().SetTitleOffset(0.95)
    histsup[0].GetYaxis().SetTitleOffset(1)
    histsup[0].GetYaxis().SetNdivisions(804)
    histsup[0].GetXaxis().SetNdivisions(808)   
    histsup[0].GetYaxis().SetRangeUser(-2.5*maxi,1.5*maxi)
    histsup[0].Draw('hist')
    for n,G in enumerate(histsup):
        histsup[n].Draw('samehist')
        histsdown[n].Draw('samehist')
    histsup[0].Draw('samehist')
    histsup[0].Draw("AXISSAMEY+")
    histsup[0].Draw("AXISSAMEX+")
    Lumi = '137.42'
    if (year == '2016'):
        Lumi = '35.92'
    if (year == '2017'):
        Lumi = '41.53'
    if (year == '2018'):
        Lumi = '59.97'
    label_cms="CMS Preliminary"
    Label_cms = ROOT.TLatex(0.22,0.92,label_cms)
    Label_cms.SetTextSize(0.035)
    Label_cms.SetNDC()
    Label_cms.SetTextFont(61)
    Label_cms.Draw()
    Label_lumi = ROOT.TLatex(0.65,0.92,Lumi+" fb^{-1} (13 TeV)")
    Label_lumi.SetTextSize(0.035)
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.Draw("same")
    Label_channel = ROOT.TLatex(0.2,0.85,year +" / "+ch+" ("+reg+")")
    Label_channel.SetNDC()
    Label_channel.SetTextSize(0.035)
    Label_channel.SetTextFont(42)
    Label_channel.Draw("same") 
    pad1.cd()
    legend.Draw("same")
    canvas.Print('sys/'+ year + '/' + ch +'/'+reg+'/sys'+var + ".png")
    del canvas
    gc.collect()

def stackPlotsError(hists, SignalHists,error, errorRatio, Fnames, ch = "channel", reg = "region", year='2017', var="sample", varname="v"):
    if not os.path.exists('sys/'+year):
       os.makedirs('sys/'+ year)
    if not os.path.exists('sys/'+year + '/' + ch):
       os.makedirs('sys/'+year + '/' + ch)
    if not os.path.exists('sys/'+year + '/' + ch +'/'+reg):
       os.makedirs('sys/'+year + '/' + ch +'/'+reg)
    hs = ROOT.THStack("hs","")
#    for num in range(len(hists)):
#        hists[num].SetBinContent(hists[num].GetXaxis().GetNbins(), hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()) + hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()+1))
#    for num in range(len(SignalHists)):
#        SignalHists[num].SetBinContent(SignalHists[num].GetXaxis().GetNbins(),SignalHists[num].GetBinContent(SignalHists[num].GetXaxis().GetNbins()) + SignalHists[num].GetBinContent(SignalHists[num].GetXaxis().GetNbins()+1))
    for num in range(1,len(hists)):
        hs.Add(hists[num])

    dummy = hists[0].Clone()
    if ('emul' not in ch) or ('OnZ' in reg):
       showData = True
    else:
       showData = False
       dummy.Reset("ICE")

    
    canvas = ROOT.TCanvas(year+ch+reg+var,year+ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.SetBottomMargin(0.17)
    canvas.cd()

    if showData:
       legend = ROOT.TLegend(0.72,0.74,0.82,0.88)
    else:
       legend = ROOT.TLegend(0.72,0.775,0.82,0.88)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0);
    legend.SetTextFont(42)
    legend.SetTextSize(0.03)
    legend2 = ROOT.TLegend(0.82,0.775,0.92,0.88)
    legend2.SetBorderSize(0)
    legend2.SetFillStyle(0);
    legend2.SetTextFont(42)
    legend2.SetTextSize(0.03)
    if showData:
       legend3 = ROOT.TLegend(0.72,0.66,0.83,0.74)
    else:
       legend3 = ROOT.TLegend(0.72,0.695,0.83,0.775)
    legend3.SetBorderSize(0)
    legend3.SetFillStyle(0);
    legend3.SetTextFont(42)
    legend3.SetTextSize(0.03)

    pad1=ROOT.TPad("pad1", "pad1", 0, 0.315, 1, 0.99 , 0)#used for the hist plot
    pad2=ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.305 , 0)#used for the ratio plot
    pad1.Draw()
    pad2.Draw() 
    pad2.SetGridy()
    pad2.SetTickx()
    pad1.SetBottomMargin(0.02)
    pad1.SetLeftMargin(0.14)
    pad1.SetRightMargin(0.05)
    pad2.SetTopMargin(0.1)
    pad2.SetBottomMargin(0.4)
    pad2.SetLeftMargin(0.14)
    pad2.SetRightMargin(0.05)
    pad2.SetFillStyle(0)
    pad1.SetFillStyle(0)
    pad1.cd()
    pad1.SetLogx(ROOT.kFALSE)
    pad2.SetLogx(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kFALSE)

    y_min=0
    if showData:
       y_max=1.7*hists[0].GetMaximum()
    else:
       y_max=1.7*hs.GetStack().Last().GetMaximum()
    dummy.SetMarkerStyle(20)
    dummy.SetMarkerSize(1.2)
    dummy.SetTitle("")
    dummy.GetYaxis().SetTitle('Events')
    dummy.GetXaxis().SetLabelSize(0)
    dummy.GetYaxis().SetTitleOffset(0.8)
    dummy.GetYaxis().SetTitleSize(0.07)
    dummy.GetYaxis().SetLabelSize(0.04)
    dummy.GetYaxis().SetRangeUser(y_min,y_max)
    dummy.GetYaxis().SetNoExponent()
    dummy.Draw("ex0")
    hs.Draw("histSAME")
    for H in SignalHists:
        H.SetLineWidth(2)
        H.SetFillColor(0)
        H.SetLineStyle(9)
        H.Draw("histSAME")
    dummy.Draw("ex0SAME")
    dummy.Draw("AXISSAMEY+")
    dummy.Draw("AXISSAMEX+")

    error.SetFillColor(13)
    error.SetLineColor(13)
    error.SetFillStyle(3004)
    error.Draw("2")

    Lumi = '137.42'
    if (year == '2016'):
        Lumi = '35.92'
    if (year == '2017'):
        Lumi = '41.53'
    if (year == '2018'):
        Lumi = '59.97'
    label_cms="CMS Preliminary"
    Label_cms = ROOT.TLatex(0.15,0.92,label_cms)
    Label_cms.SetNDC()
    Label_cms.SetTextFont(61)
    Label_cms.Draw()
    Label_lumi = ROOT.TLatex(0.71,0.92,Lumi+" fb^{-1} (13 TeV)")
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.Draw("same")
    Label_channel = ROOT.TLatex(0.2,0.8,year +" / "+ch+" ("+reg+")")
    Label_channel.SetNDC()
    Label_channel.SetTextFont(42)
    Label_channel.Draw("same")

    if showData:
       legend.AddEntry(dummy,Fnames[0],'ep')
    for num in range(1,len(hists)):
        if num<(len(hists)-2):
           legend.AddEntry(hists[num],Fnames[num],'F')
        else:
           legend2.AddEntry(hists[num],Fnames[num],'F')
    legend2.AddEntry(error,'Stat. #oplus syst. ','F')
    for H in range(len(SignalHists)):
        legend3.AddEntry(SignalHists[H], Fnames[len(hists)+H],'L')
    legend.Draw("same")
    legend2.Draw("same")
    legend3.Draw("same")

    if (showData) and (hs.GetStack().Last().Integral()>0):
        Label_DM = ROOT.TLatex(0.2,0.75,"Data/MC = " + str(round(hists[0].Integral()/hs.GetStack().Last().Integral(),2)))
        Label_DM.SetNDC()
        Label_DM.SetTextFont(42)
        Label_DM.Draw("same")

    pad1.Update()

    pad2.cd()
    SumofMC = hs.GetStack().Last()
    dummy_ratio = hists[0].Clone()
    dummy_ratio.SetTitle("")
    dummy_ratio.SetMarkerStyle(20)
    dummy_ratio.SetMarkerSize(1.2)
    dummy_ratio.GetXaxis().SetTitle(varname)
#    dummy_ratio.GetXaxis().CenterTitle()
    dummy_ratio.GetYaxis().CenterTitle()
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()  
    dummy_ratio.GetXaxis().SetTitleSize(0.04/0.3)
    dummy_ratio.GetYaxis().SetTitleSize(0.04/0.3)
    dummy_ratio.GetXaxis().SetTitleFont(42)
    dummy_ratio.GetYaxis().SetTitleFont(42)
    dummy_ratio.GetXaxis().SetTickLength(0.05)
    dummy_ratio.GetYaxis().SetTickLength(0.05)
    dummy_ratio.GetXaxis().SetLabelSize(0.115)
    dummy_ratio.GetYaxis().SetLabelSize(0.089)
    dummy_ratio.GetXaxis().SetLabelOffset(0.02)
    dummy_ratio.GetYaxis().SetLabelOffset(0.01)
    dummy_ratio.GetYaxis().SetTitleOffset(0.42)
    dummy_ratio.GetXaxis().SetTitleOffset(1.1)
    dummy_ratio.GetYaxis().SetNdivisions(504)    
    dummy_ratio.GetYaxis().SetRangeUser(0,2)
    dummy_ratio.Divide(SumofMC)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Data/Pred.')
    if not showData:
       dummy_ratio.Reset("ICE")
    dummy_ratio.Draw('ex0')
    dummy_ratio.Draw("AXISSAMEY+")
    dummy_ratio.Draw("AXISSAMEX+")
    errorRatio.SetFillColor(13)
    errorRatio.SetLineColor(13)
    errorRatio.SetFillStyle(3004)
    errorRatio.Draw("2")
    dummy_ratio.Draw('ex0same')
    canvas.Print('sys/'+ year + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()


year=['2017']
#year=['2018','All']
LumiErr = [0.023]
#year=['2016']
regions=["lll"]
#regions=["ll","llOffZ"]
channels=["eee", "emul", "mumumu"];
#channels=["emu"];
variables=["lep1Pt","lep1Eta","lep1Phi","lep2Pt","lep2Eta","lep2Phi","lep3Pt","lep3Eta","lep3Phi",
           "LFVePt","LFVeEta","LFVePhi","LFVmuPt","LFVmuEta","LFVmuPhi","balPt","balEta","balPhi","Topmass",
           "lllM","lllPt","lllHt","lllMt","jet1Pt","jet1Eta","jet1Phi","njet","nbjet","Met","MetPhi","nVtx",
           "llZM","llZPt","llZDr","llZDphi","LFVTopmass","llM","llPt","llDr","llDphi",
           "Ht","Ms","ZlDr","ZlDphi","JeDr","JmuDr"]
#variables=["lep1Pt","lep1Eta","lep1Phi","lep2Pt","lep2Eta","lep2Phi","llM","llPt","llDr","llDphi","jet1Pt","jet1Eta","jet1Phi","njet","nbjet","Met"]
#variables=["nbjet","Met","nVtx","llMZw"]
variablesName=["Leading lepton p_{T} [GeV]","Leading lepton #eta","Leading lepton #varphi","2nd-Leading lepton p_{T} [GeV]","2nd-Leading lepton #eta","2nd-Leading lepton #varphi","3rd-Leading lepton p_{T} [GeV]","3rd-Leading lepton #eta","3rd-Leading lepton #varphi","cLFV electron p_{T} [GeV]","cLFV electron #eta","cLFV electron #varphi","cLFV muon p_{T} [GeV]","cLFV muon #eta","cLFV muon #varphi","Bachelor lepton p_{T} [GeV]","Bachelor lepton #eta","Bachelor lepton #varphi","Standard top mass [GeV]","M(lll) [GeV]","p_{T}(lll) [GeV]","H_{t}(lll) [GeV]","M_{t}(lll) [GeV]","Leading jet p_{T} [GeV]","Leading jet #eta","Leading jet #varphi","Number of jets","Number of b-tagged jets","MET [GeV]","#varphi(MET)","Number of vertices", "M(ll) (OSSF) [GeV]", "p_{T}(ll) (OSSF) [GeV]", "Dr(ll) (OSSF)", "Dphi(ll) (OSSF)", "cLFV top mass [GeV]", "M(ll) (cLFV) [GeV]", "p_{T}(ll) (cLFV) [GeV]", "Dr(ll) (cLFV)", "Dphi(ll) (cLFV)", "H_{t} [GeV]", "M_{s} [GeV]", "Dr(Zl)", "Dphi(Zl)", "Dr(Je)", "Dr(Jmu)"]
sys = ["eleRecoSf", "eleIDSf", "muIdSf", "muIsoSf", "bcTagSF", "udsgTagSF","pu", "prefiring"]

# set up an argument parser
parser = argparse.ArgumentParser()

parser.add_argument('--v', dest='VERBOSE', default=True)
parser.add_argument('--l', dest = 'LOCATION', default= '/afs/cern.ch/user/a/asparker/public/LFVTopCode_MyFork/TopLFV/hists/')

ARGS = parser.parse_args()

verbose = ARGS.VERBOSE
HistAddress = ARGS.LOCATION

Samples = ['data.root','TTV.root','WZ.root', 'ZZ.root', 'TTbar.root', 'others.root', 'SMEFTfr_ST_vector_emutu.root', 'SMEFTfr_TT_vector_emutu.root']
SamplesName = ['data','TTV','WZ', 'ZZ', 'TTbar', 'others', 'ST_vector_emutu', 'TT_vector_emutu']
SamplesNameLatex = ['data', 'TTV', 'WZ', 'ZZ', 'TTbar', 'others', 'ST\_vector\_emutu', 'TT\_vector\_emutu']
NormalizationErr = [0, 0, 0, 0, 0, 0, 0, 0]

colors =  [ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kBlue-3,ROOT.kRed-4,ROOT.kOrange-3, ROOT.kOrange-6, ROOT.kCyan-6]

Hists = []
HistsSysUp = []
HistsSysDown = []
Hists_copy =[]
for numyear, nameyear in enumerate(year):
    l0=[]
    copyl0=[]
    SysUpl0=[]
    SysDownl0=[]
    Files = []
    for f in range(len(Samples)):
        l1=[]
        copyl1=[]
        SysUpl1=[]
        SysDownl1=[]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        for numch, namech in enumerate(channels):
            l2=[]
            copyl2=[]
            SysUpl2=[]
            SysDownl2=[]
            for numreg, namereg in enumerate(regions):
                l3=[]
                copyl3=[]
                SysUpl3=[]
                SysDownl3=[]
                for numvar, namevar in enumerate(variables):
                    SysUpl4=[]
                    SysDownl4=[]
                    h= Files[f].Get(namech + '_' + namereg + '_' + namevar)
                    h.SetFillColor(colors[f])
                    if 'SMEFTfr' not in Samples[f]:
                        h.SetLineColor(colors[0])
                    else:
                        h.SetLineColor(colors[f])
                    h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                    l3.append(h)
                    copyl3.append(h.Clone())
                    for numsys, namesys in enumerate(sys):
                        h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Up')
                        h.SetFillColor(colors[f])
                        h.SetLineColor(colors[f])
                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                        SysUpl4.append(h)
                        h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Down')
                        h.SetFillColor(colors[f])
                        h.SetLineColor(colors[f])
                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                        SysDownl4.append(h)
                    SysUpl3.append(SysUpl4)
                    SysDownl3.append(SysDownl4)
                l2.append(l3)
                copyl2.append(copyl3)
                SysUpl2.append(SysUpl3)
                SysDownl2.append(SysDownl3)
            l1.append(l2)
            copyl1.append(copyl2)
            SysUpl1.append(SysUpl2)
            SysDownl1.append(SysDownl2)
        l0.append(l1)
        copyl0.append(copyl1)
        SysUpl0.append(SysUpl1)
        SysDownl0.append(SysDownl1)
    Hists.append(l0)
    Hists_copy.append(copyl0)
    HistsSysUp.append(SysUpl0)       
    HistsSysDown.append(SysDownl0)


#pdfGraph=[]
#qscaleGraph=[]
#ISRGraph=[]
#FSRGraph=[]
#CRGraph=[]
#TuneGraph=[]
#hdampGraph=[]
#
#for numyear, nameyear in enumerate(year):
#    t1Pdf=[]
#    t1Qscale=[]
#    t1ISR=[]
#    t1FSR=[]
#    t1CR=[]
#    t1Tune=[]
#    t1hdamp=[]
#    sysfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTTo2L2Nu.root')
#    CR1file = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_CR1QCDbased.root')
#    erdfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_CRerdON.root')
#    TuneCP5upfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_TuneCP5up.root')
#    TuneCP5downfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_TuneCP5down.root')
#    hdampupfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_hdampUP.root')
#    hdampdownfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_hdampDOWN.root')
#    for numreg, namereg in enumerate(regions):
#        if numreg<2:
#            continue
#        t2Pdf=[]
#        t2Qscale=[]
#        t2ISR=[]
#        t2FSR=[]
#        t2CR=[]
#        t2Tune=[]
#        t2hdamp=[]
#        for numvar, namevar in enumerate(variables):
#            pdfHists=[]
#            QscaleHists=[]
#            for numsys in range(9):
#                h=sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_QscalePDF_'+str(numsys))
#                h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
#                QscaleHists.append(h)
##                del h
##                gc.collect()
#            for numsys in range(9,110):
#                h=sysfile.Get('reweightingSys/emu' +'_' + namereg + '_' + namevar+ '_QscalePDF_'+str(numsys))
#                h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
#                pdfHists.append(h)
##                del h
##                gc.collect()
#            hISRup = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_8')
#            hISRdown = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_6')
#            hFSRup = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_9')
#            hFSRdown = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_7')
#            hCR1 = CR1file.Get('emu' + '_' + namereg + '_' + namevar)
#            herd = erdfile.Get('emu' + '_' + namereg + '_' + namevar)
#            hTuneCP5up = TuneCP5upfile.Get('emu' + '_' + namereg + '_' + namevar)
#            hTuneCP5down = TuneCP5downfile.Get('emu' + '_' + namereg + '_' + namevar)
#            hhdampup = hdampupfile.Get('emu' + '_' + namereg + '_' + namevar)
#            hhdampdown = hdampdownfile.Get('emu' + '_' + namereg + '_' + namevar)
#            binwidth= array( 'd' )
#            bincenter= array( 'd' )
#            yvalue= array( 'd' )
#            yerrupQscale= array( 'd' )
#            yerrdownQscale= array( 'd' )
#            yerrupPDF= array( 'd' )
#            yerrdownPDF= array( 'd' )
#            yerrupISR = array( 'd' )
#            yerrdownISR = array( 'd' )
#            yerrupFSR = array( 'd' )
#            yerrdownFSR = array( 'd' )
#            yerrupCR = array( 'd' )
#            yerrdownCR = array( 'd' )
#            yerrupTune= array( 'd' )
#            yerrdownTune= array( 'd' )
#            yerruphdamp= array( 'd' )
#            yerrdownhdamp= array( 'd' )
#            for b in range(QscaleHists[0].GetNbinsX()):
#                QS=np.zeros(9)
#                PDF=0
#                binwidth.append(QscaleHists[0].GetBinWidth(b+1)/2)
#                bincenter.append(QscaleHists[0].GetBinCenter(b+1))
#                yvalue.append(0)
#                nomRatio = 1
##                if QscaleHists[0].GetBinContent(b+1) > 0:
##                    nomRatio = 100/QscaleHists[0].GetBinContent(b+1)
#                for numsys in range(9):
#                    if numsys==0 or numsys==5 or numsys==7:
#                        continue
#                    QS[numsys] = QscaleHists[numsys].GetBinContent(b+1) - QscaleHists[0].GetBinContent(b+1)
#                yerrupQscale.append((abs(max(QS)))*nomRatio)
#                yerrdownQscale.append((abs(min(QS)))*nomRatio)
#                for numsys in range(9,110):
#                    PDF = PDF + (pdfHists[numsys-9].GetBinContent(b+1) - QscaleHists[0].GetBinContent(b+1))**2
#                yerrupPDF.append((math.sqrt(PDF))*nomRatio)
#                yerrdownPDF.append((math.sqrt(PDF))*nomRatio)
#                yerrupISR.append((abs(max(hISRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hISRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
#                yerrdownISR.append((abs(min(hISRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hISRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
#                yerrupFSR.append((abs(max(hFSRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hFSRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
#                yerrdownFSR.append((abs(min(hFSRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hFSRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
#                yerrupCR.append((abs(max(herd.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hCR1.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
#                yerrdownCR.append((abs(min(herd.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hCR1.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
#                yerrupTune.append((abs(max(hTuneCP5up.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hTuneCP5down.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
#                yerrdownTune.append((abs(min(hTuneCP5up.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hTuneCP5down.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
#                yerruphdamp.append((abs(max(hhdampup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hhdampdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
#                yerrdownhdamp.append((abs(min(hhdampup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hhdampdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
##                del QS
##                del PDF
##                del nomRatio
##                gc.collect()
#            t2Qscale.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrupQscale,yerrdownQscale))
#            t2Pdf.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrupPDF,yerrdownPDF))
#            t2ISR.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrupISR,yerrdownISR))
#            t2FSR.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrupFSR,yerrdownFSR))
#            t2CR.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrupCR,yerrdownCR))
#            t2Tune.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrupTune,yerrdownTune))
#            t2hdamp.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerruphdamp,yerrdownhdamp))
#            del binwidth
#            del bincenter
#            del yvalue
#            del yerrupQscale
#            del yerrdownQscale
#            del yerrupPDF
#            del yerrdownPDF
#            del yerrupISR
#            del yerrdownISR
#            del yerrupFSR
#            del yerrdownFSR
#            del pdfHists
#            del QscaleHists
#            gc.collect()
#        t1Qscale.append(t2Qscale)
#        t1Pdf.append(t2Pdf)
#        t1ISR.append(t2ISR)
#        t1FSR.append(t2FSR)
#        t1CR.append(t2CR)
#        t1Tune.append(t2Tune)
#        t1hdamp.append(t2hdamp)
#    pdfGraph.append(t1Pdf)
#    qscaleGraph.append(t1Qscale)
#    ISRGraph.append(t1ISR)
#    FSRGraph.append(t1FSR)
#    CRGraph.append(t1CR)
#    TuneGraph.append(t1Tune)
#    hdampGraph.append(t1hdamp)
#    sysfile.Close()
#    CR1file.Close()
#    erdfile.Close()
#    TuneCP5upfile.Close()
#    TuneCP5downfile.Close()
#    hdampupfile.Close()
#    hdampdownfile.Close()
#    del sysfile
#    del CR1file
#    del erdfile
#    del TuneCP5upfile
#    del TuneCP5downfile
#    del hdampupfile
#    del hdampdownfile
#    gc.collect()
#
#Gttsys = []
#Gttsys.append(pdfGraph)
#Gttsys.append(qscaleGraph)
#Gttsys.append(ISRGraph)
#Gttsys.append(FSRGraph)
#Gttsys.append(CRGraph)
#Gttsys.append(TuneGraph)
#Gttsys.append(hdampGraph)
#ttSys = ['pdf','QS','ISR','FSR','CR','Tune','hdamp']

for numyear, nameyear in enumerate(year):
    for numreg, namereg in enumerate(regions):
        if numreg<2:
            continue
        for numvar, namevar in enumerate(variables):
            glistup = []
            glistdown = []
            for g in range(len(Gttsys)):
                hup = Hists[numyear][4][1][numreg][numvar].Clone()
                hdown = Hists[numyear][4][1][numreg][numvar].Clone()
                for b in range(hup.GetNbinsX()):
                    rb = 0
                    if hup.GetBinContent(b+1)>0:
                        rb = 100/hup.GetBinContent(b+1)
                    hup.SetBinContent(b+1, 0 + Gttsys[g][numyear][numreg-2][numvar].GetErrorYhigh(b)*rb)
                    hdown.SetBinContent(b+1,0 - Gttsys[g][numyear][numreg-2][numvar].GetErrorYlow(b)*rb)
                glistup.append(hup)
                glistdown.append(hdown)
#            compareError(glistup,glistdown, ttSys, 'emul', namereg, nameyear,namevar,variablesName[numvar])
#            del glist
#            gc.collect()



tgraph_nominal = []
tgraph_ratio = []
errup = 0
errdown =0
for numyear, nameyear in enumerate(year):
    t1nominal = []
    t1ratio = []
    for numch, namech in enumerate(channels): 
        t2nominal = []
        t2ratio = []
        for numreg, namereg in enumerate(regions):
            t3nominal = []
            t3ratio = []
            for numvar, namevar in enumerate(variables):
                for f in range(1,len(Samples)-3):
                    Hists_copy[numyear][f+1][numch][numreg][numvar].Add(Hists_copy[numyear][f][numch][numreg][numvar])
                for numsys, namesys in enumerate(sys):
                    for f in range(1,len(Samples)-3):
                        HistsSysUp[numyear][f+1][numch][numreg][numvar][numsys].Add(HistsSysUp[numyear][f][numch][numreg][numvar][numsys]) 
                        HistsSysDown[numyear][f+1][numch][numreg][numvar][numsys].Add(HistsSysDown[numyear][f][numch][numreg][numvar][numsys])
                binwidth= array( 'd' )
                bincenter= array( 'd' )
                yvalue= array( 'd' )
                yerrup= array( 'd' )
                yerrdown= array( 'd' )
                yvalueRatio= array( 'd' )
                yerrupRatio= array( 'd' )
                yerrdownRatio= array( 'd' )
                content=0
                for b in range(Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetNbinsX()):
                    errup = 0
                    errdown =0
                    binwidth.append(Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinWidth(b+1)/2)
                    bincenter.append(Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinCenter(b+1))
                    if Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1)>0:
                        content = Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1)
                    else:
                        content =0.0000001
                    yvalue.append(content)
                    yvalueRatio.append(content/content)
                    for numsys2, namesys2 in enumerate(sys):
                        if HistsSysUp[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].Integral()==0 or Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1)<=0:
                            continue
                        if HistsSysUp[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1)  > 0:
                            errup = errup + (HistsSysUp[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
                        else:
                            errdown = errdown + (HistsSysUp[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
                        if HistsSysDown[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1)  > 0:
                            errup = errup + (HistsSysDown[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
                        else:
                            errdown = errdown + (HistsSysDown[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
                    errup = errup + Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinError(b+1)**2
                    errdown = errdown + Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinError(b+1)**2
#Add lumi error
                    errup = errup + (LumiErr[numyear]*Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
                    errdown = errdown + (LumiErr[numyear]*Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
#add normalization error only for ttbar reegions 
                    if (numch>1):
                        for f in range(len(Samples)):
                            errup = errup + (NormalizationErr[f]*Hists[numyear][f][numch][numreg][numvar].GetBinContent(b+1))**2                    
                            errdown = errdown + (NormalizationErr[f]*Hists[numyear][f][numch][numreg][numvar].GetBinContent(b+1))**2
#add ttbar theory errors
#                    if numch==1 and numreg>1:
#                        errup = errup + (pdfGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errup = errup + (qscaleGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errup = errup + (ISRGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errup = errup + (FSRGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errup = errup + (CRGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errup = errup + (TuneGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errup = errup + (hdampGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errdown = errdown + (pdfGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        errdown = errdown + (qscaleGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        errdown = errdown + (ISRGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        errdown = errdown + (FSRGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        errdown = errdown + (CRGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        errdown = errdown + (TuneGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        errdown = errdown + (hdampGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        print str(pdfGraph[numyear][numreg-1][numvar].GetErrorYlow(b)) + '    '+str(pdfGraph[numyear][numreg-1][numvar].GetErrorYlow(b))
                    yerrup.append(math.sqrt(errup))
                    yerrdown.append(math.sqrt(errdown))
                    yerrupRatio.append(math.sqrt(errup)/content)
                    yerrdownRatio.append(math.sqrt(errdown)/content)
                t3nominal.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrup,yerrdown))
                t3ratio.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalueRatio,binwidth,binwidth,yerrupRatio,yerrdownRatio))
            t2nominal.append(t3nominal)
            t2ratio.append(t3ratio)
        t1nominal.append(t2nominal)
        t1ratio.append(t2ratio)
    tgraph_nominal.append(t1nominal)
    tgraph_ratio.append(t1ratio)


for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                HH=[]
                HHsignal=[]
                for f in range(len(Samples)):
                    if 'SMEFTfr' in Samples[f]:
                        HHsignal.append(Hists[numyear][f][numch][numreg][numvar])
                    else:
                        HH.append(Hists[numyear][f][numch][numreg][numvar])
                stackPlotsError(HH, HHsignal,tgraph_nominal[numyear][numch][numreg][numvar], tgraph_ratio[numyear][numch][numreg][numvar],SamplesName, namech, namereg, nameyear,namevar,variablesName[numvar])

#                stackPlots(HH, HHsignal, SamplesName, namech, namereg, nameyear,namevar,variablesName[numvar])

#le = '\\documentclass{article}' + "\n"
#le += '\\usepackage{rotating}' + "\n"
#le += '\\usepackage{rotating}' + "\n"
#le += '\\begin{document}' + "\n"
#
#print le
#for numyear, nameyear in enumerate(year):
#    for numch, namech in enumerate(channels):
#        cutFlowTable(Hists, SamplesNameLatex, regions, numch, numyear, nameyear + ' ' + namech, 6 )
#print '\\end{document}' + "\n"


