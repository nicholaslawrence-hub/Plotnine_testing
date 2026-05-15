# layer-facets

Facets split a plot into small multiples.

```python
+ facet_wrap('Academic_Level')
+ facet_wrap('factor(gear)')
```

Use facets when the prompt says facet by, split by, small multiples, or compare panels.

Facet variables are usually categorical.

## Examples

### Facet By String Column

```python
+ facet_wrap('Academic_Level')
```

### Facet By Numeric Category

```python
+ facet_wrap('factor(gear)')
```

### Facet Grid

```python
+ facet_grid('Gender ~ Academic_Level')
```
