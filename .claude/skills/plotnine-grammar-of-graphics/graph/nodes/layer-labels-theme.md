# layer-labels-theme

Labels and themes make the chart readable and often appear in eval checks.

```python
+ labs(title='Daily Usage', x='Hours', y='Count', fill='Gender')
+ theme_bw()
+ theme(axis_title=element_text(face='bold'))
```

Use a base theme such as `theme_minimal()`, `theme_bw()`, `theme_classic()`, or `theme_light()`.

Use `theme(...)` only for targeted overrides.

## Examples

### Minimal Scatter Labels

```python
+ labs(title='Horsepower vs MPG', x='Horsepower', y='Miles per gallon', color='Cylinders')
+ theme_minimal()
```

### Classic Bar Labels

```python
+ labs(title='Cars by Cylinder Count', x='Cylinders', y='Count', fill='Cylinders')
+ theme_classic()
```

### Targeted Theme Override

```python
+ theme_bw()
+ theme(axis_title=element_text(face='bold'), panel_grid_minor=element_blank())
```
