param(
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroup,
    [Parameter(Mandatory = $true)]
    [string]$WebAppName,
    [string]$Location = 'westeurope'
)

if (-not (Get-Module -ListAvailable -Name Az.Accounts)) {
    Write-Error "Az PowerShell modules are required. Install-Module Az -Scope CurrentUser"
    exit 1
}

Connect-AzAccount -ErrorAction Stop | Out-Null
Select-AzSubscription -Subscription (Get-AzContext).Subscription -ErrorAction Stop | Out-Null

if (-not (Get-AzResourceGroup -Name $ResourceGroup -ErrorAction SilentlyContinue)) {
    Write-Host "Creating resource group $ResourceGroup in $Location..."
    New-AzResourceGroup -Name $ResourceGroup -Location $Location -ErrorAction Stop | Out-Null
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$bicepFile = Join-Path $scriptDir 'main.bicep'

Write-Host "Deploying web app $WebAppName..."
New-AzResourceGroupDeployment `
    -ResourceGroupName $ResourceGroup `
    -TemplateFile $bicepFile `
    -webAppName $WebAppName `
    -ErrorAction Stop

Write-Host "Deployment complete."
