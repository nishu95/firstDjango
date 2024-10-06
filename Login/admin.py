import csv
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.urls.resolvers import URLPattern
from .models import Admin
from .form import CsvImportForm
from django.contrib import messages



class AdminAdmin(admin.ModelAdmin):
    list_display=['name','email']
    print("inside admin panel")

    def get_urls(self):
        print("inside get_urls() method")
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/',self.import_csv,name="import_csv"),
        ]
        return custom_urls + urls
    
    def import_csv(self, request):
        print("inside import_csv() method")
        # Check if the request method is POST
        if request.method == "POST":
            # Check if the form contains a file in 'csv_file'
            if 'csv_file' in request.FILES:
                csv_file = request.FILES['csv_file']

                # Ensure the file is a CSV
                if not csv_file.name.endswith('.csv'):
                    self.message_user(request, "This is not a CSV file!", level=messages.ERROR)
                    return render(request, "admin/csv_form.html", {'form': CsvImportForm()})

                try:
                    # Read and process the CSV file
                    file_data = csv_file.read().decode("utf-8")
                    csv_data = csv.reader(file_data.splitlines())

                    # Assuming the first row is the header
                    header = next(csv_data)

                    for row in csv_data:
                        data_dict = dict(zip(header, row))

                        # Replace 'YourModel' and 'field1', 'field2', etc. with your actual model and fields
                        Admin.objects.create(
                            name=data_dict['name'],  
                            email=data_dict['email'],
                        )

                    self.message_user(request, "CSV file imported successfully!", level=messages.SUCCESS)
                except Exception as e:
                    self.message_user(request, f"Error during CSV import: {str(e)}", level=messages.ERROR)

            else:
                # No file was uploaded
                self.message_user(request, "No file uploaded. Please select a CSV file.", level=messages.ERROR)

        # If not POST or any other errors, re-render the form
        form = CsvImportForm()
        return render(request, "admin/csv_form.html", {'form': form})
   


# Register your model and custom admin
admin.site.register(Admin, AdminAdmin)




