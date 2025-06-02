from django.db import models

# Create your models here.
# core/models.py
from django.db import models



# Status Choices
STATUS_CHOICES = [
    ('Proposed', 'Proposed'),
    ('Revised Proposed', 'Revised Proposed'),
    ('Approved', 'Approved'),
    ('Revised Approved', 'Revised Approved')
]

class Organization_Outcome(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Pillars(models.Model):
    name = models.CharField(max_length=255)
    Organization_Outcome = models.ForeignKey(Organization_Outcome,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class Pillar_kpi(models.Model):
    name = models.CharField(max_length=255)
    pillars = models.ForeignKey(Pillars, on_delete=models.CASCADE)
    def __str__(self):
        return f" {self.pillars.Organization_Outcome.name} - {self.pillars.name} | {self.name} "


class Cluster(models.Model):
    acronym  = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    director = models.CharField(max_length=255)    
    def __str__(self):
        return self.acronym

class Division(models.Model):
   
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    classification = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.name
    



class Office(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,default="OPCR")
    year = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Proposed')
    organization_outcome = models.ForeignKey(Organization_Outcome, on_delete=models.CASCADE)
    pillar = models.ForeignKey(Pillars, on_delete=models.CASCADE)  # Assuming you rename it to singular

    class Meta:
        ordering = ['year']  # Default ordering by year
        verbose_name = "Office"
        verbose_name_plural = "Offices"

    def __str__(self):
        return f"{self.division.name} | {self.name} ({self.year}- {self.status}) - {self.organization_outcome.name} | {self.pillar.name}"


class OPCR(models.Model):
    division = models.OneToOneField(Division, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,default="OPCR")
    year = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Proposed')
    pillar_kpi = models.ManyToManyField(Pillar_kpi)
    

    # class Meta:
    #     ordering = ['year']  # Default ordering by year
    #     verbose_name = "Office"
    #     verbose_name_plural = "Offices"

    def __str__(self):
        return f"{self.division.name} | {self.name} {self.year} "

from django.contrib.auth.models import User
from django.db import models

class Employee(models.Model):
    OPCR = 'OPCR'
    DPCR = 'DPCR'
    PERFORMANCE_CHOICES = [
        (OPCR, 'OPCR'),
        (DPCR, 'DPCR'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link Employee to User
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    opcr_dpcr = models.CharField(max_length=4, choices=PERFORMANCE_CHOICES, default=OPCR)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=150, null=True, blank=True)
    locked = models.BooleanField(default=False, null=True, blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    
    # def __str__(self):
    #     return f"{self.division.name} | {self.name}"
    def __str__(self):
        return f"{self.name}"

    
class OPCR_Smart_kpi(models.Model):

    Project = 'Project'
    Activity = 'Activity'
    Program = 'Program'
    Policy = 'Policy'
    CATEGORY_CHOICES = [
        (Project, 'Project'),
        (Activity, 'Activity'),
        (Program, 'Program'),
        (Policy, 'Policy'),
    ]    
    opcr = models.ForeignKey(OPCR, on_delete=models.CASCADE)
    pillar_kpi = models.ForeignKey(Pillar_kpi, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="", null=True, blank=True)
    
    first_half_percent = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    first_half_unit = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    second_half_percent = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    second_half_unit = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)    
    budget_used =models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)    
    assignedto = models.ManyToManyField(Employee)
    narrative = models.TextField(null=True, blank=True)  # Activity field with max length 250 characters
    
    accomplishment_qty= models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    accomplishment_percent = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)

    evidence_file = models.ImageField(upload_to='evidence/', null=True, blank=True)
    quality = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    efficiency = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    timeliness = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    averagescore = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    
    score = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    remarks = models.CharField(max_length=250, null=True, blank=True)  # Activity field with max length 250 characters

    def __str__(self):
        return f"{self.opcr.division.name} | {self.pillar_kpi.name} | {self.name}"


class KPI(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)  
    name = models.CharField(max_length=255)
   
   
    def __str__(self):
        return f"{self.office.division.name} - {self.office.organization_outcome.name} | {self.office.pillar.name} | {self.name} "





class DPCR(models.Model):
    smart_kpi = models.ForeignKey(OPCR_Smart_kpi, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    first_half_percent = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    first_half_unit = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    second_half_percent = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    second_half_unit = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    def __str__(self):
        return f"{self.smart_kpi.opcr.division.name} | {self.smart_kpi.pillar_kpi.name} | {self.smart_kpi.name} | {self.name}"


from django.contrib.auth.models import User

# models.py




from django.db import models

class IPCR_OPCR(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)  # One-to-One relationship with Employee
    smart_kpi = models.ManyToManyField(OPCR_Smart_kpi)  # Many-to-Many relationship with SmartKPI
    name = models.CharField(max_length=255, default="IPCR/OPCR")  # Optional name field for clarity

    def __str__(self):
        return f"{self.name} | {self.employee.name}"


class IPCR_DPCR(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)  # One-to-One relationship with Employee
    smart_kpi_dpcr = models.ManyToManyField(DPCR)  # Many-to-Many relationship with SmartKPI
    name = models.CharField(max_length=255, default="IPCR/DPCR")  # Optional name field for clarity

    def __str__(self):
        return f"{self.name} | {self.employee.name}"


class ActivitiesOPCR(models.Model):
    Approved = 'Approved'
    Revised = 'To be Revised'
    Delete = 'To be Deleted'
    STATUS_CHOICES = [
        (Approved, 'Approved'),
        (Revised, 'To be Revised'),
        (Delete, 'To be Delete'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities_opcr')  # One-to-many with Employee
    smart_kpi = models.ForeignKey(OPCR_Smart_kpi, on_delete=models.CASCADE, related_name='activities_opcr')  # One-to-many with SmartKPI
    activity = models.CharField(max_length=250)  # Activity field with max length 250 characters
    
    first_half_percent = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    first_half_unit = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    second_half_percent = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    second_half_unit = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    opcr_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="", null=True, blank=True)
    head_remarks =  models.CharField(max_length=250, null=True, blank=True)  # Activity field with max length 250 characters
    narrative = models.TextField(null=True, blank=True)  # Activity field with max length 250 characters
    evidence_file = models.ImageField(upload_to='evidence/', null=True, blank=True)
    quality = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    efficiency = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    timeliness = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    averagescore = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    weightallocation = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    remarks = models.CharField(max_length=250, null=True, blank=True)  # Activity field with max length 250 characters
    

    def __str__(self):
        return f"{self.smart_kpi.opcr.division.name} | {self.employee.username} | {self.smart_kpi.name} | {self.activity}"


class ActivitiesDPCR(models.Model):

    Approved = 'Approved'
    Revised = 'To be Revised'
    Delete = 'To be Deleted'
    STATUS_CHOICES = [
        (Approved, 'Approved'),
        (Revised, 'To be Revised'),
        (Delete, 'To be Delete'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='ActivitiesDPCR')  # One-to-many with Employee
    dpcr_kpi = models.ForeignKey(DPCR, on_delete=models.CASCADE, related_name='ActivitiesDPCR')  # One-to-many with SmartKPI
    activity = models.CharField(max_length=250)  # Activity field with max length 250 characters
    
    first_half_percent = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    first_half_unit = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    second_half_percent = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    second_half_unit = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    dpcr_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="", null=True, blank=True)
    head_remarks =  models.CharField(max_length=250, null=True, blank=True)  # Activity field with max length 250 characters
    narrative = models.TextField(null=True, blank=True)  # Activity field with max length 250 characters    
    quality = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    efficiency = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    timeliness = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    averagescore = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    weightallocation = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    remarks = models.CharField(max_length=250, null=True, blank=True)  # Activity field with max length 250 characters


    def __str__(self):
        return f"{self.dpcr_kpi.smart_kpi.opcr.division.name} | {self.employee.name} | {self.activity}"

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

# File size validation
def validate_file_size(value):
    file_size_limit = 5 * 1024 * 1024  # 5 MB
    if value.size > file_size_limit:
        raise ValidationError("The file size must not exceed 5 MB.")

def validate_file_extension(value):
    valid_extensions = ['.pdf', '.docx', '.xlsx']
    if not any(value.name.endswith(ext) for ext in valid_extensions):
        raise ValidationError(f"Only {', '.join(valid_extensions)} files are allowed.")

class Attachment(models.Model):
    opcr_smart_kpi = models.ForeignKey(
        'OPCR_Smart_kpi',
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(
        upload_to='attachments/', 
        validators=[validate_file_extension, validate_file_size]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.opcr_smart_kpi.name} - {self.file.name}"
