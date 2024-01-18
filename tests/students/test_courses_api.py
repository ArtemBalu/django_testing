import pytest
import json
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
def test_one_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=1)
    id = courses[0].id
    url = f'/api/v1/courses/{id}/'
    response = client.get(url, format='json')
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert data['name'] == courses[0].name
    

@pytest.mark.django_db
def test_list_courses(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=3)
    url = '/api/v1/courses/'
    # Act
    response = client.get(url, format='json')
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_courses_filter_id(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=3)
    url = '/api/v1/courses/'
    # Act
    response = client.get(url, {'id': courses[1].id}, format='json')
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert data[0]['id'] == courses[1].id


@pytest.mark.django_db
def test_courses_filter_name(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=3)
    url = '/api/v1/courses/'
    # Act
    response = client.get(url, {'name': courses[1].name}, format='json')
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert data[0]['name'] == courses[1].name


@pytest.mark.django_db
def test_course_create(client):
    # Arrange
    url = '/api/v1/courses/'
    count = Course.objects.count()
    # Act
    response = client.post(url, data={'id': 1, 'name': 'Python'}, format='json')  # формат указал в настройках
    # Assert
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_course_update(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=3)
    id = courses[0].id
    url = f'/api/v1/courses/{id}/'
    # Act
    response = client.patch(url, data={'name': 'Python'}, many=False, partial=True, format='json')
    # Assert
    assert response.status_code == 200


@pytest.mark.django_db
def test_course_delete(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=3)
    id = courses[0].id
    url = f'/api/v1/courses/{id}/'
    # Act
    response_1 = client.delete(url, format='json')
    response_2 = client.get(url, format='json')
    # Assert
    assert response_1.status_code == 204
    assert response_2.status_code == 404