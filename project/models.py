from django.db import models
from django.contrib.postgres.fields.array import ArrayField
from django.contrib.postgres.fields.jsonb import JSONField

class MonitorType(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    parameters = JSONField(null=True)

    @classmethod
    def get(self, **kwargs):
        monitor_types = self.objects.filter(**kwargs)
        if len(monitor_types)>0:
            return monitor_types[0]
        else:
            return None

    @classmethod
    def create(self, name: str, parameters=None):
        monitor_type = self(name=name, parameters=parameters)
        monitor_type.save()
        return monitor_type

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'parameters': self.parameters
        }

class Monitor(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    values = ArrayField(models.CharField(max_length=50))
    monitor_type = models.ForeignKey(MonitorType, on_delete=models.CASCADE)
    parameters = JSONField(null=True)

    @classmethod
    def get(self, all=False, **kwargs):
        monitors = self.objects.filter(**kwargs)
        if len(monitors)>0:
            if all:
                return monitors
            else:
                return monitors[0]
        else:
            return None

    @classmethod
    def create(self, **kwargs):
        if 'monitor_type' in kwargs:
            kwargs['monitor_type'] = MonitorType.get(name=kwargs.get('monitor_type'))
        monitor = self()
        for key, value in kwargs.items():
            if key == "id": continue
            if hasattr(self, key):
                setattr(monitor, key, value)
        monitor.save()
        return monitor

    def update(self, **kwargs):
        update_fields = []
        for key, value in kwargs.items():
            if key == "id": continue
            if key == "monitor_type": 
                monitor_type = MonitorType.get(name=value)
                if monitor_type: value = monitor_type
            if hasattr(self, key):
                setattr(self, key, value)
                update_fields.append(key)

        if len(update_fields) > 0:
            self.save(update_fields=update_fields)

        return self

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'values': self.values,
            'monitor_type': self.monitor_type.name,
            'parameters': self.parameters
        }