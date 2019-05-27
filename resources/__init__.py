from .student import (
    StudentResource,
    add_student_resources,
)
from .company import (
    CompanyResource,
    add_company_resources,
)


__all__ = [
    'add_student_resources',
    'add_company_resources',
    'StudentResource',
    'CompanyResource',
]
