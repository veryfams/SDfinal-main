# Test de balanceo de carga para el endpoint /instancia
Write-Host "Test de balanceo de carga para el endpoint /instancia" -ForegroundColor Cyan
Write-Host "--------------------------------------------------------" -ForegroundColor Cyan

for ($i = 1; $i -le 10; $i++) {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/instancia"
    $instancia = $response.instancia
    Write-Host ("Peticion $i -> Respondio: $instancia") -ForegroundColor Green
    Start-Sleep -Milliseconds 500
}
