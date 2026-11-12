# BotPsy：面向端侧个人助理的亚十亿参数 Agent 语言模型

- **作者**：Tether AI Research（报告页面署名贡献者：Milan Gritta、Jihye Back、JinUk Cho、Joon Kwon、Patrik Lambert、Mathias Buus、Amril Nurman）
- **首次公开日期**：2026-11-11
- **版本日期**：2026-11-11（Hugging Face 技术报告首版；QVAC 发布页同日更新）
- **原始报告**：https://huggingface.co/blog/qvac/botpsy
- **发布页**：https://qvac.tether.io/blog/on-device-ai-agent-botpsy
- **代码**：训练代码未公开
- **模型权重**：https://huggingface.co/qvac/BotPsy-0.8B
- **标识符**：无 arXiv ID、DOI；canonical URL 为 https://huggingface.co/blog/qvac/botpsy

## 一句话结论

【报告原文】0.8B 的 BotPsy 通过“工具轨迹 SFT → 三专家多教师 OPD → 两轮程序化奖励 RL”把六项工具/Agent 基准均值由基座的 24.7 提升到 45.0；【分析推断】它是当前“student 自己展开、teacher 给密集 token 信号、环境 verifier 再结算”的长轨迹小模型工程基线，但没有证明 MOPD 单独造成了多少收益。

## 真正新增的内容

【报告原文】BotPsy 将三个经 RL 专门化的 4B teacher（工具使用、通用推理、指令遵循）按 prompt 路由到同一个 0.8B student，在 student 自生成响应上执行逐 token reverse-KL；随后两轮 RL 不再依赖 teacher，而用规则和 verifier 奖励工具格式、工具名、参数名、参数值及最终任务表现。第二轮 RL 的训练混合中没有多轮对话，却仍提升了多轮函数调用。

【分析推断】新增价值不在提出新的 OPD 损失，而在公开了一个端到端 Agent 配方：先用多教师 OPD 修复工具 SFT 引起的通用能力回退，再让环境真值接管最终行为校正。它因此比单纯的 OPD benchmark 更接近现有 Agent verifier × OPD 路线。

## 核心方法

1. **SFT**：在模拟环境的多轮 Agent 轨迹、单/并行/多步工具调用，以及“不应调用工具”的样本上做全参数微调。
2. **多教师 OPD（MOPD）**：student 生成自己的响应；每个 prompt 被路由到工具、推理或指令遵循三类 4B specialist teacher 之一；teacher 在该 student prefix 上提供逐 token reverse-KL 信号。
3. **第一轮 RL**：采用 DAPO，重点训练工具调用；规则先检查推理与工具调用格式，再按工具名、参数名、参数值对 ground truth 的匹配给部分信用。
4. **第二轮 RL**：加入数学、代码、知识选择题、指令遵循、结构化输出和模拟工作场景中的多步工具使用；训练混合不含多轮对话。
5. **部署与评估**：发布 BF16 与 GGUF 权重；统一以 thinking mode 评估五个模型，部分 benchmark 进行 2–3 次运行。

## 关键实验结果

【报告原文】

- 六个工具/Agent 基准的非加权均值：BotPsy 45.0，Qwen3.5-0.8B 基座 24.7，Qwen3.5-2B 38.8。
- BFCL v4：44.0 对基座 23.4；ACEBench：58.7 对 30.1；τ-bench：51.5 对 23.2；ToolSandbox：64.6 对 30.5。
- BFCL v4 多轮部分由 7.5 提升到 46.1；τ²-bench telecom 达到 82.5，而 2B 对照为 69.3。
- IFEval 由 59.7 提升到 90.8，IFBench 由 22.0 提升到 55.9。
- 失败边界仍明显：BrowseComp-Plus 仅 4.5；τ³-banking 所有模型均低于 5；复杂信息检索场景均值仅 15。
- 报告按训练阶段展示能力变化，称 MOPD 将 SFT 后回退的知识与指令遵循恢复到基座以上，但正文未给出该阶段的完整逐项数字，也未提供“去掉 MOPD”的等算力终局消融。

## 证据质量与局限

【报告原文】优点包括统一评测 harness、公开权重、多个真实风格工具/Agent benchmark，以及对多轮、拒绝错误工具调用、推理 token 和任务轮数的分解。BFCL、τ-bench 等部分结果报告多次运行。

【报告原文】训练代码和训练数据未发布；模型只适合低到中等难度，主要训练和测试语言为英语，不适合高风险自动化。不同阶段使用不同数据混合，无法从最终分数识别 MOPD、数据增加与两轮 RL 的独立贡献。

【分析推断】这是机构技术报告而非同行评审论文；对照模型仅四个，未报告置信区间或完整 seed 方差，也没有独立 sealed evaluator。现有 benchmark 与训练数据许可清单可能存在任务族重叠，因此“同尺寸最强”应视为该 harness 下的结果，而不是普遍结论。

## 最接近的相关工作

- **Nemotron 系列 MOPD**：同样用 student rollout 与 specialist teacher 概率提供密集监督；BotPsy 更强调端侧 Agent、三专家 prompt 路由和后续 verifier-RL。
- **VG-OPD / ReFRAME**：前者由 verifier 选择专家，后者对齐环境 observation 后再蒸馏；BotPsy 只说明按 prompt 路由，未公开 verifier-gated 路由或 observation-alignment 机制。
- **Tool-N1 / ToolRL**：BotPsy 的 RL 阶段继承格式检查与工具参数部分信用，但把它放在 MOPD 之后。
- **OnPoKD / Verify Before You Distill**：都关注 teacher 可靠性与路由；BotPsy 没有报告逐 prompt teacher 校准或拒教机制。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可以把 BotPsy 的三段训练信号镜像到 verifier student：

1. 用环境重放得到的成功/失败/不可判定轨迹做 verifier SFT。
2. 在 student verifier 自己生成的评分与 critique states 上，请工具、推理、指令遵循三类 verifier teacher 输出完整序数分布，而不是只蒸馏均值。
3. 最后用可执行环境真值校正方向：工具名、参数、状态迁移和最终完成度由程序门控；teacher 分布只决定软幅度和不确定性。
4. 对没有合适工具、缺少必要参数、环境观测不完整的样本保留 abstain/T，而不是强迫二元好坏判断。

这是一条可执行的研究迁移路径，不是 BotPsy 已验证的结论；原报告训练的是行为 policy，不是 verifier。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level on-policy verifier distillation**：增加“行为 MOPD → verifier-grounded RL”的强工程对照；另建 score-level verifier student，检验软序数分布能否替代或补充 BotPsy 的 token reverse-KL。
- **pairwise A/B/T 与序数评分分布**：从同一环境状态采样两个工具分支，按可执行结果标 A/B；缺参数、无合适工具或证据不足标 T，并保留 teacher 的完整等级概率。BotPsy 本身没有做这项实验。
- **程序化/环境真值门控 teacher 信号**：直接复用工具名、参数名、参数值和状态转移的部分信用；硬真值决定更新方向，specialist teacher 只调节密度与幅度。
- **student-generated critique states**：在 Wi-Fi 关闭、邮箱已满、工具不存在等恢复节点，让 student 先生成 critique，再由环境重放验证其因果陈述后准入蒸馏。
- **高熵分叉下保留探索**：BotPsy 的单 teacher 路由与 reverse-KL 可能收缩到单一路径；在多个工具序列均成功时，保留多峰分布并降低 teacher 强制强度，报告分支覆盖率而非只报成功率。
- **独立 sealed eval**：冻结未参与 teacher 训练和路由的环境版本，隔离工具 schema、隐藏状态与最终 evaluator；同时做去掉 MOPD、去掉 RL、随机 teacher 路由和等算力实验，避免 policy 与 evaluator 共适应。
