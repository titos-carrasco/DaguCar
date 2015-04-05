##
## Auto Generated makefile by CodeLite IDE
## any manual changes will be erased      
##
## Release
ProjectName            :=DaguCar
ConfigurationName      :=Release
WorkspacePath          := "/home/roberto/Projects/GitHub/DaguCar/Cpp"
ProjectPath            := "/home/roberto/Projects/GitHub/DaguCar/Cpp"
IntermediateDirectory  :=./Release
OutDir                 := $(IntermediateDirectory)
CurrentFileName        :=
CurrentFilePath        :=
CurrentFileFullPath    :=
User                   :=Roberto
Date                   :=04/04/15
CodeLitePath           :="/home/roberto/.codelite"
LinkerName             :=/usr/bin/g++ 
SharedObjectLinkerName :=/usr/bin/g++ -shared -fPIC
ObjectSuffix           :=.o
DependSuffix           :=.o.d
PreprocessSuffix       :=.i
DebugSwitch            :=-g 
IncludeSwitch          :=-I
LibrarySwitch          :=-l
OutputSwitch           :=-o 
LibraryPathSwitch      :=-L
PreprocessorSwitch     :=-D
SourceSwitch           :=-c 
OutputFile             :=$(IntermediateDirectory)/$(ProjectName)
Preprocessors          :=$(PreprocessorSwitch)NDEBUG 
ObjectSwitch           :=-o 
ArchiveOutputSwitch    := 
PreprocessOnlySwitch   :=-E
ObjectsFileList        :="DaguCar.txt"
PCHCompileFlags        :=
MakeDirCommand         :=mkdir -p
LinkOptions            :=  
IncludePath            :=  $(IncludeSwitch). $(IncludeSwitch). 
IncludePCH             := 
RcIncludePath          := 
Libs                   := 
ArLibs                 :=  
LibPath                := $(LibraryPathSwitch). 

##
## Common variables
## AR, CXX, CC, AS, CXXFLAGS and CFLAGS can be overriden using an environment variables
##
AR       := /usr/bin/ar rcu
CXX      := /usr/bin/g++ 
CC       := /usr/bin/gcc 
CXXFLAGS :=  -O2 -std=c++11 -Wall $(Preprocessors)
CFLAGS   :=  -O2 -Wall $(Preprocessors)
ASFLAGS  := 
AS       := /usr/bin/as 


##
## User defined environment variables
##
CodeLiteDir:=/usr/share/codelite
Objects0=$(IntermediateDirectory)/src_DaguCar.cpp$(ObjectSuffix) $(IntermediateDirectory)/src_TestDaguCar.cpp$(ObjectSuffix) $(IntermediateDirectory)/src_SerialPort.cpp$(ObjectSuffix) 



Objects=$(Objects0) 

##
## Main Build Targets 
##
.PHONY: all clean PreBuild PrePreBuild PostBuild
all: $(OutputFile)

$(OutputFile): $(IntermediateDirectory)/.d $(Objects) 
	@$(MakeDirCommand) $(@D)
	@echo "" > $(IntermediateDirectory)/.d
	@echo $(Objects0)  > $(ObjectsFileList)
	$(LinkerName) $(OutputSwitch)$(OutputFile) @$(ObjectsFileList) $(LibPath) $(Libs) $(LinkOptions)

$(IntermediateDirectory)/.d:
	@test -d ./Release || $(MakeDirCommand) ./Release

PreBuild:


##
## Objects
##
$(IntermediateDirectory)/src_DaguCar.cpp$(ObjectSuffix): src/DaguCar.cpp $(IntermediateDirectory)/src_DaguCar.cpp$(DependSuffix)
	$(CXX) $(IncludePCH) $(SourceSwitch) "/home/roberto/Projects/GitHub/DaguCar/Cpp/src/DaguCar.cpp" $(CXXFLAGS) $(ObjectSwitch)$(IntermediateDirectory)/src_DaguCar.cpp$(ObjectSuffix) $(IncludePath)
$(IntermediateDirectory)/src_DaguCar.cpp$(DependSuffix): src/DaguCar.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) -MG -MP -MT$(IntermediateDirectory)/src_DaguCar.cpp$(ObjectSuffix) -MF$(IntermediateDirectory)/src_DaguCar.cpp$(DependSuffix) -MM "src/DaguCar.cpp"

$(IntermediateDirectory)/src_DaguCar.cpp$(PreprocessSuffix): src/DaguCar.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) $(PreprocessOnlySwitch) $(OutputSwitch) $(IntermediateDirectory)/src_DaguCar.cpp$(PreprocessSuffix) "src/DaguCar.cpp"

$(IntermediateDirectory)/src_TestDaguCar.cpp$(ObjectSuffix): src/TestDaguCar.cpp $(IntermediateDirectory)/src_TestDaguCar.cpp$(DependSuffix)
	$(CXX) $(IncludePCH) $(SourceSwitch) "/home/roberto/Projects/GitHub/DaguCar/Cpp/src/TestDaguCar.cpp" $(CXXFLAGS) $(ObjectSwitch)$(IntermediateDirectory)/src_TestDaguCar.cpp$(ObjectSuffix) $(IncludePath)
$(IntermediateDirectory)/src_TestDaguCar.cpp$(DependSuffix): src/TestDaguCar.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) -MG -MP -MT$(IntermediateDirectory)/src_TestDaguCar.cpp$(ObjectSuffix) -MF$(IntermediateDirectory)/src_TestDaguCar.cpp$(DependSuffix) -MM "src/TestDaguCar.cpp"

$(IntermediateDirectory)/src_TestDaguCar.cpp$(PreprocessSuffix): src/TestDaguCar.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) $(PreprocessOnlySwitch) $(OutputSwitch) $(IntermediateDirectory)/src_TestDaguCar.cpp$(PreprocessSuffix) "src/TestDaguCar.cpp"

$(IntermediateDirectory)/src_SerialPort.cpp$(ObjectSuffix): src/SerialPort.cpp $(IntermediateDirectory)/src_SerialPort.cpp$(DependSuffix)
	$(CXX) $(IncludePCH) $(SourceSwitch) "/home/roberto/Projects/GitHub/DaguCar/Cpp/src/SerialPort.cpp" $(CXXFLAGS) $(ObjectSwitch)$(IntermediateDirectory)/src_SerialPort.cpp$(ObjectSuffix) $(IncludePath)
$(IntermediateDirectory)/src_SerialPort.cpp$(DependSuffix): src/SerialPort.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) -MG -MP -MT$(IntermediateDirectory)/src_SerialPort.cpp$(ObjectSuffix) -MF$(IntermediateDirectory)/src_SerialPort.cpp$(DependSuffix) -MM "src/SerialPort.cpp"

$(IntermediateDirectory)/src_SerialPort.cpp$(PreprocessSuffix): src/SerialPort.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) $(PreprocessOnlySwitch) $(OutputSwitch) $(IntermediateDirectory)/src_SerialPort.cpp$(PreprocessSuffix) "src/SerialPort.cpp"


-include $(IntermediateDirectory)/*$(DependSuffix)
##
## Clean
##
clean:
	$(RM) ./Release/*$(ObjectSuffix)
	$(RM) ./Release/*$(DependSuffix)
	$(RM) $(OutputFile)
	$(RM) ".build-release/DaguCar"


