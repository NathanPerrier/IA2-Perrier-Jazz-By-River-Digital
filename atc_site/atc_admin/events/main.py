from ..config import *


class EventsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'description', 'location', 'date', 'time', 'available_tickets', 'sold', 'organizer', 'ticket_price', 'sale_release_date', 'sale_end_date', 'image' ,'last_modified')
    search_fields = ('name', 'description', 'location', 'date', 'time', 'available_tickets', 'sold', 'sale_release_date', 'sale_end_date', 'organizer', 'ticket_price', 'image')

    # def import_action(self,request):
    #     import_object_status = []
        
    #     if request.method == "POST":
    #         # clear the list for every new request
    #         create_new_characters = []
    #         # capture payload from request
    #         csv_file = json.loads(request.POST.get("file_name"))
    #         reader = json.loads(request.POST.get("rows"))
    #         column_headers = json.loads(request.POST.get("csv_headers"))
    #         # helper class for validation and other stuff
            
    #         #* handle data
            
    #         # return the response to the AJAX call
    #         context = {
    #             "file": csv_file,
    #             "entries": len(import_object_status),
    #             "results": import_object_status
    #         }
    #         return HttpResponse(json.dumps(context), content_type="application/json")
    #     # below code just displays the template once in the django-admin
    #     form = CsvImportForm()
    #     context = {"form": form, "form_title": "Upload Event data using csv file.",
    #                 "description": "The file should have following headers: "
    #                                 "[NAME,DESCRIPTION,LOCATION,DATE,TIME,AVAILABLE_TICKETS,SOLD,ORGANISER, TICKET_PRICE,SALE_RELEASE_DATE, SALE_END_DATE, IMAGE, LAST_MODIFIED, CREATION_DATE]."
    #                                 " The Following rows should contain information for the same.",
    #                                 "endpoint": "/adminevents/events/import/"}
    #     return render(
    #         request, "admin/import.html", context
    #     )