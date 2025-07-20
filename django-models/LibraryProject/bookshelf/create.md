# Create Operation

**Python command:**
```python
from bookshelf.models import Book
b = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
print(b)
```

**Expected output:**
```
1984 by George Orwell (1949)
```

# The Book instance was successfully created.
