@echo off
title Starting GST Reconciler
cd /d "%~dp0"

:: Automatically remove Windows Internet Download Block (Zone.Identifier)
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-ChildItem -Path '%~dp0' -Recurse -Include *.exe,*.dll | Unblock-File -ErrorAction SilentlyContinue"

:: Launch GST Reconciler cleanly
start "" "%~dp0GSTReconciler.exe"
