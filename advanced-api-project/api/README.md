## API Endpoints for Book Management

The Book API utilizes Django REST Framework's Generic Views for streamlined CRUD operations.

| Resource | HTTP Method | URL Path | View | Authentication |
| :--- | :--- | :--- | :--- | :--- |
| Book Collection | `GET` | `/api/books/` | `BookListCreateView` | None required (Read-Only) |
| Book Collection | `POST` | `/api/books/` | `BookListCreateView` | **Token/Session Required** |
| Single Book | `GET` | `/api/books/<id>/` | `BookRetrieveUpdateDestroyView` | None required (Read-Only) |
| Single Book | `PUT`/`PATCH`/`DELETE` | `/api/books/<id>/` | `BookRetrieveUpdateDestroyView` | **Token/Session Required** |

**Customizations & Behavior:**

1.  **Generic View Efficiency:** The views are implemented using `generics.ListCreateAPIView` and `generics.RetrieveUpdateDestroyAPIView`, which automatically map HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) to the corresponding Mixin actions.
2.  **Data Validation:** All creation and update requests are validated by the `BookSerializer`, which includes a custom check to prevent setting a future `publication_year`.
3.  **Permission Hooks:** The `permission_classes = [permissions.IsAuthenticatedOrReadOnly]` setting is a built-in DRF feature that handles the read-only/authenticated-write logic without requiring custom methods.