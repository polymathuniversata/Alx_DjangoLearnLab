# Delete Operation

**Python command:**
```python
from bookshelf.models import Book
book = Book.objects.get(title='Nineteen Eighty-Four')
book.delete()
print(Book.objects.all())
```

**Expected output:**
```
<QuerySet []>
```

# The Book instance was successfully deleted and no books remain in the database.
