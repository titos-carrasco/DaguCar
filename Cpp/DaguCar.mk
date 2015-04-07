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
Date                   :=04/06/15
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
CXXFLAGS :=  -O2 -Wall $(Preprocessors)
CFLAGS   :=  -O2 -Wall $(Preprocessors)
ASFLAGS  := 
AS       := /usr/bin/as 


##
## User defined environment variables
##
CodeLiteDir:=/usr/share/codelite
Objects0=$(IntermediateDirectory)/src_TestDaguCar.cpp$(ObjectSuffix) $(IntermediateDirectory)/utils_SerialPort.cpp$(ObjectSuffix) $(IntermediateDirectory)/utils_Lock.cpp$(ObjectSuffix) $(IntermediateDirectory)/robots_DaguCar.cpp$(ObjectSuffix) 



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
$(IntermediateDirectory)/src_TestDaguCar.cpp$(ObjectSuffix): src/TestDaguCar.cpp $(IntermediateDirectory)/src_TestDaguCar.cpp$(DependSuffix)
	$(CXX) $(IncludePCH) $(SourceSwitch) "/home/roberto/Projects/GitHub/DaguCar/Cpp/src/TestDaguCar.cpp" $(CXXFLAGS) $(ObjectSwitch)$(IntermediateDirectory)/src_TestDaguCar.cpp$(ObjectSuffix) $(IncludePath)
$(IntermediateDirectory)/src_TestDaguCar.cpp$(DependSuffix): src/TestDaguCar.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) -MG -MP -MT$(IntermediateDirectory)/src_TestDaguCar.cpp$(ObjectSuffix) -MF$(IntermediateDirectory)/src_TestDaguCar.cpp$(DependSuffix) -MM "src/TestDaguCar.cpp"

$(IntermediateDirectory)/src_TestDaguCar.cpp$(PreprocessSuffix): src/TestDaguCar.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) $(PreprocessOnlySwitch) $(OutputSwitch) $(IntermediateDirectory)/src_TestDaguCar.cpp$(PreprocessSuffix) "src/TestDaguCar.cpp"

$(IntermediateDirectory)/utils_SerialPort.cpp$(ObjectSuffix): src/utils/SerialPort.cpp $(IntermediateDirectory)/utils_SerialPort.cpp$(DependSuffix)
	$(CXX) $(IncludePCH) $(SourceSwitch) "/home/roberto/Projects/GitHub/DaguCar/Cpp/src/utils/SerialPort.cpp" $(CXXFLAGS) $(ObjectSwitch)$(IntermediateDirectory)/utils_SerialPort.cpp$(ObjectSuffix) $(IncludePath)
$(IntermediateDirectory)/utils_SerialPort.cpp$(DependSuffix): src/utils/SerialPort.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) -MG -MP -MT$(IntermediateDirectory)/utils_SerialPort.cpp$(ObjectSuffix) -MF$(IntermediateDirectory)/utils_SerialPort.cpp$(DependSuffix) -MM "src/utils/SerialPort.cpp"

$(IntermediateDirectory)/utils_SerialPort.cpp$(PreprocessSuffix): src/utils/SerialPort.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) $(PreprocessOnlySwitch) $(OutputSwitch) $(IntermediateDirectory)/utils_SerialPort.cpp$(PreprocessSuffix) "src/utils/SerialPort.cpp"

$(IntermediateDirectory)/utils_Lock.cpp$(ObjectSuffix): src/utils/Lock.cpp $(IntermediateDirectory)/utils_Lock.cpp$(DependSuffix)
	$(CXX) $(IncludePCH) $(SourceSwitch) "/home/roberto/Projects/GitHub/DaguCar/Cpp/src/utils/Lock.cpp" $(CXXFLAGS) $(ObjectSwitch)$(IntermediateDirectory)/utils_Lock.cpp$(ObjectSuffix) $(IncludePath)
$(IntermediateDirectory)/utils_Lock.cpp$(DependSuffix): src/utils/Lock.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) -MG -MP -MT$(IntermediateDirectory)/utils_Lock.cpp$(ObjectSuffix) -MF$(IntermediateDirectory)/utils_Lock.cpp$(DependSuffix) -MM "src/utils/Lock.cpp"

$(IntermediateDirectory)/utils_Lock.cpp$(PreprocessSuffix): src/utils/Lock.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) $(PreprocessOnlySwitch) $(OutputSwitch) $(IntermediateDirectory)/utils_Lock.cpp$(PreprocessSuffix) "src/utils/Lock.cpp"

$(IntermediateDirectory)/robots_DaguCar.cpp$(ObjectSuffix): src/robots/DaguCar.cpp $(IntermediateDirectory)/robots_DaguCar.cpp$(DependSuffix)
	$(CXX) $(IncludePCH) $(SourceSwitch) "/home/roberto/Projects/GitHub/DaguCar/Cpp/src/robots/DaguCar.cpp" $(CXXFLAGS) $(ObjectSwitch)$(IntermediateDirectory)/robots_DaguCar.cpp$(ObjectSuffix) $(IncludePath)
$(IntermediateDirectory)/robots_DaguCar.cpp$(DependSuffix): src/robots/DaguCar.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) -MG -MP -MT$(IntermediateDirectory)/robots_DaguCar.cpp$(ObjectSuffix) -MF$(IntermediateDirectory)/robots_DaguCar.cpp$(DependSuffix) -MM "src/robots/DaguCar.cpp"

$(IntermediateDirectory)/robots_DaguCar.cpp$(PreprocessSuffix): src/robots/DaguCar.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) $(PreprocessOnlySwitch) $(OutputSwitch) $(IntermediateDirectory)/robots_DaguCar.cpp$(PreprocessSuffix) "src/robots/DaguCar.cpp"


-include $(IntermediateDirectory)/*$(DependSuffix)
##
## Clean
##
clean:
	$(RM) ./Release/*$(ObjectSuffix)
	$(RM) ./Release/*$(DependSuffix)
	$(RM) $(OutputFile)
	$(RM) ".build-release/DaguCar"


