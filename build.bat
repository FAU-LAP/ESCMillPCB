@ECHO OFF

REM Build script for ESCMillPCB including HTML documentation.
REM When using Anaconda, run this script from Anaconda prompt!

pushd %~dp0
call makedocs html
pyinstaller --distpath="_dist" --workpath="_build" --clean ESCMillPCB.spec
xcopy /Y /E /I /Q _platforms _dist\platforms
REM xcopy /Y /E /I /Q resources _dist\resources
xcopy /Y /E /I /Q _docs _dist\_docs
REM clear icon cache to check if icon is set correctly
ie4uinit -show
popd