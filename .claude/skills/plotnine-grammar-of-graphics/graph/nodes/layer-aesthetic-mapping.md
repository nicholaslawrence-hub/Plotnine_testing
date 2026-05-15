# layer-aesthetic-mapping

Aesthetic mappings connect dataframe columns to visual channels.

Rules:

- Quote columns: `aes(x='mpg')`.
- Use constants outside `aes()`: `geom_point(color='steelblue')`.
- Use variables inside `aes()`: `aes(color='factor(cyl)')`.
- Use `factor(...)` when numeric values represent categories.

Channels:

```text
x, y, color, fill, group, alpha, size, shape, linetype, label
```

## Examples

### Numeric X/Y Mapping

```python
ggplot(df, aes(x='hp', y='mpg')) + geom_point()
```

### Categorical Numeric Mapping

```python
ggplot(df, aes(x='factor(cyl)', fill='factor(cyl)')) + geom_bar()
```

### Constant Outside Aes

```python
ggplot(summary_df, aes(x='Age', y='Mental_Health_Score')) + geom_line(color='steelblue')
```
