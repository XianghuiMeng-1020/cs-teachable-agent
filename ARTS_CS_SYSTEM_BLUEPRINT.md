# AI Resistant Teaching System for Computer Science (ARTS-CS)
## 系统蓝图与架构设计文档

---

## 1. 系统定位与核心概念

### 1.1 从 Teachable Agent 到 ARTS-CS 的演进

**AI Resistant Teaching System for Computer Science (ARTS-CS)** 融合了两种设计理念：

1. **原本设计体系（Stage One）**：以"Learning by Teaching"为核心，强调零知识起点、编程测试验证、精简可快速实现
2. **同事贡献体系（Full Framework）**：以"统一知识状态约束框架"为核心，强调跨领域可复用、误解完整生命周期、可遗忘/重学机制

### 1.2 ARTS-CS 核心主张

> **ARTS-CS 是一个统一的、知识状态约束的、误解感知的人工智能辅助教学系统，支持学生通过"教中学"（Learning by Teaching）的方式掌握计算机科学概念，同时系统具备抵抗 AI 生成内容干扰的能力。**

四个核心支柱：

| 支柱 | 描述 | 融合来源 |
|------|------|----------|
| **P1: Knowledge-State Constrained** | TA 行为由显式知识状态严格约束，而非自由生成 | 两体系共同强调 |
| **P2: Misconception Lifecycle** | 完整追踪误解从激活→纠正→遗忘→重学的全过程 | 同事体系核心贡献 |
| **P3: Cross-Domain Unified** | Python + Database + AI Literacy 共享核心引擎 | 同事体系架构设计 |
| **P4: AI-Resistant** | 系统能检测并应对学生使用 AI 作弊或 TA 生成不可靠内容的情况 | 新增安全层设计 |

---

## 2. 系统架构：双核融合设计

### 2.1 架构总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ARTS-CS 系统架构                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────┐   │
│  │   Frontend       │◄──►│    Backend       │◄──►│   LLM        │   │
│  │   (React/Vite)   │    │   (FastAPI)      │    │  (OpenAI/    │   │
│  │                  │    │                  │    │  DeepSeek)   │   │
│  └──────────────────┘    └────────┬─────────┘    └──────────────┘   │
│                                      │                              │
│                        ┌─────────────┴─────────────┐                 │
│                        ▼                             ▼                 │
│           ┌─────────────────────┐    ┌─────────────────────┐          │
│           │   Shared Core       │    │   Domain Layer    │          │
│           │   (8 引擎)          │    │   (3 领域)        │          │
│           └─────────────────────┘    └─────────────────────┘          │
│                        │                              │              │
│                        ▼                             ▼                 │
│           ┌─────────────────────┐    ┌─────────────────────┐          │
│           │   Knowledge State   │    │   Content/Adapter │          │
│           │   (统一模式)        │    │   (领域特定)      │          │
│           └─────────────────────┘    └─────────────────────┘          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Shared Core：8 个共享引擎（同事体系贡献）

| 引擎 | 功能 | 与 Stage One 的融合 |
|------|------|---------------------|
| **E1: 知识状态引擎** | 维护知识单元的完整生命周期状态 | 扩展 Stage One 的简化状态模型 |
| **E2: 交互引擎** | 处理教学输入→TA 响应的完整流程 | 保留 Stage One 的协议设计 |
| **E3: 学习者对话引擎** | 生成个性化对话响应 | LLM 作为被约束的生成器 |
| **E4: 任务/问题引擎** | 选择、呈现、评估编程问题 | 扩展 Stage One 的问题库 |
| **E5: TA 尝试引擎** | 生成 TA 代码并执行 | 保留 Stage One 的代码执行框架 |
| **E6: 掌握评估器** | 计算单元级和整体掌握度 | 融合 Stage One 的量规 |
| **E7: 误解/遗忘/重学引擎** | 核心创新：完整生命周期 | 同事体系核心贡献 |
| **E8: 防护/回退层** | AI-Resistant：检测异常、提供安全回退 | 新增安全层 |

### 2.3 Domain Layer：3 个领域实现

| 领域 | 状态 | 知识单元数 | 问题数 |
|------|------|------------|--------|
| **Python** | ✅ 完整实现 | ~35 | ~50-100 |
| **Database (SQL)** | 🔄 部分实现 | ~20 | ~30 |
| **AI Literacy** | 🔄 部分实现 | ~15 | ~25 |

**领域添加原则**：仅需添加内容和适配器，无需修改 Shared Core 引擎。

---

## 3. 知识状态模式：统一 Schema（融合设计）

### 3.1 全局字段

```json
{
  "domain": "python",
  "schema_version": "1.0",
  "last_updated": 1773550084.810432
}
```

### 3.2 每个知识单元的完整字段（融合版）

| 字段 | 来源 | 说明 |
|------|------|------|
| `knowledge_unit_id` | Stage One | 单元唯一标识 |
| `status` | Stage One + 扩展 | unknown → partially_learned → learned → misconception → corrected |
| `confidence` | 同事体系 | 掌握置信度 0-1 |
| `active_misconceptions` | 同事体系 | 当前激活的误解 ID 列表 |
| `teaching_evidence` | Stage One | 教学事件证据列表 |
| `testing_evidence` | Stage One | 测试事件证据列表 |
| `correction_evidence` | 同事体系 | 纠正事件证据列表 |
| `relearning_evidence` | 同事体系 | 重学事件证据列表 |
| `mastery_history` | 同事体系 | 掌握度历史记录 |

### 3.3 状态转移图（同事体系核心贡献）

```
        Teaching          Testing Pass
           │                   │
           ▼                   ▼
    ┌─────────────┐      ┌─────────────┐
    │   unknown   │─────►│   learned   │
    └─────────────┘      └──────┬──────┘
           │                     │
           │ Misconception       │ Correction Success
           ▼ detected            ▼
    ┌─────────────┐      ┌─────────────┐
    │misconception│─────►│  corrected  │
    └─────────────┘      └──────┬──────┘
                                │
                                │ Relearning Evidence
                                ▼
                           ┌─────────────┐
                           │   learned   │ (revalidated)
                           └─────────────┘
```

---

## 4. 误解生命周期引擎（同事体系核心贡献）

### 4.1 完整生命周期

1. **激活 (Activation)**
   - 触发：学生教学输入匹配误解模式
   - 动作：添加到 `active_misconceptions`
   - 影响：后续问题选择偏好激活误解相关题目

2. **行为 (Manifestation)**
   - 触发：TA 在测试中表现出误解
   - 动作：状态变为 `misconception`
   - 影响：降低相关 KU 置信度

3. **纠正 (Correction)**
   - 触发：学生针对性教学
   - 动作：生成纠正事件，添加到 `correction_evidence`
   - 状态：变为 `corrected`

4. **遗忘 (Unlearning)**
   - 触发：纠正后时间衰减或新教学冲突
   - 动作：降低 `corrected` 状态稳定性

5. **重学 (Relearning)**
   - 触发：遗忘后重新教学
   - 动作：添加到 `relearning_evidence`，状态恢复 `learned`

---

## 5. AI-Resistant 安全层（新增设计）

### 5.1 AI 作弊检测

| 检测类型 | 机制 | 响应 |
|----------|------|------|
| **输入异常检测** | 教学输入与历史模式对比 | 提示"请用自己的话解释" |
| **速度检测** | 输入速度过快 | 添加验证码或延迟 |
| **相似度检测** | 与已知 AI 生成内容比对 | 标记并通知教师 |

### 5.2 TA 生成内容验证

| 验证点 | 方法 | 回退策略 |
|--------|------|----------|
| **代码可执行性** | 沙箱执行 | 返回预定义错误响应 |
| **知识一致性** | 与知识状态比对 | 使用规则生成替代 |
| **响应质量** | 质量评分阈值 | 触发人工审核流程 |

---

## 6. 追踪与历史层（融合设计）

### 6.1 11 种事件类型（同事体系完整设计）

| 事件类型 | 来源 | 最小字段 |
|----------|------|----------|
| `teaching_event` | Stage One | student_input, topic, interpreted_units |
| `teaching_interpretation` | 同事体系 | interpreted_units, confidence |
| `knowledge_state_update` | Stage One | previous_state, new_state, trigger |
| `learner_dialogue` | Stage One | speaker, content, timestamp |
| `task_selection` | Stage One | problem_id, selection_reason |
| `ta_attempt` | Stage One | problem_id, code, execution_result |
| `evaluation_result` | Stage One | passed, score, feedback |
| `misconception_activation` | 同事体系 | misconception_id, trigger_evidence |
| `correction_event` | 同事体系 | misconception_id, correction_input |
| `relearning_event` | 同事体系 | unit_id, previous_state |
| `mastery_update` | Stage One | unit_id, previous_level, new_level |

---

## 7. 与现有系统的区分度（两体系共同强调）

| 维度 | 传统 ITS | LLM Tutor | ARTS-CS (本系统) |
|------|----------|-----------|------------------|
| **知识状态** | 隐式/黑盒 | 无显式状态 | ✅ **显式、可验证、约束行为** |
| **误解处理** | 预定义规则 | 无专门机制 | ✅ **完整生命周期、可研究** |
| **跨领域** | 重新开发 | 通用但不可靠 | ✅ **统一引擎+领域适配器** |
| **AI 安全** | 不涉及 | 无保障 | ✅ **多层防护、可回退** |
| **教学机制** | 系统教学生 | 对话式 | ✅ **学生教系统 (Learning by Teaching)** |
| **评估** | 答题正确率 | 无系统评估 | ✅ **TA 编程测试 + 掌握度量规** |

---

## 8. Demo 账户与使用指南

### 8.1 快速体验账户

| 角色 | 用户名 | 密码 | 用途 |
|------|--------|------|------|
| 学生 | `demo_student` | `demo123` | 体验学生端所有功能 |
| 学生 | `alice_cs101` | `demo123` | 已有教学历史的账户 |
| 教师 | `demo_teacher` | `demo123` | 体验教师仪表盘 |
| 教师 | `prof_chen` | `demo123` | 查看多学生数据 |

### 8.2 快速体验流程

1. **访问**: https://cs-teachable-agent.pages.dev/
2. **登录**: 使用 `demo_student` / `demo123`
3. **教学**: 进入 "Teach TA"，输入 Python 概念解释
4. **测试**: 进入 "Test TA"，运行编程测试
5. **查看**: 进入 "Mastery" 查看掌握度，"History" 查看历史
6. **教师视角**: 退出后用 `demo_teacher` 登录，查看学生分析

---

## 9. 迁移路线图（Stage One → ARTS-CS）

```
Stage One (当前可工作原型)
    │
    ▼
Stage A: 状态模式扩展
    │   └─ 添加完整 schema 字段 (correction_evidence, relearning_evidence, mastery_history)
    ▼
Stage B: 追踪/历史附加
    │   └─ 记录 11 种事件类型
    ▼
Stage C: 误解引擎集成
    │   └─ 状态驱动的误解激活 (替代 force_fail_problem_ids)
    ▼
Stage D: 遗忘/重学支持
    │   └─ 完整生命周期状态转移
    ▼
Stage E: 掌握聚合升级
    │   └─ mastery_history 持久化
    ▼
Stage F: 共享核心重构完成
    │   └─ Domain Layer 边界清晰
    ▼
Stage G: ARTS-CS 完整形态
        └─ 可添加 Database/AI Literacy 领域
```

---

## 10. 研究贡献与评估框架

### 10.1 核心研究问题

1. **RQ1**: 显式知识状态约束能否提高 TA 行为的可预测性和教育有效性？
2. **RQ2**: 误解生命周期追踪能否支持更有效的干预策略？
3. **RQ3**: 跨领域统一框架能否降低新领域开发成本？
4. **RQ4**: AI-Resistant 层能否有效检测和应对 AI 作弊？

### 10.2 评估指标

| 指标类型 | 具体指标 | 测量方法 |
|----------|----------|----------|
| **学习效果** | 学生掌握度提升 | 前后测试对比 |
| **系统可靠性** | TA 行为一致性 | 相同状态输入→相同输出测试 |
| **误解检测** | 检测准确率 | 人工标注对比 |
| **开发效率** | 新领域开发时间 | Database 领域开发耗时 |
| **AI 安全** | 作弊检测率 | 模拟 AI 输入测试 |

---

**文档版本**: 1.0  
**最后更新**: 2026-03-15  
**融合设计**: Stage One (原始) + Full Framework (同事体系) + AI-Resistant Layer (新增)
