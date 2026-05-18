# Установка Git hooks из папки githooks/
$Root = git rev-parse --show-toplevel
$HooksDir = Join-Path $Root ".git\hooks"
$Source = Join-Path $Root "githooks"

Copy-Item (Join-Path $Source "pre-commit") (Join-Path $HooksDir "pre-commit") -Force
Copy-Item (Join-Path $Source "post-commit") (Join-Path $HooksDir "post-commit") -Force
Write-Host "Hooks установлены в $HooksDir"
