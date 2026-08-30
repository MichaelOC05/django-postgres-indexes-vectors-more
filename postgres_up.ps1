$SecurePassword = Read-Host -Prompt "Enter password" -AsSecureString
$env:PASSWORD = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecurePassword)
)

docker compose -f postgres.yaml up -d