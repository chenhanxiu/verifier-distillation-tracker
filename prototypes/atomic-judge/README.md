# Atomic Agent Judge v0.1

一个可本地训练的 Agent 原子判据评审原型：开放 decoder-only 骨干 + LoRA + 共享三分类头。支持单判据、YOFO 启发的多位置读出、任务分组切分、温度校准与概率评测。

**这是功能原型，不是 Jev / RLCD 的精确复现，也不是已经训练好的 Judge。** 不调用 Jev API。示例全部虚构；不含公司数据。Jev 的完整结构与训练配方未公开，本项目采用公开可实现的监督学习路线。

## 整体逻辑

1. 从 Agent 轨迹中整理任务、相关用户消息、工具调用、工具结果及最终状态。
2. 一个判据对应一个标签：`satisfied`（满足）、`violated`（不满足）、`insufficient_evidence`（证据不足）。
3. 按任务族切分 train / dev / calibration / test。相同轨迹及同源变体不可跨集合。
4. 模型读取证据与判据，在判定位置取隐藏状态，经过共享 Linear(hidden_size, 3)。
5. 仅训练 LoRA 和分类头，以交叉熵监督判定；不生成解释、不进行自回归解码。
6. 根据 dev NLL 保存最佳 epoch；单独保存 adapter、分类头、tokenizer 和配置。
7. 在 calibration 集拟合正温度 T，得到 softmax(logits / T)。
8. 最后在 test 上评测；概率、语义上的证据不足和代码硬门槛共同决定是否升级强 Judge / 人工。

上层 8/37 能力树与五维评分不由本模型替代。本版输出原子判据，五维映射、硬门槛和加权规则应在业务代码中明确制定。本版没有擅自定义这些业务规则。

## 文件说明

| 文件 | 作用 |
|---|---|
| `data.py` | JSONL 校验、任务族切分、泄漏检查、判据分组及无标签 Prompt 编码 |
| `model.py` | 本地骨干、LoRA、共享分类头、右侧 padding、多个判定位置读出 |
| `run.py` | split / train / calibrate / evaluate / predict CLI |
| `metrics.py` | 温度搜索、NLL、Brier、macro-F1、混淆矩阵、ECE、覆盖率—错误率 |
| `examples/demo.jsonl` | 72 条虚构判据实例，仅验证流程 |
| `tests/test_core.py` | 标签泄漏、分组切分、校准、指标测试 |
| `tests/smoke.py` | 随机 tiny Llama 的离线端到端测试 |

## 数据协议

一行一个 JSON 对象；标注文件必需字段如下：

```json
{
  "task_family_id": "alarm-edit-family-001",
  "trajectory_id": "alarm-run-001",
  "criterion_id": "claim_grounded",
  "criterion_text": "最终答复声称修改成功，是否得到执行结果支持？",
  "evidence": {
    "task": "修改已有闹钟，不要新建",
    "tool_call": {"operation": "create", "id": "B"},
    "tool_result": {"status": "success", "id": "B"},
    "final_response": "已经修改原闹钟"
  },
  "label": "violated",
  "evidence_refs": ["tool_call", "tool_result", "final_response"],
  "label_source": "human_review"
}
```

可选 `criteria` 为三个类别的完整文字定义，key 必须等于上述三类；默认定义见 `data.py`。真实任务推荐提供更具体的边界说明。`predict` 允许省略 label、evidence_refs、label_source，但仍需要任务族、轨迹 ID 和判据 ID。

- `task_family_id` 必须把同模板、最小差异变体、重复运行归为同族，不能简单给每条数据随机 ID。
- `evidence_refs` 仅作标注审计，不输入模型；程序不验证路径语义，需人工/数据管道核验。
- **证据整理边界**：本版接受已整理的 evidence，不实现任意 harness 日志的自动解析。输入应采用固定、与标签无关的证据选择规则。不要把人工解析、Judge 理由、gold 状态结论混入 evidence。
- 多判据模式下，同一 trajectory_id 的 evidence 和 task_family_id 必须完全一致。
- 证据不足不是低置信度；它是一个明确的语义类别。不适用的判据在准备数据时过滤。
- `label_source` 可取 human_review / program_verified / teacher_reviewed / synthetic_demo 等；教师投票不自动等于真值。

## 环境

Python 3.10+。在虚拟环境安装 `requirements.txt`。依赖采用兼容范围，不是完整锁文件；实际训练请记录 `pip freeze`。本次 CPU 验证环境：torch 2.14.0+cpu、transformers 4.57.6、peft 0.18.1。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

离线环境请提前在联网机器准备依赖 wheel 和骨干权重。所有模型/tokenizer 加载使用 `local_files_only=True`，不自动下载、不运行 remote custom code。

支持有 `hidden_size`、输出 `last_hidden_state` 的标准 decoder-only AutoModel。首先使用公司已部署的中文开放模型目录；不支持 encoder-decoder、视觉骨干、多 GPU、QLoRA 或断点恢复。模型需完整装入单设备，默认 float32；GPU 资源允许可用 `--dtype bfloat16`，须确保硬件支持。CPU 用于冒烟测试，实际大模型训练建议 GPU。

## 最小训练流程

以下示例只验证流程；demo 的类别与任务过于简单，不能报告业务效果。真实数据放 `private_data/`（已忽略），不要提交生产轨迹。

```bash
python run.py split --data examples/demo.jsonl --out runs/splits

python run.py train \
  --base /models/your-decoder-model \
  --train runs/splits/train.jsonl --dev runs/splits/dev.jsonl \
  --out runs/single --mode single \
  --epochs 3 --batch-size 1 --lr 0.0001 --rank 8 \
  --max-length 4096 --device cuda --dtype bfloat16

python run.py calibrate \
  --checkpoint runs/single --data runs/splits/calibration.jsonl \
  --out runs/single-temperature.json --device cuda

python run.py evaluate \
  --checkpoint runs/single --data runs/splits/test.jsonl \
  --calibration runs/single-temperature.json \
  --out runs/single-test.json --device cuda

python run.py predict \
  --checkpoint runs/single --data runs/splits/test.jsonl \
  --calibration runs/single-temperature.json \
  --out runs/predictions.jsonl --device cuda
```

训练/split 输出目录必须不存在，防止覆盖旧实验。移动机器后用 `--base /new/local/path` 指定**同一份**骨干权重；checkpoint 只保存 adapter 和 head，不包含原始骨干。不要在相同路径下替换骨干版本。

### 多判据实验

用同一数据、同一骨干，训练命令改为 `--mode multi --out runs/multi`，其余流程相同，但必须另拟合该 checkpoint 的温度。

单判据：证据 + 判据 → 一个位置 → 三分类。
多判据：共同证据 + 判据1 + 判定位置1 + 判据2 + 判定位置2 → 一次 forward → 各位置共享分类头。

不新增特殊 token，使用每个固定“判定：”结尾的最后 token 位置作为读出点。训练和推理均无真实答案填入 Prompt；只在 loss 中使用标签。padding 判据的位置以 -1 表示、标签为 -100，loss 忽略这些位置。

**多判据并非彼此独立**：普通因果注意力下，后面的判据可看到前面的判据文本。第一版不实现分支 attention mask；上线前需测试换序、增删判据和长度的敏感性。单/多模式的训练与推理格式由 checkpoint 配置固定。

长输入直接报错，不静默截断。生产接入需显式选取证据或分组判据；不要丢弃决定标签的后续恢复步骤。多模式分组越多不一定越快，应实测。

## 校准和指标

- 温度在 exp([-4, 4]) 的 401 个候选值上搜索 calibration NLL 最小值，含 T=1。这不是 RLCD。
- 校准 JSON 绑定 adapter/head/config 的 SHA-256，避免混用 checkpoint。
- calibrate 禁止使用 train/dev 的任务族或轨迹；evaluate 还禁止使用已知 calibration 数据。
- 没传 `--calibration` 的评测使用 T=1，属于未校准结果。
- 程序只能检查提供的 ID 是否相交，无法自动识别错标 ID 或语义近重复。
- `macro_f1` 固定按三类平均，缺失类别的 F1 记 0；报告混淆矩阵和样本量再解释数值。
- ECE 为最大概率的十桶 top-label 校准误差；小样本 ECE 不稳定。
- `violation_miss_rate` 把 violated 被预测成其余两类都计为漏检；生产中 evidence不足会转人工，因此还需业务级漏放统计。
- coverage_risk 仅自动接纳非 evidence不足且最大概率超过阈值的预测；阈值表是诊断，不是上线阈值。不得用 test 选阈值后再宣称无偏性能。
- `max_probability` 是分布峰值，不是 Jev confidence，也不是正确率保证。
- infer 的批次耗时包括 tokenization / 搬运 / forward，排除加载，保留冷启动首批；不是稳定服务 P95。比较时固定硬件、batch、输入和 dtype，充分预热后另测线上延迟。

训练集可定向增补 rare failure；校准和测试应反映实际目标分布，否则概率不具有业务频率含义。数据量小时不建议按判据各自拟合温度。

## 验证代码

轻量测试无需安装模型依赖：

```bash
python -m unittest discover -s tests -v
```

安装依赖后，完全离线的模型测试：

```bash
OMP_NUM_THREADS=1 python tests/smoke.py runs/smoke
```

它本地创建随机 tiny Llama 与极简 tokenizer，对 single/multi 分别执行训练→保存→加载→校准→评测→预测。随机模型和极简 tokenizer **没有语义判断能力**；测试仅证明代码路径，不证明模型准确率、校准泛化或速度收益。

## 推荐的业务验收

先标注“假完成”问题，再扩展最新目标和失败恢复；保留未参与训练的任务族与工具。与同骨干短标签生成基线、当前强 Judge 对比：宏 F1、严重失败漏放率、概率质量、覆盖率—风险、每秒判据数。还需检查工具报错后恢复、Prompt 注入、长轨迹和判据换序。

当前原型不含自动证据提取、生成式基线、教师蒸馏、五维业务聚合、在线服务、分布式训练和 RL。先验证判别式路线有效，再添加这些模块。

## 方法来源

- [YOFO: You Only Forward Once](https://arxiv.org/abs/2511.16600)：多判据指定位置读出；本项目改为三分类头，不是论文原样复现。
- [ArmoRM](https://arxiv.org/abs/2406.12845)：隐藏表示上直接预测奖励的参考。
- [Jev / RLCD 公开介绍](https://docs.typesafe.ai/introduction/machine-learning-primer)：功能设计启发，无内部实现复现声明。
- [PEFT LoRA](https://huggingface.co/docs/peft/package_reference/lora)：开放实现。
