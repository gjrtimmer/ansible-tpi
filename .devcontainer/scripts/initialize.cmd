@echo off
setlocal

:: Get the user's home directory
set "HOME_DIR=%HOMEDRIVE%%HOMEPATH%"

:: Set the target directory
set "SSH_TARGET_DIR=%HOME_DIR%\.ssh\tpi"

:: Check if the directory exists
if not exist "%SSH_TARGET_DIR%" (
    :: Create the directory
    mkdir "%SSH_TARGET_DIR%"
    echo Directory "%SSH_TARGET_DIR%" created.
) else (
    echo Directory "%SSH_TARGET_DIR%" already exists.
)

:: Set target data directory
set "DATA_TARGET_DIR=%HOME_DIR%\.tpi"

:: Check if the directory exists
if not exist "%DATA_TARGET_DIR%" (
    :: Create the directory
    mkdir "%DATA_TARGET_DIR%"
    echo Directory "%DATA_TARGET_DIR%" created.
) else (
    echo Directory "%DATA_TARGET_DIR%" already exists.
)

:: Set the target file
set "VAULT_PASS_FILE=%HOME_DIR%\.ansible_vault_pass"

:: Check if the file exists
if not exist "%VAULT_PASS_FILE%" (
    :: Create the file
    echo. > "%VAULT_PASS_FILE%"
    echo File "%VAULT_PASS_FILE%" created.
) else (
    echo File "%VAULT_PASS_FILE%" already exists.
)

set "KUBE_TARGET_DIR=%HOME_DIR%\.kube"

:: Check if the directory exists
if not exist "%KUBE_TARGET_DIR%" (
    :: Create the directory
    mkdir "%KUBE_TARGET_DIR%"
    echo Directory "%KUBE_TARGET_DIR%" created.
) else (
    echo Directory "%KUBE_TARGET_DIR%" already exists.
)

endlocal
