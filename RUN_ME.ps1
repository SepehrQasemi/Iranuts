param(
    [switch]$SetupOnly,
    [switch]$NoBrowser,
    [string]$ServerHost = "127.0.0.1",
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Write-Step($message) {
    Write-Host "[RUN_ME] $message" -ForegroundColor Cyan
}

function Fail($message) {
    Write-Error "[RUN_ME] $message"
    exit 1
}

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

if (-not (Test-Path (Join-Path $repoRoot "manage.py"))) {
    Fail "manage.py was not found. Run this script from the repository root."
}

$pythonCommand = $null
foreach ($candidate in @("python", "py")) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        $pythonCommand = $candidate
        break
    }
}

if (-not $pythonCommand) {
    Fail "Python was not found in PATH. Install Python 3.11+ and try again."
}

$venvDir = Join-Path $repoRoot ".venv"
$venvPython = Join-Path $venvDir "Scripts\\python.exe"
$requirementsMarker = Join-Path $venvDir ".requirements-installed"
$requirementsFile = Join-Path $repoRoot "requirements.txt"
$envExample = Join-Path $repoRoot ".env.example"
$envFile = Join-Path $repoRoot ".env"

if (-not (Test-Path $venvPython)) {
    Write-Step "Creating virtual environment in .venv"
    & $pythonCommand -m venv $venvDir
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $venvPython)) {
        Fail "Failed to create the virtual environment."
    }
}
else {
    Write-Step "Reusing existing virtual environment"
}

$requirementsNeedInstall = -not (Test-Path $requirementsMarker)
if (-not $requirementsNeedInstall) {
    $requirementsNeedInstall = (Get-Item $requirementsFile).LastWriteTimeUtc -gt (Get-Item $requirementsMarker).LastWriteTimeUtc
}

if ($requirementsNeedInstall) {
    Write-Step "Installing requirements"
    & $venvPython -m pip install -r $requirementsFile
    if ($LASTEXITCODE -ne 0) {
        Fail "Dependency installation failed."
    }
    Set-Content -Path $requirementsMarker -Value (Get-Date).ToString("o")
}
else {
    Write-Step "Requirements already up to date"
}

if (-not (Test-Path $envFile)) {
    if (-not (Test-Path $envExample)) {
        Fail ".env is missing and .env.example was not found."
    }

    Write-Step "Creating .env from .env.example"
    Copy-Item $envExample $envFile
}
else {
    Write-Step "Using existing .env file"
}

Write-Step "Applying migrations"
& $venvPython manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Fail "Database migrations failed."
}

if ($SetupOnly) {
    Write-Step "Setup completed. Run this script again without -SetupOnly to start the server."
    exit 0
}

$serverUrl = "http://{0}:{1}/" -f $ServerHost, $Port
if (-not $NoBrowser) {
    Write-Step "Opening $serverUrl"
    Start-Process $serverUrl | Out-Null
}

Write-Step "Starting Django development server at $serverUrl"
& $venvPython manage.py runserver "$ServerHost`:$Port"
