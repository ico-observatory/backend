from django.db import models

class Worker(models.Model):
    name = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)
    user = models.ForeignKey('auth.User', related_name='worker_user', on_delete=models.CASCADE)
    provider = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    is_alive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Version(models.Model):
    started_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    workers = models.ManyToManyField(Worker, related_name='workers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Query(models.Model):
    version = models.ForeignKey('Version', related_name='version_id', on_delete=models.CASCADE)
    domain = models.CharField(max_length=500)
    query_type = models.CharField(max_length=255)
    query_name = models.CharField(max_length=500, null=True)
    ipv4_address = models.CharField(max_length=500, null=True)
    ipv6_address = models.CharField(max_length=500, null=True)
    as_number = models.CharField(max_length=500, null=True)
    as_name = models.CharField(max_length=500, null=True)
    bgp_prefix = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QueryFile(models.Model):
    def upload_to(instance, filename):
        print(instance)
        return 'query_files/{filename}'.format(filename=filename)
    
    query_file = models.FileField(upload_to=upload_to)
    version_id = models.ForeignKey('Version', related_name='query_version_id', on_delete=models.CASCADE)
    handle_id = models.ForeignKey('HandleVersion', related_name='handle_version_id', on_delete=models.CASCADE)
    
    
class HandleVersion(models.Model):
    version_id = models.ForeignKey('Version', related_name='handle_version_id', on_delete=models.CASCADE)
    worker_id = models.ForeignKey('Worker', related_name='handle_worker_id', on_delete=models.CASCADE)
    rank_start = models.IntegerField()
    rank_end = models.IntegerField()
    handled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    