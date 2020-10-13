#include "MyAnalysis.h"
#include "TSystem.h"
#include <iostream>

using namespace std;

void loop(TString param, TChain *tree, int nfiles=9999999)
{
    param += "/";
    const char *ext = ".root";
    const char *type = param.Data();
    const char *inDir = "root://cms-xrd-global.cern.ch/"; // Directory for the folder in Lxplus
    inDir = gSystem->ConcatFileName(inDir, type);
    char *dir = gSystem->ExpandPathName(inDir);
    void *dirp = gSystem->OpenDirectory(dir);

    const char *entry;
    const char *filename;
    TString str;
    int count = 0;

    while ((entry = (char *)gSystem->GetDirEntry(dirp)))
    {
        count++;
        cout<<count<<endl;
        str = entry;
        if (str.EndsWith(ext))
        {
            filename = gSystem->ConcatFileName(dir, entry);
            cout << filename << endl;
            tree->Add(filename);
        }
        if (count > nfiles)
            break;
    }
}

int main()
{
    TChain *ch1 = new TChain("IIHEAnalysis");
    // ch ->Add("/Users/jingyanli/eclipse-workspace/ROOT/outfile_2017_TT_vector_emutc.root");
    // ch->Add("/eos/user/a/asparker/TopLFV/2017_TTTo2L2Nu/outfile_1.root");
    // ch ->Add("/eos/cms/store/user/skinnari/TopLFV/outfile_2017_ST_vector_emutu/outfile_2718.root");
    // ch->Add("/eos/cms/store/user/asparker/TopLFV/2017_SMEFTfr_TT_vector_emutu/outfile_1577.root");
    // loop("eos/user/a/asparker/TopLFV/2017_TTTo2L2Nu", ch);
    loop("/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2017/IIHE_Ntuple/ntuple_SMEFTfr_TT_vector_emutc/", ch1, 15);
    MyAnalysis t1(ch1);
    // t1.Loop("test.root", "mc", "", "2017", "", 87.31, 41.53, 8926992);
    t1.Loop("2017_SMEFTfr_TT_vector_emutc.root", "mc", "", "2017", "", 0.032, 41.53, 500000);
    cout<<"Loop ends"<<endl;
/*
    TChain *ch2 = new TChain("IIHEAnalysis");
    loop("/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2017/IIHE_Ntuple/ntuple_SMEFTfr_TT_vector_emutu/", ch2, 15);
    MyAnalysis t2(ch2);
    t2.Loop("2017_SMEFTfr_TT_vector_emutu.root", "mc", "", "2017", "", 0.032, 41.53, 498000);

    TChain *ch4 = new TChain("IIHEAnalysis");
    loop("/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2017/IIHE_Ntuple/ntuple_SMEFTfr_ST_vector_emutu/", ch4, 15);
    MyAnalysis t4(ch4);
    t4.Loop("2017_SMEFTfr_ST_vector_emutu.root", "mc", "", "2017", "", 0.515, 41.53, 494000);

    TChain *ch5 = new TChain("IIHEAnalysis");
    loop("/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2017/IIHE_Ntuple/ntuple_SMEFTfr_ST_vector_emutc/", ch5, 15);
    MyAnalysis t5(ch5);
    t5.Loop("2017_SMEFTfr_ST_vector_emutc.root", "mc", "", "2017", "", 0.0512, 41.53, 500000);

    TChain *ch3 = new TChain("IIHEAnalysis");
    loop("/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_TTTo2L2Nu_v14_v1/191201_124029/0000/", ch3, 30);
    MyAnalysis t3(ch3);
    t3.Loop("2017_TTbar.root", "mc", "", "2017", "", 87.31, 41.53, 8926992);

    TChain *ch6 = new TChain("IIHEAnalysis");
    loop("/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_TTWJetsToLNu_v14_v1/191201_125315/0000/", ch6, 5);
    MyAnalysis t6(ch6);
    t6.Loop("2017_TTWJetsToLNu.root", "mc", "", "2017", "", 0.2043, 41.53, 2678775);

    TChain *ch7 = new TChain("IIHEAnalysis");
    loop("/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_WZTo3LNu/191201_124341/0000/", ch7, 3);
    MyAnalysis t7(ch7);
    t7.Loop("2017_WZTo3LNu.root", "mc", "", "2017", "", 4.43, 41.53, 6887413);
*/
    return 0;
}
