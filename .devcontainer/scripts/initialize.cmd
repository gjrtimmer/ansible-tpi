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

endlocal
