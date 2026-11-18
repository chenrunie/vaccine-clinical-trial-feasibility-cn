# 汇总指标反算脚本

`scripts/check_aggregate_metrics.py` 只接受汇总输入，用于发现报告中的基础算术差异。不得输入受试者逐例记录。

## 支持的指标

- `seroprotection_rate`
- `seropositivity_rate`
- `seroconversion_rate`
- `gmt`
- `gmc`
- `gmi`
- `gmfr`
- `gmr`
- `vaccine_efficacy`

## 输入格式

JSON顶层为列表。示例中的数值均为虚构汇总数据：

```json
[
  {
    "metric": "seroconversion_rate",
    "numerator": 92,
    "denominator": 100
  },
  {
    "metric": "gmt",
    "mean_log": 4.605170186,
    "log_base": "e"
  },
  {
    "metric": "gmr",
    "test_mean_log": 4.7,
    "control_mean_log": 4.5,
    "log_base": "e"
  },
  {
    "metric": "vaccine_efficacy",
    "vaccine_measure": 10,
    "control_measure": 25
  }
]
```

其中保护效力的 `vaccine_measure` 与 `control_measure` 必须使用相同口径：要么均为累积风险，要么均为人时发生率。

## 限制

- 不计算置信区间；
- 不判断非劣效、等效或临床意义；
- 不验证分子、分母或平均对数值如何从原始数据产生；
- 不替代SAP、经验证的统计程序和独立程序核查；
- 输出仅可标记为“汇总算术反算”。

