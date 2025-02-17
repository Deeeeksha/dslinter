---
title: "Loss API Misused"
disableShare: true
# ShowReadingTime: true
tags: ["api-specific", "model training", "error-prone"]
weight: 23
summary: "Check the input for loss API in PyTorch carefully."
---

### Description

### Context

Loss functions are always used in optimization problems. 

#### Problem

Different loss APIs accept different input formats, but the distinction is not made in some documentation or is overlooked by some developers, making it easy to misuse. For example, in PyTorch, the `NLLLoss` takes the output of `LogSoftmax` as the input. If the input given to `NLLLoss` has not been processed by `LogSoftmax`, it may lead to a wrong result.

#### Solution

Developers should check whether they use the loss API in PyTorch correctly.


### Type

API-Specific

### Existing Stage

Model Training

### Effect

Error-prone

### Example

```diff
### PyTorch
import torch.nn as nn
import torch

+ m = nn.LogSoftmax(dim=1)
loss = nn.NLLLoss()
input = torch.randn(3, 5, requires_grad=True)
target = torch.tensor([1, 0, 4])
- output = loss(input, target)
+ output = loss(m(input), target)
output.backward()
```

### Source:

#### Paper 

#### Grey Literature
- https://medium.com/missinglink-deep-learning-platform/most-common-neural-net-pytorch-mistakes-456560ada037

#### GitHub Commit

#### Stack Overflow

#### Documentation

