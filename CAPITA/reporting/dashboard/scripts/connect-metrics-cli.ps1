param (
  [Parameter(Mandatory=$true, ParameterSetName="ScriptExecution")][String]
  $Client,
  [Parameter(Mandatory=$true, ParameterSetName="ScriptExecution")][String]
  $Environment,
  [Parameter(Mandatory=$true, ParameterSetName="ScriptExecution")][String]
  $ProfileName,
  [Parameter(Mandatory=$true, ParameterSetName="ScriptExecution")][String]
  $PowerBIUrl,
  [Parameter(ParameterSetName="Version")][Switch]
  $Version
)

$ErrorActionPreference = "Stop"

$outputPath = "$PSScriptRoot/../output"

function Write-Log() {
  Param (
    [String]
    $Message
  )

  $timestamp = Get-Date -UFormat "%Y-%m-%d %T"

  Write-Host "$timestamp - INFO - $message"
}

function New-PipEnvShell() {
  pipenv shell --three
}

function Invoke-ConnectMetrics() {
  Param(
    [String]
    $ProfileName,
    [String]
    $Client,
    [String]
    $Environment
  )

  Write-Log "Executing the connectmetrics script..."
  Write-Log "**************************************"
  $process = Start-Process  -FilePath "python" `
                            -ArgumentList "$PSScriptRoot/../src/connectmetrics/code/connectmetrics.py --profile $ProfileName --client $Client --environment $Environment" `
                            -NoNewWindow `
                            -Wait `
                            -PassThru

  if ($process.ExitCode -ne 0) {
    throw "Failed to retrieve Amazon Connect metrics for $Configuration"
  }
  Write-Log "**************************************"
  Write-Log "connectmetrics execution succeded"

  $metrics = Read-Metrics -Client $Client -Environment $Environment
  return $metrics
}

function Test-Python3Installed() {
  $python = & python -V 2>&1
  if ($python -match "Python\s3.*") {
    return
  }

  throw "The connectmetrics script requires Python 3 to be installed. Please download and install from https://www.python.org/downloads/windows/"
}

function Confirm-VirtualenvExists() {
  Test-Python3Installed

  $venvPath = "$PSScriptRoot/venv"

  if (-Not(Test-Path -Path $venvPath)) {
    Write-Log "Creating virtual environment"
    python -m venv $venvPath
    Write-Log "Activating virtual environment..."
    & "$venvPath/Scripts/Activate.ps1"
  }
  Write-Log "Installing dependencies..."
  pip install -r "$PSScriptRoot/../requirements.txt"
}

function Read-Metrics() {
    Param(
      [String]
      $Client,
      [String]
      $Environment
    )
    Write-Log "Reading the metrics data file"
    $metrics = Get-Content "$OutputPath/$Client-$Environment-metric-data.json" | ConvertFrom-Json
    return $metrics
}

function Test-OutputDirectory() {
  Param(
    [String]
    $OutputPath
  )

  if (-Not(Test-Path -Path $OutputPath)) {
    Write-Log "Creating output directory $OutputPath"
    New-Item -ItemType Directory -Path $OutputPath | Out-Null
  }
}

function Invoke-PowerBI() {
  param (
    [PSObject]
    $Metric
  )
  $payload = ConvertTo-Json $metric
  Invoke-WebRequest -Method Post -Uri $PowerBIUrl -Body $payload -UseDefaultCredentials | Out-Null
}

function Send-MetricsToPowerBI() {
   Param (
    [PSObject]
    $Metrics
  )
  Write-Log "Sending metrics to PowerBI"
  foreach ($metric in $Metrics) {
      Invoke-PowerBI -Metric $metric
  }
  Write-Log "Successfully sent metrics"
}

function Read-Version() {
  $process = Start-Process  -FilePath "python" `
                            -ArgumentList "$PSScriptRoot/../src/connectmetrics/code/connectmetrics.py --version" `
                            -NoNewWindow `
                            -Wait `
                            -PassThru
}

if ($Version) {
  Read-Version
  Exit
}

Confirm-VirtualenvExists
Test-OutputDirectory -OutputPath $outputPath
$metrics = Invoke-ConnectMetrics -Client $Client -ProfileName $ProfileName -Environment $Environment
Send-MetricsToPowerBI -Metrics $metrics



