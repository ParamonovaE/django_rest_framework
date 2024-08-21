import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_get_course(client, courses_factory):
    # Arrange
    course = courses_factory(name="Course 1")

    # Act
    response = client.get(f'/api/v1/courses/{course.id}/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == course.id
    assert data['name'] == course.name

@pytest.mark.django_db
def test_get_list_courses(client, courses_factory):
    # Arrange
    courses = courses_factory(_quantity=20)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)

@pytest.mark.django_db
def test_filter_courses_by_id(client, courses_factory):
    # Arrange
    course1 = courses_factory(name="Course 1")
    course2 = courses_factory(name="Course 2")
    courses_id = [course1.id, course2.id]

    # Act
    response = client.get(f'/api/v1/courses/?id={course1.id}&id={course2.id}')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses_id)
    for index, course in enumerate(data):
        assert course['id'] == courses_id[index]

@pytest.mark.django_db
def test_filter_courses_by_name(client, courses_factory):
    # Arrange
    course1 = courses_factory(name="Course 1")
    course2 = courses_factory(name="Course 2")
    courses_name = [course1.name, course2.name]

    # Act
    response = client.get(f'/api/v1/courses/?name={course1.name}&name={course2.name}')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses_name)
    for index, course in enumerate(data):
        assert course['name'] == courses_name[index]

@pytest.mark.django_db
def test_create_course(client):
    # Arrange
    count = Course.objects.count()

    # Act
    response = client.post('/api/v1/courses/', data={'name': 'Course'})

    # Assert
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

@pytest.mark.django_db
def test_update_course(client, courses_factory):
    # Arrange
    #course = courses_factory(name="Couse")
    courses = courses_factory(_quantity=5)
    course_for_update = courses[0]
    # Act
    response = client.put(f'/api/v1/courses/{course_for_update.id}/', data={'name': 'Course'})

    # Assert
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_course(client, courses_factory):
    # Arrange
    courses = courses_factory(_quantity=5)
    count = Course.objects.count()
    course_for_delete = courses[0]

    # Act
    response = client.delete(f'/api/v1/courses/{course_for_delete.id}/')

    # Assert
    assert response.status_code == 204
    assert Course.objects.count() == count - 1