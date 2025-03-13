@echo off
setlocal enabledelayedexpansion
set JAVA_8_HOME=D:\etc\java\jdk1.8.0_202
set JAVA_17_HOME=D:\etc\java\jdk-17.0.8

:: 参数解析初始化
set jvm_version=8
set args=
set arg_count=0

:: 循环解析所有参数
:loop
if "%1"=="" goto end_loop

:: 处理 -v 参数
if "%1"=="-v" (
    if "%2"=="8" set jvm_version=8
    if "%2"=="17" set jvm_version=17
    shift
    goto continue
)

:: 记录其他参数
set args=!args! %1
set /a arg_count+=1

:continue
shift
goto loop

:end_loop

:: 设置JDK路径
if "%jvm_version%"=="8" (
    set JAVA_HOME=%JAVA_8_HOME%
) else (
    set JAVA_HOME=%JAVA_17_HOME%
)

:: 应用环境变量
set PATH=%JAVA_HOME%\bin;%PATH%
echo [INFO] 共收到%arg_count%个参数
echo [INFO] 剩余参数: %args%

mvn %args%
endlocal