# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Service(models.Model):
    """
    It's service model to store the information of services.
    """

    CHANGE_STATUS_CHOICE =(
        ('created', 'created'),
        ('changed', 'changed'),
        ('removed', 'removed'),
    )

    service = models.CharField(max_length=52, verbose_name='Service')
    version = models.CharField(max_length=12, verbose_name="Version")
    archeive = models.BooleanField(default=False, verbose_name='Archeive service')
    change = models.CharField(max_length=12, verbose_name='Chioce', choices=CHANGE_STATUS_CHOICE, default='created')

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Update date')

    def __str__(self):
        return '{0}::{1}'.format(self.service, self.version)
