from django.contrib.auth import authenticate, login  # Add this import
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Employee, Division
from django.db import IntegrityError

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserCreationForm, EmployeeForm

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        employee_form = EmployeeForm(request.POST)

        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save()
            employee = employee_form.save(commit=False)
            employee.user = user  # Link employee to the user
            employee.save()
            login(request, user)  # Log the user in after registration
            return redirect('dashboard')  # Redirect to a success page
    else:
        user_form = UserCreationForm()
        employee_form = EmployeeForm()

    return render(request, 'opcr/register.html', {
        'user_form': user_form,
        'employee_form': employee_form
    })




def login_view(request):
    if request.user.is_authenticated:
        return redirect('landing_page')  # Replace 'landing_page' with your URL name
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Log the user in
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("landing_page")  # Replace "home" with the name of your home page or dashboard URL
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        
        return render(request, "opcr/login.html")


from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required

@login_required
def user_logout(request):
    logout(request)
    return render(request, "opcr/login.html")


from django.shortcuts import render
from django.contrib.auth.decorators import login_required



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee, KPI, ActivitiesOPCR

# your_app/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Employee, KPI, ActivitiesOPCR, ActivitiesDPCR


# def dashboard(request):
#     employees = Employee.objects.all()  # Get all employees
#     kpis = KPI.objects.all()  # Get all KPIs
#     smart_kpis = SmartKPI.objects.all()  # Get all SmartKPIs
#     activities_opcr = ActivitiesOPCR.objects.all()  # Get all OPCR activities
#     activities_dpc = ActivitiesDPCR.objects.all()  # Get all DPCR activities

#     return render(request, 'opcr/dashboard.html', {
#         'employees': employees,
#         'kpis': kpis,
#         'smart_kpis': smart_kpis,
#         'activities_opcr': activities_opcr,
#         'activities_dpc': activities_dpc,
#     })




# from django.shortcuts import get_object_or_404, redirect, render
# from .models import User, Employee, ActivitiesOPCR, ActivitiesDPCR
# from .forms import ActivitiesOPCRForm



from django.shortcuts import get_object_or_404, redirect, render
from .models import User, Employee, ActivitiesOPCR, ActivitiesDPCR
from .forms import ActivitiesOPCRForm

def employee_report(request, user_id):
    # Check if the logged-in user matches the requested user
    if request.user.id != user_id:
        return redirect('landing_page')  # Redirect to landing page if user IDs do not match

    # Retrieve user and employee instances
    employee_user = get_object_or_404(User, id=user_id)
    employee = get_object_or_404(Employee, user=employee_user)  # Ensure this is an Employee instance

    # Initialize form and set default context
    form = ActivitiesOPCRForm(user=request.user)                     
    context = {
        'employee': employee_user,
        'form': form  # Include form in context if used in template
    }
    

    # Choose the activity model and template based on employee's OPCR or DPCR status

    


    if employee.opcr_dpcr == 'OPCR':
        print(employee.opcr_dpcr,"pag sure")
        activities = ActivitiesOPCR.objects.filter(employee=user_id) \
            .select_related('smart_kpi') \
            .order_by('smart_kpi__pillar_kpi__name', 'smart_kpi__name', 'activity')
        template_name = 'opcr/employee_report.html'
        context['activities'] = activities
        return render(request, template_name, context)
    
    if employee.opcr_dpcr == 'DPCR':
        print(employee.opcr_dpcr,"way sure")
        activities = ActivitiesDPCR.objects.filter(employee=employee) \
            .select_related('dpcr_kpi').order_by('dpcr_kpi__smart_kpi__name', 'dpcr_kpi__name', 'activity')
        template_name = 'opcr/employee_report_dpcr.html'
        context['activities'] = activities
        return render(request, template_name, context)



   
 

@login_required
def confirm_delete_activity(request, activity_id):
    activity = get_object_or_404(ActivitiesOPCR, id=activity_id)
    return render(request, 'opcr/confirm_delete.html', {'activity': activity})


@login_required
def confirm_delete_activity_dpcr(request, activity_id):
    activity = get_object_or_404(ActivitiesDPCR, id=activity_id)
    return render(request, 'opcr/confirm_delete_dpcr.html', {'activity': activity})



@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(ActivitiesOPCR, id=activity_id)
    if request.method == "POST":
        activity.delete()
        messages.success(request, f'Activity "{activity.activity}" has been deleted successfully.')  # Set a success message
        print("Activity deleted and message set.")

        return redirect('employee_report', request.user.id)
        
        

    return render(request, 'confirm_delete.html', {'activity': activity})


@login_required
def delete_activity_dpcr(request, activity_id):
    activity = get_object_or_404(ActivitiesDPCR, id=activity_id)
    if request.method == "POST":
        activity.delete()
        messages.success(request, f'Activity "{activity.activity}" has been deleted successfully.')  # Set a success message
        print("Activity deleted and message set.")

        return redirect('employee_report', request.user.id)
        
        

    return render(request, 'confirm_delete_dpcr.html', {'activity': activity})



from django.shortcuts import render
from .models import Employee

def select_employee_view(request):
    employees = Employee.objects.all()  # Fetch all employees
    return render(request, 'opcr/employee.html', {
        'employees': employees,
    })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def landing_page(request):
    return render(request, 'opcr/landing_page.html')

def show_ipcr(request):
    return render(request, 'show_ipcr.html')  # Create this template as needed

def add_edit_activities(request):
    return render(request, 'add_edit_activities.html')  # Create this template as needed

# your_app_name/views.py
# your_app_name/views.py

from django.shortcuts import render, redirect
from .forms import ActivitiesOPCRForm

# def activity_view(request):
#     if request.method == "POST":
#         form = ActivitiesOPCRForm(request.POST, user=request.user)  # Pass the logged-in user
#         if form.is_valid():
#             form.save()  # Save the form; employee will be set automatically
#             return redirect('landing_page')  # Redirect after saving
#     else:
#         form = ActivitiesOPCRForm(user=request.user)  # Create form instance with logged-in user

#     return render(request, 'opcr/activities_opcr_form.html', {'activities_opcr_form': form})

# # your_app_name/views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .forms import ActivitiesOPCRForm, ActivitiesDPCRForm
from .models import User, Employee, ActivitiesOPCR, ActivitiesDPCR

class ActivitiesView(View):
    

    def get(self, request, user_id):

        if request.user.id != user_id:
            return redirect('landing_page')  # Redirect to landing page if user IDs do not match
    
        employee_user = get_object_or_404(User, id=user_id)
        employee = get_object_or_404(Employee, user=employee_user)  # Assuming Employee has a OneToOneField with User

        if employee.opcr_dpcr == 'OPCR':
            print("opcr1")
            form = ActivitiesOPCRForm(user=request.user)          
            return render(request, 'opcr/activities.html', {'form': form})
        
       
        if employee.opcr_dpcr == 'DPCR':            
            
            form = ActivitiesDPCRForm(user=request.user)  # Pass user instead of employee
            return render(request, 'opcr/activities_dpcr.html', {'form': form})
        

    def post(self, request, user_id):
        employee_user = get_object_or_404(User, id=user_id)
        employee = get_object_or_404(Employee, user=employee_user)

        # Handle OPCR form submission
        if employee.opcr_dpcr == 'OPCR':
            form = ActivitiesOPCRForm(request.POST, user=request.user)
            if form.is_valid():
                activity = form.save(commit=False)
                activity.employee = request.user  # Assign the employee instance, not request.user
                activity.save()
                # Optional: Add a success message and redirect if needed
                # messages.success(request, "Your OPCR activity has been saved successfully!")
                return redirect('employee_report', request.user.id)  # Redirect after successful form submission
            return render(request, 'opcr/activities.html', {'form': form})
        
        # Handle DPCR form submission
        if employee.opcr_dpcr == 'DPCR':
            form = ActivitiesDPCRForm(request.POST, user=request.user)  # Pass the user
            if form.is_valid():
                activity = form.save(commit=False)
                activity.employee = employee  # Assign the employee instance correctly
                activity.save()
                # Optional: Add a success message and redirect if needed
                # messages.success(request, "Your DPCR activity has been saved successfully!")
                return redirect('employee_report', request.user.id)  # Redirect after successful form submission
            return render(request, 'opcr/activities_dpcr.html', {'form': form})

        
        
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import IPCR_OPCRForm
from .models import Employee, OPCR_Smart_kpi, IPCR_OPCR

def add_ipcr_opcr(request):
    user_division = request.user.employee.division

    if request.method == 'POST':
        form = IPCR_OPCRForm(request.POST, user_division=user_division)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            smart_kpis = form.cleaned_data.get('smart_kpi', [])
            
            # Check if an IPCR_OPCR instance already exists for this employee
            ipcr_opcr_instance = IPCR_OPCR.objects.filter(employee=employee).first()
            
            if ipcr_opcr_instance:
                # Update the existing instance
                ipcr_opcr_instance.smart_kpi.set(smart_kpis)  # Update ManyToMany field in a single step
                # ipcr_opcr_instance.name = form.cleaned_data.get('name', 'IPCR/OPCR')  # Update the name if needed
                ipcr_opcr_instance.save()  # Save the updated instance
                
                messages.success(request, f"IPCR/OPCR record for {employee.name} has been updated successfully.")
            else:
                # If no instance exists, create a new one
                ipcr_opcr_instance = IPCR_OPCR.objects.create(
                    employee=employee,
                    name=form.cleaned_data.get('name', 'IPCR/OPCR')  # Set name upon creation
                )
                ipcr_opcr_instance.smart_kpi.add(*smart_kpis)  # Add smart_kpis on creation
                
                messages.success(request, f"IPCR/OPCR record for {employee.name} has been added successfully.")
            
            return redirect('landing_page')  # Adjust this to your target redirect URL
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = IPCR_OPCRForm(user_division=user_division)  # Pass user_division to filter fields

    return render(request, 'opcr/opcr_ipcr.html', {'form': form})




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import IPCR_OPCR, IPCR_DPCR, ActivitiesOPCR, ActivitiesDPCR

@login_required
def smart_kpi_not_in_activities_view(request):
    # Fetch the IPCR_OPCR record for the logged-in user
    try:
        ipcr_opcr = IPCR_OPCR.objects.get(employee__user=request.user)
    except IPCR_OPCR.DoesNotExist:
        ipcr_opcr = None

    # Fetch the IPCR_DPCR record for the logged-in user (needed for DPCR section)
    try:
        ipcr_dpcr = IPCR_DPCR.objects.get(employee__user=request.user)
    except IPCR_DPCR.DoesNotExist:
        ipcr_dpcr = None

    # Check if the user's performance type is OPCR or DPCR
    if request.user.employee.opcr_dpcr == "OPCR":
        # Initialize an empty list for missing smart KPIs in ActivitiesOPCR
        smart_kpi_not_in_activitiesopcr = []

        if ipcr_opcr:
            # Get the smart_kpi items in IPCR_OPCR
            smart_kpi_all = ipcr_opcr.smart_kpi.all()
            
            # Get smart_kpi IDs in ActivitiesOPCR for this user
            smart_kpi_in_activities = ActivitiesOPCR.objects.filter(
                employee=request.user
            ).values_list('smart_kpi_id', flat=True)

            # Filter smart_kpi that are not in ActivitiesOPCR
            smart_kpi_not_in_activitiesopcr = smart_kpi_all.exclude(id__in=smart_kpi_in_activities)

        context = {
            'smart_kpi_not_in_activitiesopcr': smart_kpi_not_in_activitiesopcr,
        }
        return render(request, 'opcr/smart_kpi_not_in_activitiesopcr.html', context)

    else:
        # Initialize an empty list for missing smart KPIs in ActivitiesDPCR
        smart_kpi_not_in_activitiesdpcr = []

        if ipcr_dpcr:
            # Get all smart_kpi_dpcr for the logged-in user in IPCR_DPCR
            smart_kpis = ipcr_dpcr.smart_kpi_dpcr.all()

            # Get all ActivitiesDPCR entries for the logged-in user
            activities_dpcr_kpis = ActivitiesDPCR.objects.filter(employee=request.user.employee).values_list('dpcr_kpi', flat=True)

            # Filter smart_kpi_dpcr items that are not in activitiesdpcr
            smart_kpi_not_in_activitiesdpcr = smart_kpis.exclude(id__in=activities_dpcr_kpis)

        # Render the template with missing smart KPIs
        return render(request, 'opcr/smart_kpi_not_in_activitiesdpcr.html', {
            'smart_kpi_not_in_activitiesdpcr': smart_kpi_not_in_activitiesdpcr
        })

# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import IPCR_DPCR, ActivitiesDPCR

# @login_required
# def missing_dpcr_kpi_view(request):
#     # Get the IPCR_DPCR for the logged-in user
#     try:
#         ipcr_dpcr = IPCR_DPCR.objects.get(employee=request.user.employee)
#     except IPCR_DPCR.DoesNotExist:
#         ipcr_dpcr = None

#     # Initialize an empty list for smart KPIs not in ActivitiesDPCR
#     smart_kpi_not_in_activitiesdpcr = []

#     if ipcr_dpcr:
#         # Get all smart_kpi_dpcr for the logged-in user in IPCR_DPCR
#         smart_kpis = ipcr_dpcr.smart_kpi_dpcr.all()

#         # Get all ActivitiesDPCR entries for the logged-in user
#         activities_dpcr_kpis = ActivitiesDPCR.objects.filter(employee=request.user.employee).values_list('dpcr_kpi', flat=True)

#         # Filter smart_kpi_dpcr items that are not in activitiesdpcr
#         smart_kpi_not_in_activitiesdpcr = smart_kpis.exclude(id__in=activities_dpcr_kpis)

#     # Render the template with missing smart KPIs
#     return render(request, 'opcr/smart_kpi_not_in_activitiesdpcr.html', {
#         'smart_kpi_not_in_activitiesdpcr': smart_kpi_not_in_activitiesdpcr
#     })


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Employee

@login_required
def lock_employee_profile(request):
    # Set the logged-in user's Employee model `locked` field to True
    employee = Employee.objects.get(user=request.user)
    employee.locked = True
    employee.save()
    
    # Redirect to the landing page after saving
    return redirect('landing_page')


from django.shortcuts import render, redirect
from .models import IPCR_OPCR, Employee
from .forms import IPCR_OPCRForm

# def update_ipcr_opcr(request):
#     if request.method == 'POST':
#         form = IPCR_OPCRForm(request.POST)
#         if form.is_valid():
#             # Check if an IPCR_OPCR instance already exists for the selected employee
#             employee = form.cleaned_data['employee']
#             ipcr_opcr, created = IPCR_OPCR.objects.get_or_create(employee=employee)
            
#             # If the instance exists, update the fields
#             ipcr_opcr.smart_kpi.set(form.cleaned_data['smart_kpi'])
#             ipcr_opcr.save()

#             return redirect('success_url')  # Redirect to a success page or where needed
#     else:
#         form = IPCR_OPCRForm()

#     return render(request, 'opcr/update_ipcr_opcr.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import IPCR_OPCR, IPCR_DPCR

def update_ipcr_opcr(request, pk):
    ipcr_opcr = get_object_or_404(IPCR_OPCR, pk=pk)
    if request.method == 'POST':
        form = Update_IPCR_OPCRForm(request.POST, instance=ipcr_opcr, user=request.user)
        if form.is_valid():
            form.save()  # Save the updated IPCR_OPCR instance
            return redirect('landing_page')  # Redirect to a success page after saving
    else:
        form = Update_IPCR_OPCRForm(instance=ipcr_opcr, user=request.user)  # Populate the form with existing data

    return render(request, 'opcr/update_ipcr_opcr.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import IPCR_OPCRForm, IPCR_DPCR
from .models import IPCR_OPCR, IPCR_DPCR, DPCR

def add_ipcr_opcr(request):
    if request.method == 'POST':
        form = IPCR_OPCRForm(request.POST, user=request.user)  

        employee = request.POST.get('employee')
        # employee = form.cleaned_data['employee']  # Get the employee instance from cleaned_data
            
            # Check if an IPCR_OPCR instance already exists for this employee
        existing_instance = IPCR_OPCR.objects.filter(employee=employee).first()
        if existing_instance:
                # Redirect to the update form if instance exists
            return redirect('update_ipcr_opcr', pk=existing_instance.pk)
        else:
            if form.is_valid():           
                form.save()  # Save the new IPCR_OPCR instance
                return redirect('landing_page')  # Redirect to a success page after saving
        
            
    else:
        form = IPCR_OPCRForm(user=request.user)  # For GET request, render an empty form

    return render(request, 'opcr/add_ipcr_opcr.html', {'form': form})


    # return render(request, 'opcr/add_ipcr_opcr.html', {'form': form})




def add_ipcr_dpcr(request):
    if request.method == 'POST':
        form = IPCR_DPCRForm(request.POST, user=request.user)  

        employee = request.POST.get('employee')
        # employee = form.cleaned_data['employee']  # Get the employee instance from cleaned_data
            
            # Check if an IPCR_OPCR instance already exists for this employee
        existing_instance = IPCR_DPCR.objects.filter(employee=employee).first()
        if existing_instance:
                # Redirect to the update form if instance exists
            return redirect('update_ipcr_dpcr', pk=existing_instance.pk)
        else:
            if form.is_valid():           
                form.save()  # Save the new IPCR_OPCR instance
                return redirect('landing_page')  # Redirect to a success page after saving
        
            
    else:
        form = IPCR_DPCRForm(user=request.user)  # For GET request, render an empty form

    return render(request, 'opcr/add_ipcr_dpcr.html', {'form': form})


    # return render(request, 'opcr/add_ipcr_opcr.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import IPCR_OPCR, IPCR_DPCR


def update_ipcr_dpcr(request, pk):
    ipcr_dpcr = get_object_or_404(IPCR_DPCR, pk=pk)
    if request.method == 'POST':
        form = Update_IPCR_DPCRForm(request.POST, instance=ipcr_dpcr, user=request.user)
        if form.is_valid():
            form.save()  # Save the updated IPCR_OPCR instance
            return redirect('landing_page')  # Redirect to a success page after saving
    else:
        form = Update_IPCR_DPCRForm(instance=ipcr_dpcr, user=request.user)  # Populate the form with existing data

    return render(request, 'opcr/update_ipcr_dpcr.html', {'form': form})



from django.shortcuts import render, get_object_or_404
from .models import Employee
from .forms import EmployeeUpdateForm

def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            # Redirect to a success page or back to the employee list
            return redirect('employee_list')  # Adjust as per your URL name
    else:
        form = EmployeeUpdateForm(instance=employee)

    return render(request, 'opcr/employee_update.html', {'form': form})



from django.shortcuts import render
from .models import Employee

def employee_list(request):
    # Fetch the logged-in user
    user = request.user

    # Filter employees based on the division of the logged-in user
    employees = Employee.objects.filter(division=user.employee.division)

    return render(request, 'opcr/employee_list.html', {'employees': employees})


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import OPCR_Smart_kpi
from .forms import OPCRSmartKpiForm

from django.urls import reverse

def update_opcr_smart_kpi(request, pk=None):
    opcr_smart_kpi = None  # Default to None for new records

    if pk:
        # Editing an existing record
        opcr_smart_kpi = get_object_or_404(OPCR_Smart_kpi, pk=pk)
        if request.method == 'POST':
            form = OPCRSmartKpiForm(user=request.user, data=request.POST, instance=opcr_smart_kpi)
            if form.is_valid():
                form.save()
                return redirect('opcr_smart_kpi_list')  # Redirect after successful update
        else:
            form = OPCRSmartKpiForm(user=request.user, instance=opcr_smart_kpi)
    else:
        # Adding a new record
        if request.method == 'POST':
            form = OPCRSmartKpiForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('opcr_smart_kpi_list')  # Redirect after successful creation
        else:
            form = OPCRSmartKpiForm(user=request.user)

    # Include the object in the context for editing
    return render(request, 'opcr/update_opcr_smart_kpi.html', {'form': form, 'object': opcr_smart_kpi})




from django.shortcuts import render, get_object_or_404, redirect
from .models import OPCR_Smart_kpi
from .forms import OPCRSmartKpiForm

def opcr_smart_kpi_page(request, pk=None):
    # Get the form filtered by the logged-in user's division
    form = OPCRSmartKpiForm(user=request.user)

    if pk:
        # If pk is provided, we are editing an existing record
        opcr_smart_kpi = get_object_or_404(OPCR_Smart_kpi, pk=pk)
        if request.method == 'POST':
            form = OPCRSmartKpiForm(user=request.user, data=request.POST, instance=opcr_smart_kpi)
            if form.is_valid():
                form.save()
                return redirect('opcr_smart_kpi_list')  # Redirect to a list page after update
        else:
            form = OPCRSmartKpiForm(user=request.user, instance=opcr_smart_kpi)
    elif request.method == 'POST':
        form = OPCRSmartKpiForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('opcr_smart_kpi_list')  # Redirect to a list page after adding new

    return render(request, 'opcr/add_opcr_smart_kpi.html', {'form': form})



# Example list view
def opcr_smart_kpi_list(request):
    opcr_smart_kpis = OPCR_Smart_kpi.objects.filter(opcr__division=request.user.employee.division).order_by('-pillar_kpi', '-name')
    

    return render(request, 'opcr/opcr_smart_kpi_list.html', {'opcr_smart_kpis': opcr_smart_kpis})


def opcr_smart_kpi_list_all(request):
    opcr_smart_kpis = OPCR_Smart_kpi.objects.all().order_by('-budget')

    

    return render(request, 'opcr/opcr_smart_kpi_list_all.html', {'opcr_smart_kpis': opcr_smart_kpis})


from django.shortcuts import render
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import *
from datetime import datetime
from io import BytesIO

def render_to_pdf(template_src, context_dict):
    # Render HTML to PDF
    template = render(None, template_src, context_dict)
    html = template.content.decode("utf-8")
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None

from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import *  # Ensure you import your model correctly

@login_required  # Ensures that only logged-in users can access this view
def generate_pdf(request):
    # Fetch the division of the logged-in user (assumed to be in the User or related Employee model)
    user_division = request.user.employee.division  # Adjust this if the division is elsewhere

    # Filter OPCR_Smart_kpi objects by the logged-in user's division
    objects = OPCR_Smart_kpi.objects.filter(opcr__division=user_division).order_by('-pillar_kpi', '-name')  # Modify according to your relationships
 
    division = request.user.employee.division


    for obj in objects:
        obj.first_half_unit = float(obj.first_half_unit or 0)
        obj.second_half_unit = float(obj.second_half_unit or 0)

        
        
    # Create the context for the PDF
    context = {
        'title': 'Your PDF Title',
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'objects': objects,
        'division': division,

        
    }
    
    # Render PDF from template
    pdf = render_to_pdf('opcr/pdf_template.html', context)
    
    if pdf:
        # Return the PDF as an inline response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="report_preview.pdf"'
        return response
    else:
        return HttpResponse("Error generating PDF", status=500)

    
    

def pdf_preview(request):
    return render(request, 'opcr/pdf_preview.html')


from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *

def rate_opcr_smart_kpi(request, pk):
    opcr_smart_kpi = get_object_or_404(OPCR_Smart_kpi, pk=pk)

    if request.method == "POST":
        form = OPCRSmartKpiForm_rate(request.POST, instance=opcr_smart_kpi)

        delete_attachments = request.POST.getlist('delete_attachments')
        if delete_attachments:
            for attachment_id in delete_attachments:
                attachment = get_object_or_404(Attachment, id=attachment_id, opcr_smart_kpi=opcr_smart_kpi)
                attachment.file.delete()  # Delete the file from storage
                attachment.delete()  # Delete the record from the database
                
        files = request.FILES.getlist('attachments')
        if form.is_valid():
            form.save()
            # Save attachments
            for file in files:
                Attachment.objects.create(opcr_smart_kpi=opcr_smart_kpi, file=file)
            return redirect('opcr_smart_kpi_list')

    else:
        form = OPCRSmartKpiForm_rate(instance=opcr_smart_kpi)

    return render(request, 'opcr/opcr_smart_kpi_rating.html', {
        'form': form,
        'opcr_smart_kpi': opcr_smart_kpi,
    })
    
    

from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *

def rate_opcr_smart_kpi_rate(request, pk):
    opcr_smart_kpi = get_object_or_404(OPCR_Smart_kpi, pk=pk)

    if request.method == "POST":
        form = OPCRSmartKpiForm_rate_final(request.POST, instance=opcr_smart_kpi)

        delete_attachments = request.POST.getlist('delete_attachments')
        if delete_attachments:
            for attachment_id in delete_attachments:
                attachment = get_object_or_404(Attachment, id=attachment_id, opcr_smart_kpi=opcr_smart_kpi)
                attachment.file.delete()  # Delete the file from storage
                attachment.delete()  # Delete the record from the database
                
        files = request.FILES.getlist('attachments')
        if form.is_valid():
            form.save()
            # Save attachments
            for file in files:
                Attachment.objects.create(opcr_smart_kpi=opcr_smart_kpi, file=file)
            return redirect('opcr_smart_kpi_list')

    else:
        form = OPCRSmartKpiForm_rate_final(instance=opcr_smart_kpi)

    return render(request, 'opcr/opcr_smart_kpi_rating _final.html', {
        'form': form,
        'opcr_smart_kpi': opcr_smart_kpi,
    })


from django.contrib import messages

def delete_opcr_smart_kpi(request, pk):
    if request.method == "POST":
        opcr_smart_kpi = get_object_or_404(OPCR_Smart_kpi, pk=pk)
        opcr_smart_kpi.delete()
        messages.success(request, "OPCR Smart KPI deleted successfully.")
        return redirect('opcr_smart_kpi_list')



import pandas as pd
from django.http import HttpResponse
from .models import Office, Division, Organization_Outcome, Pillars, Pillar_kpi, Cluster, OPCR, Employee, OPCR_Smart_kpi, KPI, DPCR, IPCR_OPCR, IPCR_DPCR, ActivitiesOPCR, ActivitiesDPCR, Attachment

# Export all data to Excel
def export_to_excel(request):
    # Query data from all models
    office_data = Office.objects.select_related(
        'division', 'organization_outcome', 'pillar'
    ).values(
        'division__name', 'division__cluster__name', 'division__cluster__acronym', 
        'name', 'year', 'status', 'organization_outcome__name', 'pillar__name'
    )
    
    division_data = Division.objects.all().values('id', 'name', 'cluster__name', 'cluster__acronym', 'classification')
    organization_outcome_data = Organization_Outcome.objects.all().values('id', 'name')
    pillar_data = Pillars.objects.all().values('id', 'name', 'Organization_Outcome__name')
    pillar_kpi_data = Pillar_kpi.objects.all().values('id', 'name', 'pillars__name', 'pillars__Organization_Outcome__name')
    cluster_data = Cluster.objects.all().values('id', 'name', 'acronym', 'director')
    opcr_data = OPCR.objects.all().values('id', 'division__name', 'name', 'year', 'status')
    employee_data = Employee.objects.all().values('id', 'user__username', 'division__name', 'name', 'designation', 'opcr_dpcr')
    opcr_smart_kpi_data = OPCR_Smart_kpi.objects.all().values(
        'id', 'opcr__division__name', 'pillar_kpi__name', 'name', 'category', 
        'first_half_percent', 'first_half_unit', 'second_half_percent', 'second_half_unit', 
        'budget', 'budget_used', 'narrative', 'accomplishment_qty', 'accomplishment_percent', 
        'evidence_file', 'quality', 'efficiency', 'timeliness', 'averagescore', 'score', 'remarks'
    )
    kpi_data = KPI.objects.all().values('id', 'office__division__name', 'office__organization_outcome__name', 'office__pillar__name', 'name')
    dpcr_data = DPCR.objects.all().values('id', 'smart_kpi__opcr__division__name', 'smart_kpi__pillar_kpi__name', 'name')
    ipcr_opcr_data = IPCR_OPCR.objects.all().values('id', 'employee__name', 'smart_kpi__name')
    ipcr_dpcr_data = IPCR_DPCR.objects.all().values('id', 'employee__name', 'smart_kpi_dpcr__name')
    activities_opcr_data = ActivitiesOPCR.objects.all().values('id', 'employee__username', 'smart_kpi__name', 'activity')
    activities_dpcr_data = ActivitiesDPCR.objects.all().values('id', 'employee__name', 'dpcr_kpi__name', 'activity')
    attachment_data = Attachment.objects.all().values('id', 'opcr_smart_kpi__name', 'file')

    # Create an Excel writer in memory
    excel_file = pd.ExcelWriter("exported_data.xlsx", engine='openpyxl')

    # Write data to Excel sheets
    pd.DataFrame(office_data).to_excel(excel_file, sheet_name="Offices", index=False)
    pd.DataFrame(division_data).to_excel(excel_file, sheet_name="Divisions", index=False)
    pd.DataFrame(organization_outcome_data).to_excel(excel_file, sheet_name="Organization Outcomes", index=False)
    pd.DataFrame(pillar_data).to_excel(excel_file, sheet_name="Pillars", index=False)
    pd.DataFrame(pillar_kpi_data).to_excel(excel_file, sheet_name="Pillar KPIs", index=False)
    pd.DataFrame(cluster_data).to_excel(excel_file, sheet_name="Clusters", index=False)
    pd.DataFrame(opcr_data).to_excel(excel_file, sheet_name="OPCR", index=False)
    pd.DataFrame(employee_data).to_excel(excel_file, sheet_name="Employees", index=False)
    pd.DataFrame(opcr_smart_kpi_data).to_excel(excel_file, sheet_name="OPCR Smart KPIs", index=False)  # Added OPCR Smart KPIs
    pd.DataFrame(kpi_data).to_excel(excel_file, sheet_name="KPIs", index=False)
    pd.DataFrame(dpcr_data).to_excel(excel_file, sheet_name="DPCR", index=False)
    pd.DataFrame(ipcr_opcr_data).to_excel(excel_file, sheet_name="IPCR OPCR", index=False)
    pd.DataFrame(ipcr_dpcr_data).to_excel(excel_file, sheet_name="IPCR DPCR", index=False)
    pd.DataFrame(activities_opcr_data).to_excel(excel_file, sheet_name="Activities OPCR", index=False)
    pd.DataFrame(activities_dpcr_data).to_excel(excel_file, sheet_name="Activities DPCR", index=False)
    pd.DataFrame(attachment_data).to_excel(excel_file, sheet_name="Attachments", index=False)

    # Close the writer and save the Excel file
    excel_file.close()

    # Serve the Excel file as a download
    with open("exported_data.xlsx", "rb") as excel_data:
        response = HttpResponse(excel_data.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment; filename=exported_data.xlsx"
        return response


from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'opcr/employee_listnew.html', {'employees': employees})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.division = request.user.employee.division  # auto-assign division
            employee.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'opcr/employee_form.html', {'form': form, 'title': 'Add Employee'})

def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    # Optional: Only allow updates to employees in same division
    if employee.division != request.user.employee.division:
        return redirect('employee_list')  # or raise PermissionDenied

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            updated_employee = form.save(commit=False)
            updated_employee.division = request.user.employee.division  # ensure division remains correct
            updated_employee.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'opcr/employee_form.html', {'form': form, 'title': 'Edit Employee'})


def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'opcr/employee_confirm_delete.html', {'employee': employee})
