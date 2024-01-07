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
    courses = course_factory(_quantity=10)
    id = courses[5].id
    base_url = 'http://127.0.0.1:8000/'
    url = base_url + '/api/v1/courses/' + str(id)
    headers = {
        'Content-Type': 'application/json',
    }
    # Act
    response = client.get(url, headers=headers)
    r_data = response.json()
    # Assert
    assert response.status_code == 200
    assert r_data['id'] == Course.objects.get(pk=id)
    

@pytest.mark.django_db
def test_list_courses(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    base_url = 'http://127.0.0.1:8000/'
    url = base_url + '/api/v1/courses'
    headers = {
        'Content-Type': 'application/json',
    }
    # Act
    response = client.get(url, headers=headers)
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_courses_filter_id(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    base_url = 'http://127.0.0.1:8000/'
    url = base_url + '/api/v1/courses'
    params = {
        'id': courses[5].id,
    }
    headers = {
        'Content-Type': 'application/json',
    }
    # Act
    response = client.get(url, params=params, headers=headers)
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert data['id'] == Course.objects.filter(id=params['id'])


@pytest.mark.django_db
def test_courses_filter_name(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    base_url = 'http://127.0.0.1:8000/'
    url = base_url + '/api/v1/courses'
    params = {
        'name': courses[5].name,
    }
    headers = {
        'Content-Type': 'application/json',
    }
    # Act
    response = client.get(url, params=params, headers=headers)
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert data['name'] == Course.objects.filter(name=params['name'])


@pytest.mark.django_db
def test_course_create(client):
    # Arrange
    base_url = 'http://127.0.0.1:8000/'
    url = base_url + '/api/v1/courses'
    headers = {
        'Content-Type': 'application/json',
    }
    count = Course.objects.count()
    # Act
    response = client.post(url, data={'id': 1, 'name': 'Python'}, headers=headers)  # формат указал в настройках
    # Assert
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_course_update(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=3)
    id = courses[0].id
    base_url = 'http://127.0.0.1:8000/'
    url = base_url + '/api/v1/courses' + str(id)
    headers = {
        'Content-Type': 'application/json',
    }
    # Act
    response = client.patch(url, data={'name': 'Python'}, many=False, partial=True, headers=headers)
    # Assert
    assert response.status_code == 200


@pytest.mark.django_db
def test_course_delete(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=3)
    id = courses[0].id
    base_url = 'http://127.0.0.1:8000/'
    url = base_url + '/api/v1/courses' + str(id)
    headers = {
        'Content-Type': 'application/json',
    }
    id_list = []
    for course in courses:
        id_list.append(course.id)
    # Act
    response = client.delete(url, headers=headers)
    # Assert
    assert response.status_code == 204
    assert id not in id_list