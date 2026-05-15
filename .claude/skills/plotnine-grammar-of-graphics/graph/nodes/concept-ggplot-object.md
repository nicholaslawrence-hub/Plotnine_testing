# concept-ggplot-object

The root object binds data and global mappings.

```python
p = (
    ggplot(df, aes(x='x_col', y='y_col'))
    + geom_point()
    + labs(title='Title')
    + theme_minimal()
)
```

Rules:

- Use `+` to add layers.
- Put shared mappings in global `aes()`.
- Put layer-specific mappings inside the layer.
- Save explicitly in scripts.

## Examples

### Scatter Root

```python
p = (
    ggplot(df, aes(x='hp', y='mpg'))
    + geom_point()
)
```

### Count Root

```python
p = (
    ggplot(df, aes(x='factor(cyl)', fill='factor(cyl)'))
    + geom_bar()
)
```

### Layer-Specific Mapping

```python
p = (
    ggplot(df, aes(x='wt', y='mpg'))
    + geom_point()
    + geom_smooth(aes(color='factor(cyl)'), method='lm', se=False)
)
```
