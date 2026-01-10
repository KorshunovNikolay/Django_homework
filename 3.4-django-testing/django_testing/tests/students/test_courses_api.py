import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student


#Фикстуры
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

#Тесты
# Проверка получения первого курса
@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args = [course.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name

# Проверка получения списка курсов
@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url)
    response_courses = {(course['id'], course['name']) for course in response.data}
    expected_courses = {(course.id, course.name) for course in courses}

    assert response.status_code == 200
    assert len(response.data) == 10
    assert response_courses == expected_courses

# Проверка фильтрации списка курсов по `id`
@pytest.mark.django_db
def test_filter_course_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    course = courses[5]
    url = reverse('courses-list')
    response = client.get(url, data={'id': course.id})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == course.id
    assert response.data[0]['name'] == course.name

# Проверка фильтрации списка курсов по `name`
@pytest.mark.django_db
def test_filter_course_by_name(client, course_factory):
    course_factory(name='course 1')
    course = course_factory(name='course 2')
    course_factory(name='course 3')
    url = reverse('courses-list')
    response = client.get(url, data={'name': course.name})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == course.id
    assert response.data[0]['name'] == course.name

# Тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    url = reverse('courses-list')
    response = client.post(url, data={'name': 'new course'})

    assert response.status_code == 201
    assert response.data['name'] == 'new course'
    assert 'id' in response.data

# Тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(name='old name')
    url = reverse('courses-detail', args=[course.id])
    response = client.patch(url, data={'name': 'new name'})

    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['name'] == 'new name'

# Тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])
    response = client.delete(url)
    get_response = client.get(url)


    assert response.status_code == 204
    assert get_response.status_code == 404













