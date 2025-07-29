# Test de balanceo de carga para el endpoint /instancia
Write-Host "Test de balanceo de carga para el endpoint /instancia" -ForegroundColor Cyan
Write-Host "--------------------------------------------------------" -ForegroundColor Cyan

$conteo = @{}
for ($i = 1; $i -le 10; $i++) {
    try {
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/instancia"
        $instancia = $response.instancia
        if ($conteo.ContainsKey($instancia)) {
            $conteo[$instancia] += 1
        } else {
            $conteo[$instancia] = 1
        }

        Write-Host ("Petición $i -> Respondió: $instancia") -ForegroundColor Green
        Start-Sleep -Milliseconds 500
    } catch {
        Write-Host "Error en la petición $i" -ForegroundColor Red
    }
}

Write-Host "`nResumen de respuestas:" -ForegroundColor Yellow
foreach ($key in $conteo.Keys) {
    Write-Host ("$($key): $($conteo[$key]) respuestas") -ForegroundColor White
}
