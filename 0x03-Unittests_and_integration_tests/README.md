# Python Testing: Access Nested Map

This project tests the `access_nested_map` utility function using Python’s `unittest` framework and the `parameterized` library for multiple test cases. It includes unit tests that ensure the function behaves correctly with nested dictionaries and key paths.

## 0x03. Unittests and Integration Tests

This project is part of the ALX Software Engineering curriculum and focuses on writing **unit tests** and **integration tests** for Python modules using `unittest`, `mock`, and `parameterized`.

---

## 📂 Project Structure

├── client.py # GithubOrgClient class with GitHub API calls
├── fixtures.py # Sample data used for integration tests
├── test_client.py # Integration tests using parameterized_class and fixtures
├── test_utils.py # Unit tests for utility functions
├── utils.py # General-purpose utility functions
└── README.md # Project documentation

---

## ✅ Learning Objectives

- Understand the **difference between unit and integration tests**
- Write comprehensive tests using `unittest`
- Use `patch`, `Mock`, and `side_effect` for mocking behavior
- Parametrize tests with `parameterized.expand()` and `@parameterized_class`
- Maintain clean code and ensure **code quality with pycodestyle**

---

## 🧪 Test Coverage

| File            | Type         | Purpose                                      |
|-----------------|--------------|----------------------------------------------|
| `test_utils.py` | Unit Tests   | Tests for `access_nested_map`, `get_json`, and `memoize` functions |
| `test_client.py`| Integration  | Tests for `GithubOrgClient` using real-like mocked GitHub data |
| `fixtures.py`   | Test Data    | Contains mock payloads for GitHub API responses |

---

## 🔍 Sample Tests

**Unit Test (parameterized)**,

```python
@parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a", "b"), 2),
])
def test_access_nested_map(self, nested_map, path, expected):
    self.assertEqual(access_nested_map(nested_map, path), expected)

@classmethod
def setUpClass(cls):
    cls.get_patcher = patch("requests.get")
    mock_get = cls.get_patcher.start()

    def side_effect(url):
        if url == "https://api.github.com/orgs/google":
            return Mock(json=lambda: cls.org_payload)
        if url == cls.org_payload["repos_url"]:
            return Mock(json=lambda: cls.repos_payload)
    mock_get.side_effect = side_effect

 How to Run Tests
Install dependencies

pip install requests parameterized pycodestyle
Run unit tests

python -m unittest test_utils.py
Run integration tests


python -m unittest test_client.py
Check PEP8 style


pycodestyle .
📄 Fixtures Used
In fixtures.py:

org_payload = {
    "repos_url": "https://api.github.com/orgs/google/repos"
}

repos_payload = [
    {"id": 1, "name": "repo1", "license": {"key": "apache-2.0"}},
    {"id": 2, "name": "repo2", "license": {"key": "other"}}
]

expected_repos = ["repo1", "repo2"]
apache2_repos = ["repo1"]
These mock API responses are used in the integration tests for validating functionality.

👨‍💻 Author
Stevo
ALX Software Engineering Student
GitHub: @your-username

📌 Acknowledgments
Holberton School / ALX Curriculum

GitHub API Docs

Python unittest, mock, and parameterized modules


---

Let me know if you also want:
- Screenshots
- Markdown badge icons (like build status, test coverage)
- Versioning info

Otherwise, go ahead and **save the file as `README.md`** and commit it:
```bash
git add README.md
git commit -m "Add detailed README for testing project"
git push

