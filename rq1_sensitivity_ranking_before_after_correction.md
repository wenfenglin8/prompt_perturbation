# RQ1 敏感度排序：Sample-Noise Correction 前后对比

## 指标含义

RQ1 的敏感度排序可以分为 correction 前和 correction 后：

```text
correction 前 = 按 raw_perturbation_drift 排序

correction 后 = 按 noise_corrected_drift 排序
```

当前 RQ1 50x3 结果使用的 sample-noise baseline 是：

```text
noise_baseline = original_noise
```

其中：

```text
original_noise = original prompt 下重复生成之间的平均 pairwise embedding distance
```

因此：

```text
noise_corrected_drift = max(0, raw_perturbation_drift - original_noise)
```

## 整体 perturbation 排序

### Correction 前：按 raw drift 排序

```text
1. paraphrase          0.0719
2. formatting          0.0666
3. reordering          0.0600
4. surface_noise       0.0545
5. context_injection   0.0513
```

### Correction 后：按 noise-corrected drift 排序

```text
1. paraphrase          0.0321
2. formatting          0.0283
3. reordering          0.0221
4. surface_noise       0.0152
5. context_injection   0.0139
```

### 整体解释

整体 perturbation 排序在 correction 前后没有变化：

```text
paraphrase > formatting > reordering > surface_noise > context_injection
```

但是所有 perturbation 的敏感度数值都明显下降。

这说明 sample-noise correction 没有推翻总体排序，但显著降低了 prompt perturbation 的敏感度估计。

换句话说：

```text
raw drift 会高估 perturbation-specific sensitivity。
noise-corrected drift 给出了更保守、更接近扰动特异性影响的估计。
```

## 按任务排序

## factual_qa

### Correction 前

```text
1. paraphrase          0.0983
2. formatting          0.0437
3. reordering          0.0400
4. surface_noise       0.0381
5. context_injection   0.0332
```

### Correction 后

```text
1. paraphrase          0.0715
2. formatting          0.0230
3. reordering          0.0225
4. surface_noise       0.0210
5. context_injection   0.0164
```

### 解释

`factual_qa` 的排序基本不变。

`paraphrase` 在 correction 前后都明显最高，说明 factual QA 对 paraphrasing 的 semantic drift 最敏感。

Correction 后其他扰动类型的 drift 明显降低，但仍保留一定差异。

## math_reasoning

### Correction 前

```text
1. reordering          0.0752
2. surface_noise       0.0534
3. formatting          0.0530
4. paraphrase          0.0512
5. context_injection   0.0505
```

### Correction 后

```text
1. reordering          0.0282
2. formatting          0.0105
3. context_injection   0.0088
4. paraphrase          0.0079
5. surface_noise       0.0059
```

### 解释

`math_reasoning` 的排序变化最大。

尤其是 `surface_noise`：

```text
correction 前排名第 2
correction 后排名第 5
```

这说明 surface noise 在 math reasoning 中看起来敏感，主要是因为 raw drift 中包含了较多 sample noise。

校正后，`reordering` 仍然是 math reasoning 中最明显的 perturbation-specific sensitivity。

## code_generation

### Correction 前

```text
1. formatting          0.0832
2. paraphrase          0.0644
3. surface_noise       0.0491
4. reordering          0.0433
5. context_injection   0.0355
```

### Correction 后

```text
1. formatting          0.0562
2. paraphrase          0.0382
3. surface_noise       0.0228
4. reordering          0.0212
5. context_injection   0.0083
```

### 解释

`code_generation` 的排序在 correction 前后不变。

`formatting` 和 `paraphrase` 是 code generation 中最强的扰动类型。

Correction 后数值降低，但前两名仍然保留较明显的 perturbation-specific drift。

## open_ended_writing

### Correction 前

```text
1. formatting          0.0865
2. context_injection   0.0859
3. reordering          0.0813
4. surface_noise       0.0775
5. paraphrase          0.0735
```

### Correction 后

```text
1. formatting          0.0234
2. context_injection   0.0221
3. reordering          0.0165
4. surface_noise       0.0111
5. paraphrase          0.0109
```

### 解释

`open_ended_writing` 的排序基本不变，但 correction 后数值大幅下降。

这说明 open-ended writing 的 raw drift 很高，但其中很大一部分来自模型自然生成波动。

因此，对于开放式写作任务，如果不做 sample-noise correction，很容易把正常的生成多样性误判为 prompt perturbation 的影响。

## 总结

### 主要发现

```text
1. 整体排序 correction 前后没有变化：
   paraphrase > formatting > reordering > surface_noise > context_injection

2. correction 后所有 perturbation 的敏感度估计都下降。

3. math_reasoning 的排序变化最大，尤其是 surface_noise 从第 2 降到第 5。

4. open_ended_writing 的 raw drift 很高，但 corrected drift 很低，说明自然生成波动很大。

5. factual_qa 和 code_generation 在 correction 后仍保留较明显 sensitivity。
```

## 可写进论文的英文表述

```text
Sample-noise correction substantially reduces the estimated sensitivity magnitudes while largely preserving the overall perturbation ranking. The main exception is math reasoning, where surface noise appears sensitive under raw drift but drops sharply after correction, indicating that much of its apparent sensitivity is attributable to repeated-generation variability rather than perturbation-specific effects.
```

## 可写进论文的中文表述

```text
Sample-noise correction 显著降低了各类扰动的敏感度估计，但总体 perturbation 排序基本保持不变。主要例外是 math reasoning：surface noise 在 raw drift 下表现为较高敏感度，但在校正后明显下降，说明其表观敏感度很大程度上来自 repeated-generation variability，而不是扰动本身造成的特异性影响。
```
