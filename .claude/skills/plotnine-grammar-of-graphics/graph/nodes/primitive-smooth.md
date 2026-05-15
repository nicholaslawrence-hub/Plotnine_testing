# primitive-smooth

Geom: `geom_smooth()`

Use for trend lines over scatter plots.

```python
+ geom_smooth(method='lm', se=False)
```

Pairs with: `primitive-point`.

Use `se=False` when the prompt asks for no confidence interval.

## Examples

### Linear Trend

```python
+ geom_smooth(method='lm', se=False)
```

### Scatter With Trend

```python
+ geom_point(alpha=0.8)
+ geom_smooth(method='lm', se=False)
```

### Grouped Trend

```python
ggplot(df, aes(x='hp', y='mpg', color='factor(cyl)')) + geom_point() + geom_smooth(method='lm', se=False)
```
