# your_app/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Employee

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'division', 'opcr_dpcr']




# # forms.py
# from django import forms
# from .models import ActivitiesOPCR
# from django.contrib.auth.models import User

from django import forms
from .models import ActivitiesOPCR, OPCR_Smart_kpi, OPCR, Employee

class ActivitiesOPCRForm(forms.ModelForm):
    class Meta:
        model = ActivitiesOPCR
        fields = [
            'smart_kpi', 'activity', 'first_half_percent',
            'first_half_unit', 'second_half_unit', 'budget', 'remarks'
        ]

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter `smart_kpi` based on the logged-in user's division
        if user:
            employee = Employee.objects.filter(user=user).first()
            if employee:
                # Retrieve OPCR records for the employee's division
                user_opcr_records = OPCR.objects.filter(division=employee.division)

                # Filter Smart KPI objects linked to these OPCR records
                self.fields['smart_kpi'].queryset = OPCR_Smart_kpi.objects.filter(assignedto=employee)

# from django import forms
# from .models import ActivitiesDPCR, Employee, IPCR_OPCR, DPCR, IPCR_DPCR

# class ActivitiesDPCRForm(forms.ModelForm):
#     class Meta:
#         model = ActivitiesDPCR
#         fields = ['dpcr_kpi', 'activity', 'first_half_percent', 
#                   'first_half_unit', 'second_half_unit', 'budget', 'remarks'] 

#     def __init__(self, *args, **kwargs):
#         # Extract the 'employee' argument from kwargs if it exists
#         employee = kwargs.pop('employee', None)
#         super().__init__(*args, **kwargs)

#         # Filter the 'DPCR_kpi' queryset based on the logged-in employee's related IPCR_DPCR records
#         if employee:
#             # Retrieve the IPCR_DPCR records linked to this employee
#             user_ipcr_dpcr_records = IPCR_DPCR.objects.filter(employee=employee)

#             # Set the queryset for DPCR_kpi to only those DPCR entries linked to the employee's IPCR_DPCR records
#             self.fields['dpcr_kpi'].queryset = DPCR.objects.filter(smart_kpi__in=user_ipcr_dpcr_records.values_list('smart_kpi_dpcr'))
#         else:
#             # If no employee is found, clear the queryset for DPCR_kpi as a fallback
#             self.fields['dpcr_kpi'].queryset = DPCR.objects.none()

from django import forms
from .models import *

class ActivitiesDPCRForm(forms.ModelForm):
    class Meta:
        model = ActivitiesDPCR
        fields = ['dpcr_kpi', 'activity', 'first_half_percent', 
                   'first_half_unit', 'second_half_unit', 'budget', 'remarks'] 

    def __init__(self, *args, **kwargs):
        # Extract user from kwargs
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        

        # Filter smart_kpi queryset based on the logged-in user
        if user:
            # Retrieve the Employee instance linked to this User
            employee = Employee.objects.filter(user=user).first()            
            if employee:
                print(employee)
                # Retrieve IPCR_OPCR records associated with the employee
                user_ipcr_dpcr_records = IPCR_DPCR.objects.filter(employee=employee)
                
                # Filter SmartKPI objects linked to these IPCR_OPCR records
                self.fields['dpcr_kpi'].queryset = DPCR.objects.filter(ipcr_dpcr__in=user_ipcr_dpcr_records)
 




class EmployeeForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())
    opcr_dpcr = forms.ChoiceField(choices=[('OPCR', 'OPCR'), ('DPCR', 'DPCR')])



# from django import forms
# from .models import IPCR_OPCR

# from django import forms
# from .models import IPCR_OPCR, Employee, OPCR_Smart_kpi

# class IPCR_OPCRForm(forms.ModelForm):
#     class Meta:
#         model = IPCR_OPCR
#         fields = ['employee', 'smart_kpi']
#         widgets = {
#             'smart_kpi': forms.CheckboxSelectMultiple(),  # Display smart_kpi as checkboxes
#             'name': forms.TextInput(attrs={'placeholder': 'Enter name for IPCR/OPCR'})
#         }

#     def __init__(self, *args, **kwargs):
#         # Pass additional queryset filters for employee and smart_kpi via kwargs
#         user_division = kwargs.pop('user_division', None)
#         super().__init__(*args, **kwargs)

#         if user_division:
#             # Filter employees based on division
#             self.fields['employee'].queryset = Employee.objects.filter(division=user_division)
#             # Filter smart_kpi choices based on division
#             self.fields['smart_kpi'].queryset = OPCR_Smart_kpi.objects.filter(opcr__division=user_division)

#     def clean(self):
#         # Add any form-level validation here if necessary
#         cleaned_data = super().clean()
#         return cleaned_data

from django import forms
from .models import IPCR_OPCR, Employee

class IPCR_OPCRForm(forms.ModelForm):
    class Meta:
        model = IPCR_OPCR
        fields = ['employee', 'smart_kpi']
        widgets = {
            'smart_kpi': forms.CheckboxSelectMultiple(),  # Use checkboxes for smart_kpi field
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Get the logged-in user from the view
        super().__init__(*args, **kwargs)

        # Filter the employee queryset based on the logged-in user's division and opcr_dpcr value
        if hasattr(user, 'employee') and user.employee.division:
            self.fields['employee'].queryset = Employee.objects.filter(
                division=user.employee.division,
                opcr_dpcr='OPCR'  # Filter based on 'OPCR' value for opcr_dpcr
            )
        
        self.fields['smart_kpi'].required = True

           

   

from django import forms
from .models import IPCR_OPCR, Employee

class Update_IPCR_OPCRForm(forms.ModelForm):
    class Meta:
        model = IPCR_OPCR
        fields = ['employee', 'smart_kpi']
        widgets = {
            'smart_kpi': forms.CheckboxSelectMultiple(),  # Use checkboxes for smart_kpi field        
        
        }
    
 
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Get the logged-in user from the view
        super().__init__(*args, **kwargs)
        
        # Filter the employee queryset based on the logged-in user's division
        if hasattr(user, 'employee') and user.employee.division:
            self.fields['employee'].queryset = Employee.objects.filter(division=user.employee.division)

        self.fields['employee'].disabled = True
        self.fields['smart_kpi'].required = True


from django import forms
from .models import IPCR_OPCR, Employee

class IPCR_DPCRForm(forms.ModelForm):
    class Meta:
        model = IPCR_DPCR
        fields = ['employee', 'smart_kpi_dpcr']
        widgets = {
            'smart_kpi_dpcr': forms.CheckboxSelectMultiple(),  # Use checkboxes for smart_kpi field
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Get the logged-in user from the view
        super().__init__(*args, **kwargs)

        # Filter the employee queryset based on the logged-in user's division and opcr_dpcr value
        if hasattr(user, 'employee') and user.employee.division:
            self.fields['employee'].queryset = Employee.objects.filter(
                division=user.employee.division,
                opcr_dpcr='DPCR'  # Filter based on 'OPCR' value for opcr_dpcr
            )
        
        self.fields['smart_kpi_dpcr'].required = True


class Update_IPCR_DPCRForm(forms.ModelForm):
    class Meta:
        model = IPCR_DPCR
        fields = ['employee', 'smart_kpi_dpcr']
        widgets = {
            'smart_kpi_dpcr': forms.CheckboxSelectMultiple(),  # Use checkboxes for smart_kpi field        
        
        }
    
 
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Get the logged-in user from the view
        super().__init__(*args, **kwargs)
        
        # Filter the employee queryset based on the logged-in user's division
        if hasattr(user, 'employee') and user.employee.division:
            self.fields['employee'].queryset = Employee.objects.filter(division=user.employee.division)

        self.fields['employee'].disabled = True
        self.fields['smart_kpi_dpcr'].required = True


from django import forms
from .models import Employee

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'designation', 'opcr_dpcr', 'locked']
        labels = {
            'name': 'Full Name',
            'designation': 'Job Title',
            'opcr_dpcr': 'Performance Category',
            'locked': 'Lock Status',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name', 'readonly': 'readonly'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title', 'readonly': 'readonly'}),
            'opcr_dpcr': forms.Select(attrs={'class': 'form-control'}),
            'locked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("This field cannot be empty.")
        return name

    def clean_locked(self):
        locked = self.cleaned_data.get('locked')
        return locked  # Custom validation can be added here if needed

# forms.py


from django import forms
from .models import OPCR_Smart_kpi, OPCR, Employee

class OPCRSmartKpiForm(forms.ModelForm):
    class Meta:
        model = OPCR_Smart_kpi
        fields = [
            'opcr', 'pillar_kpi', 'category', 'name', 'assignedto',
            'first_half_unit','first_half_percent',
            'second_half_unit',  'second_half_percent', 'budget'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Safely pop the `user` argument
        super().__init__(*args, **kwargs)
        
        # Filter employees based on the logged-in user's division
        if user and hasattr(user, 'employee') and user.employee.division:
            user_division = user.employee.division
            self.fields['assignedto'].queryset = Employee.objects.filter(division=user_division)
            self.fields['opcr'].queryset = OPCR.objects.filter(division=user_division)
        
        # Customizing field labels
        self.fields['first_half_percent'].label = 'Jan-Jun %'
        self.fields['first_half_unit'].label = 'Jan-Jun Qty'
        self.fields['name'].label = 'Smart KPI'
        self.fields['second_half_percent'].label = 'Jul-Dec %'
        self.fields['second_half_unit'].label = 'Jul-Dec Qty'
        self.fields['name'].widget = forms.Textarea(
        attrs={
        'style': 'font-family: calibre; font-size: 18px;'  # Adjust font size as needed
            }
        )
        

from django import forms
from .models import OPCR_Smart_kpi, Employee, OPCR  # Assuming OPCR is also being used

class OPCRSmartKpiForm_rate(forms.ModelForm):
    class Meta:
        model = OPCR_Smart_kpi
        fields = ['opcr','pillar_kpi','name','category','first_half_percent','second_half_percent','second_half_unit','budget_used',
                  'accomplishment_qty','accomplishment_percent','narrative']

        
        


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Safely pop the `user` argument
        super().__init__(*args, **kwargs)
        
        # Filter employees based on the logged-in user's division
        if user and hasattr(user, 'employee') and user.employee.division:
            user_division = user.employee.division
            # self.fields['assignedto'].queryset = Employee.objects.filter(division=user_division)
            # self.fields['opcr'].queryset = OPCR.objects.filter(division=user_division)
        
        # Customizing field labels
        self.fields['name'].label = 'Smart KPI'
        
        self.fields['opcr'].widget = forms.HiddenInput()
        self.fields['pillar_kpi'].widget = forms.HiddenInput()
        # self.fields['assignedto'].widget = forms.HiddenInput()
        self.fields['name'].widget = forms.HiddenInput()
        self.fields['category'].widget = forms.HiddenInput()
        # self.fields['assignedto'].widget = forms.SelectMultiple(attrs={'readonly': 'readonly'})
        

        # self.fields['assignedto'].widget = forms.Textarea(attrs={'readonly': 'readonly'})

        # self.fields['pillar_kpi'].widget.attrs['readonly'] = 'readonly'
        # self.fields['pillar_kpi'].widget.attrs['disabled'] = 'disabled'
        # self.fields['opcr'].widget.attrs['readonly'] = 'disabled'
        # self.fields['category'].widget.attrs['disabled'] = 'disabled'
        # self.fields['name'].widget = forms.Textarea(attrs={'readonly': 'readonly'})
        # self.fields['budget'].widget.attrs['disabled'] = 'disabled'
        # self.fields['budget'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'

        # self.fields['opcr'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;color:black'
        self.fields['pillar_kpi'].widget.attrs['style'] = 'font-weight: bold; font-size: 15px;color:black'
        # self.fields['name'].widget.attrs['style'] = 'font-size: 18px;color:black; font-family:Calibri, Candara, Segoe, "Segoe UI", Optima, sans-serif'

        # self.fields['first_half_percent'].widget.attrs['disabled'] = 'disabled'
        # self.fields['first_half_percent'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        # self.fields['second_half_percent'].widget.attrs['disabled'] = 'disabled'
        # self.fields['second_half_percent'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        # self.fields['first_half_unit'].widget.attrs['disabled'] = 'disabled'
        # self.fields['first_half_unit'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        # self.fields['second_half_unit'].widget.attrs['disabled'] = 'disabled'
        # self.fields['second_half_unit'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        # self.fields['budget'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        # self.fields['budget'].widget.attrs['disabled'] = 'disabled'
        self.fields['budget_used'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'

        self.fields['accomplishment_qty'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        self.fields['accomplishment_percent'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'

        self.fields['narrative'].widget = forms.Textarea()
        self.fields['narrative'].widget.attrs['style'] = 'font-size: 18px;color:black; font-family:Calibri, Candara, Segoe, "Segoe UI", Optima, sans-serif'
        
        
    


from django import forms
from .models import OPCR_Smart_kpi, Employee, OPCR  # Assuming OPCR is also being used

class OPCRSmartKpiForm_rate_final(forms.ModelForm):
    class Meta:
        model = OPCR_Smart_kpi
        fields = ['opcr','pillar_kpi','name','category','first_half_percent','second_half_percent','second_half_unit','budget_used',
                  'accomplishment_qty','accomplishment_percent','narrative','quality','efficiency','timeliness','averagescore','score','remarks']

        
        
               
        


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Safely pop the `user` argument
        super().__init__(*args, **kwargs)
        
        # Filter employees based on the logged-in user's division
        if user and hasattr(user, 'employee') and user.employee.division:
            user_division = user.employee.division
            # self.fields['assignedto'].queryset = Employee.objects.filter(division=user_division)
            # self.fields['opcr'].queryset = OPCR.objects.filter(division=user_division)
        
        # Customizing field labels
        self.fields['name'].label = 'Smart KPI'
        
        self.fields['opcr'].widget = forms.HiddenInput()
        self.fields['pillar_kpi'].widget = forms.HiddenInput()
        # self.fields['assignedto'].widget = forms.HiddenInput()
        self.fields['name'].widget = forms.HiddenInput()
        self.fields['category'].widget = forms.HiddenInput()
        # self.fields['assignedto'].widget = forms.SelectMultiple(attrs={'readonly': 'readonly'})
        

        # self.fields['assignedto'].widget = forms.Textarea(attrs={'readonly': 'readonly'})

        # self.fields['pillar_kpi'].widget.attrs['readonly'] = 'readonly'
        # self.fields['pillar_kpi'].widget.attrs['disabled'] = 'disabled'
        # self.fields['opcr'].widget.attrs['readonly'] = 'disabled'
        # self.fields['category'].widget.attrs['disabled'] = 'disabled'
        # self.fields['name'].widget = forms.Textarea(attrs={'readonly': 'readonly'})
        # self.fields['budget'].widget.attrs['disabled'] = 'disabled'
        # self.fields['budget'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'

        # self.fields['opcr'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;color:black'
        self.fields['pillar_kpi'].widget.attrs['style'] = 'font-weight: bold; font-size: 15px;color:black'
        # self.fields['name'].widget.attrs['style'] = 'font-size: 18px;color:black; font-family:Calibri, Candara, Segoe, "Segoe UI", Optima, sans-serif'

        # self.fields['first_half_percent'].widget.attrs['disabled'] = 'disabled'
        # self.fields['first_half_percent'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        # self.fields['second_half_percent'].widget.attrs['disabled'] = 'disabled'
        # self.fields['second_half_percent'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        # self.fields['first_half_unit'].widget.attrs['disabled'] = 'disabled'
        # self.fields['first_half_unit'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        # self.fields['second_half_unit'].widget.attrs['disabled'] = 'disabled'
        # self.fields['second_half_unit'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        # self.fields['budget'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        # self.fields['budget'].widget.attrs['disabled'] = 'disabled'
        self.fields['budget_used'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'

        self.fields['accomplishment_qty'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        self.fields['accomplishment_percent'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'

        self.fields['narrative'].widget = forms.Textarea()
        self.fields['narrative'].widget.attrs['style'] = 'font-size: 18px;color:black; font-family:Calibri, Candara, Segoe, "Segoe UI", Optima, sans-serif'
        
       
        self.fields['quality'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'     
        
        self.fields['efficiency'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        self.fields['timeliness'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        self.fields['averagescore'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        # self.fields['weightallocation'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        self.fields['score'].widget.attrs['style'] = 'text-align: center; font-weight: bold; font-size: 30px;'
        self.fields['remarks'].widget = forms.Textarea()
        self.fields['remarks'].widget.attrs['style'] = 'font-size: 18px;color:black; font-family:Calibri, Candara, Segoe, "Segoe UI", Optima, sans-serif'
        
        

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['division']
        
        
        
        
from django import forms
from django.contrib.auth.models import User
from .models import Employee

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.initial = None
            field.widget.attrs.update({
                'autocomplete': 'off',
                'class': 'form-control form-control-lg',  # Bootstrap large input
                'style': 'width: 100%; max-width: 100%;'  # Ensures full width
            })


from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'designation', 'opcr_dpcr']

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.initial = None
            field.widget.attrs.update({
                'autocomplete': 'off',
                'class': 'form-control form-control-lg',  # Bootstrap large input
                'style': 'width: 100%; max-width: 100%;'  # Optional for fine control
            })


