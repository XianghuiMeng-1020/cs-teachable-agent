# CS Teachable Agent E2E Test Script
$ErrorActionPreference = "Continue"

$baseUrl = "http://localhost:3000"
$apiUrl = "http://127.0.0.1:8000/api"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$testUsername = "test_student_$timestamp"
$testPassword = "TestPass123!"

Write-Host "`n=== CS Teachable Agent E2E Testing ===" -ForegroundColor Cyan
Write-Host "Timestamp: $timestamp" -ForegroundColor Gray
Write-Host "Test User: $testUsername`n" -ForegroundColor Gray

# Test counter
$script:passCount = 0
$script:failCount = 0
$script:testResults = @()

function Test-API {
    param(
        [string]$Name,
        [string]$Url,
        [string]$Method = "GET",
        [hashtable]$Headers = @{},
        [string]$Body = $null
    )
    
    try {
        $params = @{
            Uri = $Url
            Method = $Method
            Headers = $Headers
            TimeoutSec = 15
            UseBasicParsing = $true
        }
        
        if ($Body) {
            $params.Body = $Body
            $params.ContentType = "application/json; charset=utf-8"
        }
        
        $response = Invoke-WebRequest @params
        
        Write-Host "[PASS] $Name" -ForegroundColor Green
        Write-Host "  Status: $($response.StatusCode)" -ForegroundColor Gray
        
        $script:passCount++
        $script:testResults += @{
            Test = $Name
            Status = "PASS"
            StatusCode = $response.StatusCode
        }
        
        return @{
            Success = $true
            StatusCode = $response.StatusCode
            Content = $response.Content
        }
    }
    catch {
        Write-Host "[FAIL] $Name" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
        
        $script:failCount++
        $script:testResults += @{
            Test = $Name
            Status = "FAIL"
            Error = $_.Exception.Message
        }
        
        return @{
            Success = $false
            Error = $_.Exception.Message
        }
    }
}

# Scenario 1: Registration and Login
Write-Host "`n--- Scenario 1: Student Registration & Login ---" -ForegroundColor Yellow

$result = Test-API -Name "Access Landing Page" -Url $baseUrl

$registerBody = @{
    username = $testUsername
    password = $testPassword
    role = "student"
} | ConvertTo-Json -Compress

$result = Test-API -Name "Register New Student" -Url "$apiUrl/auth/register" -Method "POST" -Body $registerBody

if ($result.Success) {
    $authData = $result.Content | ConvertFrom-Json
    $script:authToken = $authData.access_token
    Write-Host "  Token acquired" -ForegroundColor Gray
}

$loginBody = @{
    username = $testUsername
    password = $testPassword
} | ConvertTo-Json -Compress

$result = Test-API -Name "Login Student" -Url "$apiUrl/auth/login" -Method "POST" -Body $loginBody

if ($result.Success) {
    $authData = $result.Content | ConvertFrom-Json
    $script:authToken = $authData.access_token
}

if ($script:authToken) {
    $headers = @{
        "Authorization" = "Bearer $($script:authToken)"
    }
    
    $result = Test-API -Name "Get Current User Info" -Url "$apiUrl/auth/me" -Headers $headers
    
    if ($result.Success) {
        $user = $result.Content | ConvertFrom-Json
        $script:userId = $user.id
        Write-Host "  User ID: $($user.id), Role: $($user.role)" -ForegroundColor Gray
    }
}

# Scenario 2: TA Creation
Write-Host "`n--- Scenario 2: TA Creation & Domain Selection ---" -ForegroundColor Yellow

if ($script:authToken) {
    $headers = @{
        "Authorization" = "Bearer $($script:authToken)"
    }
    
    # Create Python TA
    $createTABody = @{
        name = "Python_TA_Test"
        domain_id = "python"
    } | ConvertTo-Json -Compress
    
    $result = Test-API -Name "Create Python TA" -Url "$apiUrl/ta" -Method "POST" -Headers $headers -Body $createTABody
    
    if ($result.Success) {
        $ta = $result.Content | ConvertFrom-Json
        $script:pythonTAId = $ta.id
        Write-Host "  Python TA ID: $($ta.id)" -ForegroundColor Gray
    }
    
    # Create Database TA
    $createTABody = @{
        name = "Database_TA_Test"
        domain_id = "database"
    } | ConvertTo-Json -Compress
    
    $result = Test-API -Name "Create Database TA" -Url "$apiUrl/ta" -Method "POST" -Headers $headers -Body $createTABody
    
    if ($result.Success) {
        $ta = $result.Content | ConvertFrom-Json
        $script:databaseTAId = $ta.id
        Write-Host "  Database TA ID: $($ta.id)" -ForegroundColor Gray
    }
    
    # Create AI Literacy TA
    $createTABody = @{
        name = "AI_Literacy_TA_Test"
        domain_id = "ai_literacy"
    } | ConvertTo-Json -Compress
    
    $result = Test-API -Name "Create AI Literacy TA" -Url "$apiUrl/ta" -Method "POST" -Headers $headers -Body $createTABody
    
    if ($result.Success) {
        $ta = $result.Content | ConvertFrom-Json
        $script:aiLiteracyTAId = $ta.id
        Write-Host "  AI Literacy TA ID: $($ta.id)" -ForegroundColor Gray
    }
    
    $result = Test-API -Name "List All TAs" -Url "$apiUrl/ta" -Headers $headers
    
    if ($result.Success) {
        $tas = $result.Content | ConvertFrom-Json
        Write-Host "  Total TAs: $($tas.Count)" -ForegroundColor Gray
    }
}

# Scenario 3: Teaching Interaction
Write-Host "`n--- Scenario 3: Teaching Interaction ---" -ForegroundColor Yellow

if ($script:authToken -and $script:pythonTAId) {
    $headers = @{
        "Authorization" = "Bearer $($script:authToken)"
    }
    
    # Teach about variables
    $teachBody = @{
        student_input = "Variables are like containers that store data. For example, x = 5 stores the number 5 in a variable named x."
    } | ConvertTo-Json -Compress
    
    $result = Test-API -Name "Teach Concept: Variables" -Url "$apiUrl/ta/$($script:pythonTAId)/teach" -Method "POST" -Headers $headers -Body $teachBody
    
    if ($result.Success) {
        $teachResponse = $result.Content | ConvertFrom-Json
        Write-Host "  TA Response Length: $($teachResponse.response.Length) chars" -ForegroundColor Gray
    }
    
    Start-Sleep -Seconds 2
    
    # Teach about loops
    $teachBody = @{
        student_input = "Loops let you repeat code multiple times. A for loop can iterate through a range of numbers."
    } | ConvertTo-Json -Compress
    
    $result = Test-API -Name "Teach Concept: Loops" -Url "$apiUrl/ta/$($script:pythonTAId)/teach" -Method "POST" -Headers $headers -Body $teachBody
    
    Start-Sleep -Seconds 2
    
    # Teach about functions
    $teachBody = @{
        student_input = "Functions are reusable blocks of code. You define them with def keyword and can call them multiple times."
    } | ConvertTo-Json -Compress
    
    $result = Test-API -Name "Teach Concept: Functions" -Url "$apiUrl/ta/$($script:pythonTAId)/teach" -Method "POST" -Headers $headers -Body $teachBody
    
    # Get chat history
    $result = Test-API -Name "Get Chat History" -Url "$apiUrl/ta/$($script:pythonTAId)/messages" -Headers $headers
    
    if ($result.Success) {
        $messages = $result.Content | ConvertFrom-Json
        Write-Host "  Messages: $($messages.messages.Count)" -ForegroundColor Gray
    }
    
    # Get knowledge state
    $result = Test-API -Name "Get Knowledge State" -Url "$apiUrl/ta/$($script:pythonTAId)/state" -Headers $headers
    
    if ($result.Success) {
        $state = $result.Content | ConvertFrom-Json
        Write-Host "  Knowledge Units: $($state.knowledge_units.Count)" -ForegroundColor Gray
        $script:knowledgeState = $state
    }
}

# Scenario 4: Testing & Assessment
Write-Host "`n--- Scenario 4: Testing & Assessment ---" -ForegroundColor Yellow

if ($script:authToken -and $script:pythonTAId) {
    $headers = @{
        "Authorization" = "Bearer $($script:authToken)"
    }
    
    # Get available problems
    $result = Test-API -Name "Get Problem List" -Url "$apiUrl/ta/$($script:pythonTAId)/problems" -Headers $headers
    
    if ($result.Success) {
        $problems = $result.Content | ConvertFrom-Json
        Write-Host "  Problems Available: $($problems.Count)" -ForegroundColor Gray
        
        if ($problems.Count -gt 0) {
            $script:testProblemId = $problems[0].id
            Write-Host "  Selected Problem ID: $($script:testProblemId)" -ForegroundColor Gray
        }
    }
    
    # Test single problem
    if ($script:testProblemId) {
        $testBody = @{
            problem_id = $script:testProblemId
        } | ConvertTo-Json -Compress
        
        $result = Test-API -Name "Run Single Problem Test" -Url "$apiUrl/ta/$($script:pythonTAId)/test" -Method "POST" -Headers $headers -Body $testBody
        
        if ($result.Success) {
            $testResult = $result.Content | ConvertFrom-Json
            $status = if ($testResult.passed) { "PASSED" } else { "FAILED" }
            Write-Host "  Test Result: $status" -ForegroundColor Gray
        }
        
        Start-Sleep -Seconds 2
    }
    
    # Comprehensive test
    $result = Test-API -Name "Run Comprehensive Test" -Url "$apiUrl/ta/$($script:pythonTAId)/test/comprehensive" -Method "POST" -Headers $headers
    
    if ($result.Success) {
        $compResult = $result.Content | ConvertFrom-Json
        Write-Host "  Pass Rate: $($compResult.total_passed)/$($compResult.total_run)" -ForegroundColor Gray
        Write-Host "  Tests Run: $($compResult.results.Count)" -ForegroundColor Gray
    }
}

# Scenario 5: Knowledge Visualization
Write-Host "`n--- Scenario 5: Knowledge Visualization ---" -ForegroundColor Yellow

if ($script:authToken -and $script:pythonTAId) {
    $headers = @{
        "Authorization" = "Bearer $($script:authToken)"
    }
    
    $result = Test-API -Name "Get Knowledge Graph Data" -Url "$apiUrl/ta/$($script:pythonTAId)/state" -Headers $headers
    
    if ($result.Success) {
        $state = $result.Content | ConvertFrom-Json
        $learnedCount = ($state.knowledge_units | Where-Object { $_.status -eq "learned" }).Count
        $totalCount = $state.knowledge_units.Count
        Write-Host "  Learned: $learnedCount / $totalCount" -ForegroundColor Gray
    }
    
    # Get mastery data
    $result = Test-API -Name "Get Mastery Data" -Url "$apiUrl/ta/$($script:pythonTAId)/mastery" -Headers $headers
    
    if ($result.Success) {
        $mastery = $result.Content | ConvertFrom-Json
        if ($mastery.mastery_percent -ne $null) {
            Write-Host "  Mastery Percentage: $($mastery.mastery_percent)%" -ForegroundColor Gray
        }
    }
}

# Scenario 6: History & Trace
Write-Host "`n--- Scenario 6: History & Trace ---" -ForegroundColor Yellow

if ($script:authToken -and $script:pythonTAId) {
    $headers = @{
        "Authorization" = "Bearer $($script:authToken)"
    }
    
    $result = Test-API -Name "Get History Records" -Url "$apiUrl/ta/$($script:pythonTAId)/history" -Headers $headers
    
    if ($result.Success) {
        $history = $result.Content | ConvertFrom-Json
        Write-Host "  Total Records: $($history.items.Count)" -ForegroundColor Gray
        
        $teachEvents = ($history.items | Where-Object { $_.type -eq "teach" }).Count
        $testEvents = ($history.items | Where-Object { $_.type -eq "test" }).Count
        Write-Host "  Teach Events: $teachEvents, Test Events: $testEvents" -ForegroundColor Gray
    }
    
    # Get trace data
    $result = Test-API -Name "Get Trace Data" -Url "$apiUrl/ta/$($script:pythonTAId)/trace" -Headers $headers
    
    if ($result.Success) {
        Write-Host "  Trace data retrieved successfully" -ForegroundColor Gray
    }
}

# UI Route Tests
Write-Host "`n--- UI Route Tests ---" -ForegroundColor Yellow

$routes = @(
    "/dashboard",
    "/teach",
    "/test",
    "/mastery",
    "/history"
)

foreach ($route in $routes) {
    $result = Test-API -Name "Route: $route" -Url "$baseUrl$route"
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$totalTests = $script:passCount + $script:failCount
$passRate = if ($totalTests -gt 0) { [Math]::Round(($script:passCount / $totalTests) * 100, 2) } else { 0 }

Write-Host "Total Tests: $totalTests" -ForegroundColor White
Write-Host "Passed: $($script:passCount)" -ForegroundColor Green
Write-Host "Failed: $($script:failCount)" -ForegroundColor Red
Write-Host "Pass Rate: $passRate%" -ForegroundColor $(if ($script:failCount -eq 0) { "Green" } else { "Yellow" })

# Save report
$reportPath = "e:\cs teachable agent\test_report_$timestamp.json"
$script:testResults | ConvertTo-Json -Depth 5 | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "`nDetailed report saved to: $reportPath" -ForegroundColor Cyan

if ($script:failCount -gt 0) {
    Write-Host "`nFailed Tests:" -ForegroundColor Red
    $script:testResults | Where-Object { $_.Status -eq "FAIL" } | ForEach-Object {
        Write-Host "  - $($_.Test)" -ForegroundColor Red
        if ($_.Error) {
            Write-Host "    Error: $($_.Error)" -ForegroundColor DarkRed
        }
    }
}

Write-Host "`nTesting Complete!`n" -ForegroundColor Green
