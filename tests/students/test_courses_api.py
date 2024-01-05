import pytest
from students.models import Course, Student

from rest_framework.test import APIClient
from model_bakery import baker

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_firt_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=1)
    base_url = 'http://127.0.0.1:8000/'
    url = base_url + '/api/v1/courses/'
    # Act
    response = client.get(url)
    # Assert
    assert response.status_code == 200
    


@pytest.mark.django_db
def test_list_courses():
    # Arrange

    # Act

    # Assert
   pass

@pytest.mark.django_db
def test_courses_filter_id():
    # Arrange

    # Act

    # Assert
   pass

@pytest.mark.django_db
def test_courses_filter_name():
   # Arrange

    # Act

    # Assert
   pass

@pytest.mark.django_db
def test_course_create():
   # Arrange

    # Act

    # Assert
   pass

@pytest.mark.django_db
def test_course_update():
   # Arrange

    # Act

    # Assert
   pass

@pytest.mark.django_db
def test_course_delete():
   # Arrange

    # Act

    # Assert
   pass