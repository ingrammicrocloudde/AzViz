# Quickstart

We need to install GraphViz on our system before we can proceed with using the 'AzViz' PowerShell module. Depending upon the operating system you are using please follow the below mentioned steps:

### Linux

```bash
# Ubuntu
$ sudo apt install graphviz

# Fedora
$ sudo yum install graphviz

# Debian
$ sudo apt install graphviz
```

### Windows

```bash
# chocolatey packages Graphviz for Windows
choco install graphviz

# alternatively using windows package manager
winget install graphviz
```

### Mac

```bash
brew install graphviz
```

## Installation

### Deploy the sample Azure Web App (lists subscription resources)

1. Sign in:

   ```powershell
   Connect-AzAccount
   ```

2. Deploy the App Service plan + Web App (with managed identity) using Bicep:

   ```powershell
   cd ./webapp/infra
   ./deploy.ps1 -ResourceGroup rg-azviz-web -WebAppName azviz-demo-web
   ```

   The deployment assigns the Web App a system-assigned managed identity.

3. Grant subscription context to the app via app setting:

   ```powershell
   Set-AzWebApp -ResourceGroup rg-azviz-web -Name azviz-demo-web `
     -AppSettings @{ "AZURE_SUBSCRIPTION_ID" = (Get-AzContext).Subscription.Id }
   ```

4. Browse to `https://azviz-demo-web.azurewebsites.net` to see resources (first 200) in that subscription.

### From PowerShell Gallery

```Bash
# install from powershell gallery
Install-Module AzViz -Verbose -Scope CurrentUser -Force

# import the module
Import-Module AzViz -Verbose

# login to azure, this is required for module to work
Connect-AzAccount
```

### Clone the project from GitHub

```Bash
# optionally clone the project from github
git clone https://github.com/PrateekKumarSingh/AzViz.git
cd .\AzViz\
   
# import the powershell module
Import-Module .\AzViz.psm1 -Verbose

# login to azure, this is required for module to work
Connect-AzAccount
```
