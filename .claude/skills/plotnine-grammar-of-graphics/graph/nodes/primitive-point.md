# primitive-point

Geom: `geom_point()`

Use for observation-level x/y relationships.

```python
+ geom_point(alpha=0.8, size=3)
```

Required mappings: usually `x`, `y`.

Common mappings: `color`, `shape`, `size`, `alpha`.

Pairs with: `primitive-smooth`.

## Examples

### Basic Scatter

```python
+ geom_point(alpha=0.8, size=3)
```

### Color By Category

```python
ggplot(df, aes(x='hp', y='mpg', color='factor(cyl)')) + geom_point()
```

### Overlay Points On A Line

```python
+ geom_line(color='steelblue')
+ geom_point(size=2)
```
