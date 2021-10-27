import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from students.models import Course


def test_example():
    assert False, "Just test example"


def test_second_example():
    assert True, "Second test example"


def test_sample_view(client):
    url = reverse('sample')
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['status'] == 'OK!'


THREE_COURSES = [
    Course(name='Course A'),
    Course(name='Course B'),
    Course(name='Course C')
]
FIELDS_DATA = ['name', 'http_status']
COURSE_DATA = (
    ('Course One', HTTP_201_CREATED),
    ('Course Two', HTTP_201_CREATED),
    ('Course Three', HTTP_201_CREATED)
)


@pytest.mark.django_db
class TestCourses:
    def setup(self):
        self.url_list = reverse('courses-list')

# 1) проверка получения 1го курса
    def test_get_first(self, api_client, course_factory):
        course_factory(_quantity=7)
        first_course = Course.objects.first()
        url = reverse('courses-detail', kwargs={'pk': first_course.pk})
        response = api_client.get(url)
        assert response.status_code == HTTP_200_OK
        assert response.data.get('name') == first_course.name

# 2) проверка получения списка курсов
    def test_get_list(self, api_client, course_factory):
        course_factory(_quantity=7)
        response = api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 7

# 3) проверка фильтрации списка курсов по id
    def test_id_filter(self, api_client):
        response = api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        Course.objects.bulk_create(THREE_COURSES)
        last_course_id = Course.objects.last().id
        response = api_client.get(self.url_list, data={'id': last_course_id})
        assert response.status_code == HTTP_200_OK
        assert response.data[0].get('name') == 'Course C'

# 4) проверка фильтрации списка курсов по name
    def test_name_filter(self, api_client):
        response = api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        Course.objects.bulk_create(THREE_COURSES)
        response = api_client.get(self.url_list, data={'name': 'Course A'})
        assert response.status_code == HTTP_200_OK
        assert response.data[0].get('name') == 'Course A'

# 5) тест успешного создания курса
    @pytest.mark.parametrize(FIELDS_DATA, COURSE_DATA)
    def test_successful_create(self, api_client, name, http_status):
        new_name = {'name': name}
        response = api_client.post(self.url_list, new_name)
        assert response.status_code == http_status
        assert response.data.get('name') == name

# 6) тест успешного обновления курса
    def test_successful_patch(self, api_client, course_factory):
        course_factory(_quantity=7)
        patch_course = Course.objects.first()
        new_name = {'name': 'Patch'}
        url = reverse('courses-detail', kwargs={'pk': patch_course.pk})
        response = api_client.patch(url, data=new_name)
        assert response.status_code == HTTP_200_OK
        assert Course.objects.filter(pk=patch_course.pk)[0].name == 'Patch'

# 7) тест успешного удаления курса
    def test_delete(self, api_client, course_factory):
        course_factory(_quantity=7)
        first_course = Course.objects.first()
        url = reverse('courses-detail', kwargs={'pk': first_course.pk})
        response_del = api_client.delete(url)
        assert response_del.status_code == HTTP_204_NO_CONTENT
