# KAN_Impl

This folder contains the core PyTorch modules and utilities for KAN implementation.

## Key Features

### 1. **Custom Linear and Convolutional Layers**
- **KANLinear**: Implements a kernel-based linear layer with flexible quantization and regularization options.
- **KANConv**: Implements a kernel-based convolutional layer.

### 2. **Quantization and Clipping**
- **Clipping Quantization**: Set `quantize_clip=True` to use standard clipping for quantization (values outside the range are clipped).
- **Wrap-Around Quantization**: Set `quantize_clip=False` to use wrap-around (modulo) quantization (values outside the range wrap around).
- **Configurable Precision**: Set `tp` (total bits) and `fp` (fractional bits) in the constructor to control quantization precision.
- **Enable Quantization**: Set `quantize=True` in the constructor to enable quantization.

### 3. **Regularization and Loss Control**
- **L1/L2 Regularization**: The `regularization_loss` method supports L1 regularization on spline weights and entropy-based regularization.
- **Custom Loss Weighting**: When calling `regularization_loss`, you can set:
  - `regularize_activation`: Weight for L1 regularization (default: 1.0)
  - `regularize_entropy`: Weight for entropy regularization (default: 1.0)
  - `regularize_clipping`: Weight for quantization/clipping loss (default: 0.1)
- **Example:**
  ```python
  reg_loss = model.regularization_loss(
      regularize_activation=0.5,
      regularize_entropy=0.2,
      regularize_clipping=0.05
  )
  ```

## Main Classes and Arguments

### **KANLinear**
```python
KANLinear(
    in_features, out_features,
    grid_size=5, spline_order=3,
    scale_noise=0.1, scale_base=1.0, scale_spline=1.0,
    enable_standalone_scale_spline=True,
    base_activation=torch.nn.SiLU,
    grid_eps=0.02, grid_range=[-1, 1],
    quantize=False, tp=16, fp=6, lut_res=256,
    quantize_clip=False
)
```
- **Quantization**: Use `quantize`, `tp`, `fp`, `lut_res`, `quantize_clip`
- **Regularization**: Use `regularization_loss()` with custom weights