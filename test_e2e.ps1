# CS Teachable Agent - 端到端测试脚本
# 测试日期: 2026-03-14

$baseUrl = "http://localhost:3000"
$apiUrl = "http://127.0.0.1:8000/api"
$testResults = @()
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$testUsername = "test_student_$timestamp"
$testPassword = "TestPass123!"

function Log-Test {
    param(
        [string]$Scenario,
        [string]$Test,
        [string]$Status,
        [string]$Details = ""
    )
    
    $result = [PSCustomObject]@{
        Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Scenario = $Scenario
        Test = $Test
        Status = $Status
        Details = $Details
    }
    
    $testResults += $result
    
    $color = if ($Status -eq "PASS") { "Green" } elseif ($Status -eq "FAIL") { "Red" } else { "Yellow" }
    Write-Host "[$Status] $Scenario - $Test" -ForegroundColor $color
    if ($Details) {
        Write-Host "  Details: $Details" -ForegroundColor Gray
    }
    
    return $result
}

function Test-Endpoint {
    param(
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
            TimeoutSec = 10
            UseBasicParsing = $true
        }
        
        if ($Body) {
            $params.Body = $Body
            $params.ContentType = "application/json"
        }
        
        $response = Invoke-WebRequest @params
        return @{
            Success = $true
            StatusCode = $response.StatusCode
            Content = $response.Content
            Headers = $response.Headers
        }
    }
    catch {
        return @{
            Success = $false
            Error = $_.Exception.Message
            StatusCode = $_.Exception.Response.StatusCode.value__
        }
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "CS Teachable Agent - 端到端测试" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 场景 1: 学生注册和登录
Write-Host "`n=== 场景 1: 学生注册和登录 ===" -ForegroundColor Yellow

# 1.1 测试首页访问
$response = Test-Endpoint -Url $baseUrl
if ($response.Success -and $response.StatusCode -eq 200) {
    Log-Test "场景1" "访问首页" "PASS" "状态码: $($response.StatusCode)"
} else {
    Log-Test "场景1" "访问首页" "FAIL" "错误: $($response.Error)"
}

# 1.2 测试注册API
$registerBody = @{
    username = $testUsername
    password = $testPassword
    role = "student"
} | ConvertTo-Json

$response = Test-Endpoint -Url "$apiUrl/auth/register" -Method "POST" -Body $registerBody
if ($response.Success) {
    Log-Test "场景1" "用户注册" "PASS" "用户名: $testUsername"
    $global:authToken = ($response.Content | ConvertFrom-Json).access_token
} else {
    Log-Test "场景1" "用户注册" "FAIL" "错误: $($response.Error)"
}

# 1.3 测试登录API
$loginBody = @{
    username = $testUsername
    password = $testPassword
} | ConvertTo-Json

$response = Test-Endpoint -Url "$apiUrl/auth/login" -Method "POST" -Body $loginBody
if ($response.Success) {
    Log-Test "场景1" "用户登录" "PASS" "获取到访问令牌"
    $global:authToken = ($response.Content | ConvertFrom-Json).access_token
} else {
    Log-Test "场景1" "用户登录" "FAIL" "错误: $($response.Error)"
}

# 1.4 测试获取当前用户信息
if ($global:authToken) {
    $headers = @{
        "Authorization" = "Bearer $($global:authToken)"
    }
    
    $response = Test-Endpoint -Url "$apiUrl/auth/me" -Headers $headers
    if ($response.Success) {
        $user = $response.Content | ConvertFrom-Json
        Log-Test "场景1" "获取用户信息" "PASS" "用户ID: $($user.id), 角色: $($user.role)"
        $global:userId = $user.id
    } else {
        Log-Test "场景1" "获取用户信息" "FAIL" "错误: $($response.Error)"
    }
}

# 场景 2: TA创建和领域选择
Write-Host "`n=== 场景 2: TA创建和领域选择 ===" -ForegroundColor Yellow

if ($global:authToken) {
    $headers = @{
        "Authorization" = "Bearer $($global:authToken)"
    }
    
    # 2.1 测试获取可用领域
    $response = Test-Endpoint -Url "$apiUrl/domains" -Headers $headers
    if ($response.Success) {
        $domains = $response.Content | ConvertFrom-Json
        Log-Test "场景2" "获取可用领域" "PASS" "找到 $($domains.Count) 个领域"
        $global:domains = $domains
    } else {
        Log-Test "场景2" "获取可用领域" "FAIL" "错误: $($response.Error)"
    }
    
    # 2.2 测试创建Python领域的TA
    $createTABody = @{
        name = "Python助教_测试"
        domain = "python"
    } | ConvertTo-Json
    
    $response = Test-Endpoint -Url "$apiUrl/tas" -Method "POST" -Headers $headers -Body $createTABody
    if ($response.Success) {
        $ta = $response.Content | ConvertFrom-Json
        Log-Test "场景2" "创建Python TA" "PASS" "TA ID: $($ta.id), 名称: $($ta.name)"
        $global:pythonTAId = $ta.id
    } else {
        Log-Test "场景2" "创建Python TA" "FAIL" "错误: $($response.Error)"
    }
    
    # 2.3 测试创建Database领域的TA
    $createTABody = @{
        name = "数据库助教_测试"
        domain = "database"
    } | ConvertTo-Json
    
    $response = Test-Endpoint -Url "$apiUrl/tas" -Method "POST" -Headers $headers -Body $createTABody
    if ($response.Success) {
        $ta = $response.Content | ConvertFrom-Json
        Log-Test "场景2" "创建Database TA" "PASS" "TA ID: $($ta.id)"
        $global:databaseTAId = $ta.id
    } else {
        Log-Test "场景2" "创建Database TA" "FAIL" "错误: $($response.Error)"
    }
    
    # 2.4 测试创建AI Literacy领域的TA
    $createTABody = @{
        name = "AI素养助教_测试"
        domain = "ai_literacy"
    } | ConvertTo-Json
    
    $response = Test-Endpoint -Url "$apiUrl/tas" -Method "POST" -Headers $headers -Body $createTABody
    if ($response.Success) {
        $ta = $response.Content | ConvertFrom-Json
        Log-Test "场景2" "创建AI Literacy TA" "PASS" "TA ID: $($ta.id)"
        $global:aiLiteracyTAId = $ta.id
    } else {
        Log-Test "场景2" "创建AI Literacy TA" "FAIL" "错误: $($response.Error)"
    }
    
    # 2.5 测试获取TA列表
    $response = Test-Endpoint -Url "$apiUrl/tas" -Headers $headers
    if ($response.Success) {
        $tas = $response.Content | ConvertFrom-Json
        Log-Test "场景2" "获取TA列表" "PASS" "找到 $($tas.Count) 个TA"
    } else {
        Log-Test "场景2" "获取TA列表" "FAIL" "错误: $($response.Error)"
    }
}

# 场景 3: 教学交互
Write-Host "`n=== 场景 3: 教学交互 ===" -ForegroundColor Yellow

if ($global:authToken -and $global:pythonTAId) {
    $headers = @{
        "Authorization" = "Bearer $($global:authToken)"
    }
    
    # 3.1 测试教学 - 变量概念
    $teachBody = @{
        message = "Variables are like containers that store data. For example, x = 5 stores the number 5 in a variable named x."
    } | ConvertTo-Json
    
    $response = Test-Endpoint -Url "$apiUrl/tas/$($global:pythonTAId)/teach" -Method "POST" -Headers $headers -Body $teachBody
    if ($response.Success) {
        $teachResponse = $response.Content | ConvertFrom-Json
        Log-Test "场景3" "教学-变量" "PASS" "TA回复长度: $($teachResponse.response.Length) 字符"
    } else {
        Log-Test "场景3" "教学-变量" "FAIL" "错误: $($response.Error)"
    }
    
    Start-Sleep -Seconds 2
    
    # 3.2 测试教学 - 循环概念
    $teachBody = @{
        message = "Loops let you repeat code multiple times. A for loop can iterate through a range of numbers."
    } | ConvertTo-Json
    
    $response = Test-Endpoint -Url "$apiUrl/tas/$($global:pythonTAId)/teach" -Method "POST" -Headers $headers -Body $teachBody
    if ($response.Success) {
        $teachResponse = $response.Content | ConvertFrom-Json
        Log-Test "场景3" "教学-循环" "PASS" "TA回复: $($teachResponse.response.Substring(0, [Math]::Min(50, $teachResponse.response.Length)))..."
    } else {
        Log-Test "场景3" "教学-循环" "FAIL" "错误: $($response.Error)"
    }
    
    Start-Sleep -Seconds 2
    
    # 3.3 测试教学 - 函数概念
    $teachBody = @{
        message = "Functions are reusable blocks of code. You define them with 'def' keyword and can call them multiple times."
    } | ConvertTo-Json
    
    $response = Test-Endpoint -Url "$apiUrl/tas/$($global:pythonTAId)/teach" -Method "POST" -Headers $headers -Body $teachBody
    if ($response.Success) {
        $teachResponse = $response.Content | ConvertFrom-Json
        Log-Test "场景3" "教学-函数" "PASS" "知识状态已更新"
    } else {
        Log-Test "场景3" "教学-函数" "FAIL" "错误: $($response.Error)"
    }
    
    # 3.4 测试获取聊天历史
    $response = Test-Endpoint -Url "$apiUrl/tas/$($global:pythonTAId)/messages" -Headers $headers
    if ($response.Success) {
        $messages = $response.Content | ConvertFrom-Json
        Log-Test "场景3" "获取聊天历史" "PASS" "找到 $($messages.Count) 条消息"
    } else {
        Log-Test "场景3" "获取聊天历史" "FAIL" "错误: $($response.Error)"
    }
    
    # 3.5 测试获取知识状态
    $response = Test-Endpoint -Url "$apiUrl/tas/$($global:pythonTAId)/state" -Headers $headers
    if ($response.Success) {
        $state = $response.Content | ConvertFrom-Json
        Log-Test "场景3" "获取知识状态" "PASS" "知识单元数: $($state.knowledge_units.Count)"
        $global:knowledgeState = $state
    } else {
        Log-Test "场景3" "获取知识状态" "FAIL" "错误: $($response.Error)"
    }
}

# 场景 4: 测试和评估
Write-Host "`n=== 场景 4: 测试和评估 ===" -ForegroundColor Yellow

if ($global:authToken -and $global:pythonTAId) {
    $headers = @{
        "Authorization" = "Bearer $($global:authToken)"
    }
    
    # 4.1 测试获取可用问题
    $response = Test-Endpoint -Url "$apiUrl/problems?domain=python" -Headers $headers
    if ($response.Success) {
        $problems = $response.Content | ConvertFrom-Json
        Log-Test "场景4" "获取问题列表" "PASS" "找到 $($problems.Count) 个问题"
        if ($problems.Count -gt 0) {
            $global:testProblemId = $problems[0].id
        }
    } else {
        Log-Test "场景4" "获取问题列表" "FAIL" "错误: $($response.Error)"
    }
    
    # 4.2 测试单个问题测试
    if ($global:testProblemId) {
        $testBody = @{
            problem_id = $global:testProblemId
        } | ConvertTo-Json
        
        $response = Test-Endpoint -Url "$apiUrl/tas/$($global:pythonTAId)/test" -Method "POST" -Headers $headers -Body $testBody
        if ($response.Success) {
            $testResult = $response.Content | ConvertFrom-Json
            $status = if ($testResult.passed) { "通过" } else { "失败" }
            Log-Test "场景4" "单个问题测试" "PASS" "测试结果: $status, 问题ID: $($global:testProblemId)"
            $global:testResult = $testResult
        } else {
            Log-Test "场景4" "单个问题测试" "FAIL" "错误: $($response.Error)"
        }
    }
    
    Start-Sleep -Seconds 2
    
    # 4.3 测试综合评估
    $response = Test-Endpoint -Url "$apiUrl/tas/$($global:pythonTAId)/comprehensive-test" -Method "POST" -Headers $headers
    if ($response.Success) {
        $compResult = $response.Content | ConvertFrom-Json
        Log-Test "场景4" "综合评估" "PASS" "掌握度: $($compResult.mastery_percentage)%, 测试数: $($compResult.results.Count)"
        $global:comprehensiveResult = $compResult
    } else {
        Log-Test "场景4" "综合评估" "FAIL" "错误: $($response.Error)"
    }
}

# 场景 5: 知识可视化
Write-Host "`n=== 场景 5: 知识可视化 ===" -ForegroundColor Yellow

if ($global:authToken -and $global:pythonTAId) {
    $headers = @{
        "Authorization" = "Bearer $($global:authToken)"
    }
    
    # 5.1 测试获取知识图谱数据
    $response = Test-Endpoint -Url "$apiUrl/tas/$($global:pythonTAId)/state" -Headers $headers
    if ($response.Success) {
        $state = $response.Content | ConvertFrom-Json
        $learnedCount = ($state.knowledge_units | Where-Object { $_.status -eq "learned" }).Count
        $totalCount = $state.knowledge_units.Count
        Log-Test "场景5" "知识图谱数据" "PASS" "已学习: $learnedCount/$totalCount"
    } else {
        Log-Test "场景5" "知识图谱数据" "FAIL" "错误: $($response.Error)"
    }
    
    # 5.2 测试掌握度页面
    $response = Test-Endpoint -Url "$baseUrl/mastery"
    if ($response.Success) {
        Log-Test "场景5" "掌握度页面访问" "PASS" "页面加载成功"
    } else {
        Log-Test "场景5" "掌握度页面访问" "FAIL" "错误: $($response.Error)"
    }
}

# 场景 6: 历史和追踪
Write-Host "`n=== 场景 6: 历史和追踪 ===" -ForegroundColor Yellow

if ($global:authToken -and $global:pythonTAId) {
    $headers = @{
        "Authorization" = "Bearer $($global:authToken)"
    }
    
    # 6.1 测试获取历史记录
    $response = Test-Endpoint -Url "$apiUrl/tas/$($global:pythonTAId)/history" -Headers $headers
    if ($response.Success) {
        $history = $response.Content | ConvertFrom-Json
        Log-Test "场景6" "获取历史记录" "PASS" "找到 $($history.Count) 条记录"
        
        # 检查事件类型
        $teachEvents = ($history | Where-Object { $_.event_type -eq "teach" }).Count
        $testEvents = ($history | Where-Object { $_.event_type -eq "test" }).Count
        Log-Test "场景6" "历史记录分类" "INFO" "教学事件: $teachEvents, 测试事件: $testEvents"
    } else {
        Log-Test "场景6" "获取历史记录" "FAIL" "错误: $($response.Error)"
    }
    
    # 6.2 测试历史页面访问
    $response = Test-Endpoint -Url "$baseUrl/history"
    if ($response.Success) {
        Log-Test "场景6" "历史页面访问" "PASS" "页面加载成功"
    } else {
        Log-Test "场景6" "历史页面访问" "FAIL" "错误: $($response.Error)"
    }
}

# 额外测试: UI组件和路由
Write-Host "`n=== 额外测试: UI组件和路由 ===" -ForegroundColor Yellow

# 测试各个页面路由
$pages = @(
    @{Name="仪表板"; Path="/dashboard"},
    @{Name="教学页面"; Path="/teach"},
    @{Name="测试页面"; Path="/test"},
    @{Name="掌握度页面"; Path="/mastery"},
    @{Name="历史页面"; Path="/history"}
)

foreach ($page in $pages) {
    $response = Test-Endpoint -Url "$baseUrl$($page.Path)"
    if ($response.Success) {
        Log-Test "UI测试" "$($page.Name)路由" "PASS" "路径: $($page.Path)"
    } else {
        Log-Test "UI测试" "$($page.Name)路由" "FAIL" "错误: $($response.Error)"
    }
}

# 生成测试报告
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "测试总结" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$passCount = ($testResults | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($testResults | Where-Object { $_.Status -eq "FAIL" }).Count
$totalCount = $testResults.Count

Write-Host "总测试数: $totalCount" -ForegroundColor White
Write-Host "通过: $passCount" -ForegroundColor Green
Write-Host "失败: $failCount" -ForegroundColor Red
Write-Host "通过率: $([Math]::Round(($passCount / $totalCount) * 100, 2))%" -ForegroundColor $(if ($failCount -eq 0) { "Green" } else { "Yellow" })

# 保存详细报告
$reportPath = "e:\cs teachable agent\test_report_$timestamp.json"
$testResults | ConvertTo-Json -Depth 10 | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "`n详细报告已保存到: $reportPath" -ForegroundColor Cyan

# 失败测试详情
if ($failCount -gt 0) {
    Write-Host "`n失败的测试:" -ForegroundColor Red
    $testResults | Where-Object { $_.Status -eq "FAIL" } | ForEach-Object {
        Write-Host "  - $($_.Scenario) - $($_.Test): $($_.Details)" -ForegroundColor Red
    }
}

Write-Host "`n测试完成!" -ForegroundColor Green
