# 🤖 TERMCODE--终端AI编程助手

## 📖 项目简介

TERMCODE 是一个运行在终端里的 AI 编程助手。用自然语言完成编码任务：读写文件、执行命令、派发子代理并行工作、代码审查、技能包扩展……一切都在交互式 TUI 中完成。

- **语言**：Python（>= 3.11），全部使用 `asyncio` 异步驱动
- **界面**：[Textual](https://github.com/Textualize/textual) TUI

## ✨ 功能特性

- 🖥️ **终端 TUI** — 基于 Textual 的交互式界面，支持多行输入与流式输出
- 🌐 **多模型支持** — Anthropic Claude / OpenAI / 任意 OpenAI 兼容 API（DeepSeek、Qwen 等）
- 👥 **Agent 团队** — 多 Agent 协作、coordinator 协调模式
- 🔌 **MCP 支持**
- 🧩 **技能包（Skills）** — 可插拔技能系统，内置 commit / review / test 等
- 🧠 **持久记忆** — 跨会话记忆、自动记忆与召回
- 🛡️ **权限系统** — 多种权限模式、规则引擎、危险命令检测、路径沙箱
- 📋 **Plan 模式** — 先规划、后执行
- 🌿 **Git Worktree** — 隔离环境并行开发
- 💾 **会话管理** — 会话保存 / 恢复 / 检查点回退

## 🏗️ 系统架构


| 层 | 模块 | 职责 |
|----|------|------|
| 交互层 | `app.py` | Textual TUI，输入框、流式输出、权限 / Plan / 会话对话框 |
| 代理层 | `agent.py` + `context/` + `hooks/` + `memory/` | 主循环：上下文管理、工具调度、生命周期 Hooks、记忆注入 |
| 能力层 | `tools/` `agents/` `teams/` `skills/` `mcp/` | Agent 的全部能力：执行命令、派发子代理、组建团队、加载技能、接入 MCP |
| 安全层 | `permissions/` | 权限模式、规则引擎、危险命令检测、工作目录沙箱 |
| 接入层 | `client.py` + `config.py` | 多协议 LLM 客户端与三层配置合并 |

## 🎯 核心功能

### ⌨️ 斜杠命令

| 命令 | 别名 | 说明 |
|------|------|------|
| `/help` | `/h` `/?` | 显示帮助信息 |
| `/clear` | | 清除对话历史 |
| `/compact` | `/c` | 压缩上下文 |
| `/plan` | `/p` | 切换到 Plan 模式 |
| `/review` | | 审查代码变更 |
| `/rewind` | | 回退到之前的检查点 |
| `/session` | | 会话管理（list / resume / new / delete） |
| `/skill` | `/skills` | 管理技能包（list / info / reload） |
| `/memory` | | 记忆管理（list / clear / edit） |
| `/permission` | | 权限管理（mode / rules / add / reset） |
| `/status` | `/s` | 显示状态信息 |
| `/mcp` | | 显示 MCP 服务器状态 |
| `/tasks` | `/task` | 管理后台任务（info / cancel） |
| `/trace` | `/tree` | 查看 Agent 父子追踪树 |

内置技能包也会自动注册为命令（如 `/commit`、`/test`）。

### 🤖 子代理

主代理可以派发子代理并行处理任务，内置 4 个：

| 代理 | 说明 |
|------|------|
| `explore` | 只读搜索代理，快速定位代码 |
| `general-purpose` | 通用任务代理 |
| `plan` | 软件架构规划代理 |
| `verification` | 校验代理 |


### 👥 Agent 团队

- 主代理可创建团队，多个 teammate 并行协作、互发消息
- 支持 in-process / tmux / iterm2 三种 teammate 后端
- coordinator 模式：由 coordinator 代理统一协调分工

### 🧩 技能包

技能包是可复用的「指令 + 工具」集合，目录结构：

```
.termcode/skills/
└── my-skill/
    ├── SKILL.md      # 技能说明（frontmatter 声明 name / description）
    ├── tool.json     # 可选：注册自定义工具
    └── references/   # 可选：参考资料
```

内置技能包：`commit`（提交代码）、`review`（代码审查）、`test`（编写测试）、`backend-interview`（后端面试）。


### 🧠 持久记忆

- 记忆文件持久化到磁盘，跨会话保留
- 自动记忆与召回：每次会话自动加载相关记忆
- `/memory list | clear | edit` 手动管理
- 自动加载项目指令文件 `TERMCODE.md`

### 🛡️ 权限系统

| 模式 | 说明 |
|------|------|
| `default` | 默认模式，危险操作需确认 |
| `acceptEdits` | 自动接受文件编辑，命令仍需确认 |
| `plan` | 只读规划模式，不执行修改 |
| `bypassPermissions` | 跳过所有权限检查（谨慎使用） |
| `custom` | 自定义规则 |
| `dontAsk` | 不再询问，直接执行 |

- **危险命令检测**：自动识别高危操作并强制确认
- **路径沙箱**：默认限制在工作目录内，防越权访问
- **规则引擎**：`~/.termcode/permissions.yaml` → `.termcode/permissions.yaml` → `.termcode/permissions.local.yaml`

### 📋 Plan 模式 / 🌿 Worktree / 💾 会话

- **Plan 模式**：Agent 先输出规划方案，人工确认后再执行修改
- **Git Worktree**：在隔离的 worktree 中并行开发，共享 `node_modules` 等目录（软链接）
- **会话管理**：会话持久化到磁盘，支持 `resume` 恢复、检查点 `rewind` 回退

## 🚀 快速开始

### 环境要求

- Python >= 3.11


### 配置

首次运行前需要创建配置文件 `.termcode/config.yaml`（项目级）或 `~/.termcode/config.yaml`（用户级）：

```yaml
# LLM 提供商，支持多 provider 配置
providers:
  - name: claude
    protocol: anthropic              # anthropic | openai | openai-compat
    base_url: https://api.anthropic.com
    model: claude-sonnet-4-5
    api_key: ${ANTHROPIC_API_KEY}    # 支持 ${ENV_VAR} 环境变量展开
    thinking: false

permission_mode: default             # default | acceptEdits | plan | bypassPermissions | custom | dontAsk
enable_fork: false                   # 允许子代理派生
enable_verification_agent: false     # 启用校验代理
teammate_mode: ""                    # "" | "in-process"
enable_coordinator_mode: false       # coordinator 协调模式

worktree:
  symlink_directories: ["node_modules", ".venv", "vendor"]
```

- 配置采用三层合并：`~/.termcode/config.yaml` → `.termcode/config.yaml` → `.termcode/config.local.yaml`，后者覆盖前者
- `api_key` 留空时自动回退到环境变量 `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`

### 启动

```bash
termcode                          # 进入交互式 TUI
termcode -p "帮我修复这个 bug"      # 非交互模式，输出到 stdout
termcode --mode acceptEdits       # 指定权限模式（覆盖配置文件）
```

### 🧪 开发

```bash
pip install -e ".[dev]"
pytest
```

## 📁 项目结构

```
termcode/
├── app.py            # Textual TUI 主界面
├── agent.py          # 主代理循环
├── client.py         # 多协议 LLM 客户端
├── config.py         # 配置加载与合并
├── agents/           # 子代理系统（加载器、任务管理、追踪）
├── teams/            # Agent 团队协作
├── skills/           # 技能包系统
├── commands/         # 斜杠命令（注册表 + 各命令处理器）
├── tools/            # Agent 工具（bash、文件读写、任务……）
├── mcp/              # MCP 客户端
├── memory/           # 持久记忆
├── hooks/            # 事件钩子
├── permissions/      # 权限检查、沙箱、规则引擎
├── context/          # 上下文管理
├── worktree/         # Git Worktree 管理
└── conversation.py   # 会话与检查点管理
```
