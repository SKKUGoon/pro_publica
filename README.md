# Propublica Congress API

<p>
API Connector that requests american congress information.
</p>

## class Congress
<p>
util functions(static)
- def header()
- def query(*args)
</p>

<p>
- 1. def get_members
- 2. def get_committees

example usage
</p>

```python
c = Congress()
r = c.get_members(102, "house")
c.process(r)
```