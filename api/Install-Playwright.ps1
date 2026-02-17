# ======================================================================
# Script : Install-Playwright.ps1
# Objet  : Lire PROXY_URL depuis un fichier .env, configurer l'env,
#          puis lancer playwright.exe install
# ======================================================================

$ErrorActionPreference = "Stop"

# --- 1. Lecture du fichier .env ---------------------------------------

$envFilePath = Join-Path -Path (Get-Location) -ChildPath ".env"

if (-not (Test-Path $envFilePath)) {
    Write-Host "[ERREUR] Fichier .env introuvable : $envFilePath"
    Write-Host "         Crée un fichier .env contenant par exemple :"
    Write-Host '         PROXY_URL=http://user:password@proxy.host:8080'
    exit 1
}

Write-Host "[INFO] Lecture du fichier .env : $envFilePath"

# Fonction simple pour parser .env (lignes 'clé=valeur', ignore # et lignes vides)
$envContent = Get-Content $envFilePath | Where-Object {
    $_ -and ($_ -notmatch '^\s*#') -and ($_ -match '=')
}

$envDict = @{}

foreach ($line in $envContent) {
    $parts = $line -split '=', 2
    if ($parts.Count -eq 2) {
        $key = $parts[0].Trim()
        $val = $parts[1].Trim()
        $envDict[$key] = $val
    }
}

# Récupération des valeurs utiles
$ProxyUrl   = $envDict["PROXY_URL"]

# --- 2. Configuration du proxy ----------------------------------------

if ($ProxyUrl -and $ProxyUrl.Trim() -ne "") {
    Write-Host "[INFO] Configuration du proxy depuis .env : $ProxyUrl"
    $env:HTTP_PROXY  = $ProxyUrl
    $env:HTTPS_PROXY = $ProxyUrl
} else
{
    Write-Host "[INFO] Aucune valeur PROXY_URL dans .env (pas de proxy configuré)."
}


# --- 5. Lancement de l'installation Playwright ------------------------

Write-Host "[INFO] Lancement de l'installation des navigateurs Playwright..."
playwright.exe install

if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCCÈS] Installation des navigateurs Playwright terminée."
} else {
    Write-Host "[ÉCHEC] L'installation a échoué avec le code : $LASTEXITCODE"
}