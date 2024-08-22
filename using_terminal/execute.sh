If (!(Test-Path -Path $PROFILE )) {
    New-Item -Type File -Path $PROFILE -Force
}