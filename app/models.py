from django.db import models
from django.contrib import admin
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User  # Для дополнительного задания
from django.contrib import admin  # Импорт модуля admin
from django.core.validators import FileExtensionValidator
from django.utils.html import format_html

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    summary = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
    # Добавленное поле для изображения
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True, verbose_name="Изображение")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blogpost", kwargs={"parametr": self.pk})  # Используем существующее имя



    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"
        ordering = ["-posted"]


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    post = models.ForeignKey('Blog', on_delete=models.CASCADE, verbose_name="Статья")  # 'Blog' — если модель Blog в том же приложении

    def __str__(self):
        return f"Комментарий от {self.user.username}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

# models.py
class Branch(models.Model):
    city = models.CharField("Город", max_length=100)
    address = models.TextField("Адрес")
    phone = models.CharField("Телефон", max_length=20)
    warning_text = models.TextField("Текст предупреждения", blank=True)
    is_warning = models.BooleanField("Показывать предупреждение", default=False)
    schedule = models.JSONField("Расписание", default=list)

    def __str__(self):
        return self.city


class CarouselImage(models.Model):
    title = models.CharField("Заголовок", max_length=200, blank=True)
    image = models.ImageField(upload_to='about/carousel/', verbose_name="Изображение")
    description = models.TextField("Описание", blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Добавил")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.title or f"Изображение #{self.id}"

    class Meta:
        verbose_name = "Изображение карусели"
        verbose_name_plural = "Изображения карусели"
        ordering = ["-created_at"]

class CompanyVideo(models.Model):
    title = models.CharField("Название видео", max_length=200)
    video_file = models.FileField(
        upload_to='about/videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])],
        help_text="Поддерживаемые форматы: MP4, WebM, Ogg"
    )
    preview_image = models.ImageField(
        upload_to='about/video_previews/',
        blank=True,
        help_text="Постер для видео (опционально)"
    )
    description = models.TextField("Описание", blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Видео компании"
        verbose_name_plural = "Видео компании"
        ordering = ["-uploaded_at"]


@admin.register(CompanyVideo)
class CompanyVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_preview', 'uploaded_at')
    readonly_fields = ('video_preview',)

    def video_preview(self, obj):
        if obj.preview_image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.preview_image.url)
        return "-"
    video_preview.short_description = "Превью"

@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'added_by', 'created_at')
    list_filter = ('added_by',)



admin.site.register(Blog); admin.site.register(Comment); admin.site.register(Branch)# Объединенная регистрация

