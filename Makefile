ROOTCFLAGS     = $(shell root-config --cflags)
ROOTLIBS       = $(shell root-config --libs)
ROOTGLIBS      = $(shell root-config --glibs) 

INCLUDES       = -I./include 

CXX            = g++
CXXFLAGS       = -fPIC -fno-var-tracking -Wno-deprecated -D_GNU_SOURCE -O2  $(INCLUDES) 
CXXFLAGS      += $(ROOTCFLAGS)

LD             = g++
LDFLAGS        = 

SOFLAGS        = -O -shared  -fPIC #-flat_namespace 
LIBS           = $(ROOTLIBS) 

GLIBS         = $(ROOTGLIBS) -lMinuit -lTreePlayer -lTMVA

SRCS = src/BTagCalibrationStandalone.cc src/RoccoR.cc src/lepton_candidate.cc src/jet_candidate.cc src/PU_reWeighting.cc src/MyAnalysis.cc 
OBJS =  $(patsubst %.C,%.o,$(SRCS:.cc=.o))

LIB=lib/main.so


.SUFFIXES: .cc,.C,.hh,.h

# Rules ====================================
all: $(LIB)  RunAll

lib : $(LIB)
$(LIB): $(OBJS)
	@echo "Creating library $(LIB)"
	mkdir -p lib
	$(LD) $(LDFLAGS) $(GLIBS) $(SOFLAGS) $(OBJS) -o $(LIB)
	@echo "$(LIB) successfully compiled!"

RunAll : src/main.cc $(LIB)	
	mkdir -p bin
	$(CXX) $(CXXFLAGS) -ldl $(LDFLAGS) -o $@ $^ $(GLIBS)

clean:
	$(RM) $(OBJS)	
	$(RM) $(LIB)
	$(RM) RunAll

purge:
	$(RM) $(OBJS)

deps: $(SRCS)
	makedepend $(INCLUDES) $^

# DO NOT DELETE THIS LINE -- make depend needs it
