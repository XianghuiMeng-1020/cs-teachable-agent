# Debug script to check data loading
$apiUrl = "http://127.0.0.1:8000/api"

# Login first
$loginBody = @{
    username = "test_student_20260314_234835"
    password = "TestPass123!"
} | ConvertTo-Json

$loginResponse = Invoke-WebRequest -Uri "$apiUrl/auth/login" -Method POST -Body $loginBody -ContentType "application/json" -UseBasicParsing
$token = ($loginResponse.Content | ConvertFrom-Json).access_token

$headers = @{
    "Authorization" = "Bearer $token"
}

Write-Host "`n=== Checking TA State ===" -ForegroundColor Cyan

# Get TA state
$stateResponse = Invoke-WebRequest -Uri "$apiUrl/ta/1/state" -Headers $headers -UseBasicParsing
$state = $stateResponse.Content | ConvertFrom-Json

Write-Host "`nKnowledge State Structure:" -ForegroundColor Yellow
$state | ConvertTo-Json -Depth 5 | Write-Host

Write-Host "`n=== Checking Problems ===" -ForegroundColor Cyan

# Get problems
$problemsResponse = Invoke-WebRequest -Uri "$apiUrl/ta/1/problems" -Headers $headers -UseBasicParsing
$problems = $problemsResponse.Content | ConvertFrom-Json

Write-Host "`nProblems Response:" -ForegroundColor Yellow
$problems | ConvertTo-Json -Depth 3 | Write-Host

Write-Host "`n=== Checking Messages ===" -ForegroundColor Cyan

# Get messages
$messagesResponse = Invoke-WebRequest -Uri "$apiUrl/ta/1/messages" -Headers $headers -UseBasicParsing
$messages = $messagesResponse.Content | ConvertFrom-Json

Write-Host "`nMessages Response:" -ForegroundColor Yellow
$messages | ConvertTo-Json -Depth 3 | Write-Host
