from .students import (
    StudentsResource,
    add_student_resources,
)
from .companies import (
    CompaniesResource,
    add_company_resources,
)


__all__ = [
    'add_student_resources',
    'add_company_resources',
    'StudentsResource',
    'CompaniesResource',
]
