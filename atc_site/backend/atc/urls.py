from django.contrib import admin
from django.urls import include, path
from .views import stream_video_atc_site, contact_ajax, newsletter_ajax
from atc_site.backend import views as atc_views
from . import admin, main, views, errors, vendor

urlpatterns = [
    path("", main.index, name="atc_index"),
    
    path('events/', include('atc_site.backend.atc.events.urls')),
    path('booking/', include('atc_site.backend.atc.events.booking.urls')),
    path("", include('atc_site.backend.atc.chatbotATC.urls')),

    path("erea", main.erea, name="erea"),
    
    path("subjects", main.subjects, name="subjects"),
    path("subjects/english", main.english, name="english"),
    path("subjects/maths", main.maths, name="maths"),
    path("subjects/music", main.music, name="music"),
    path("subjects/religion", main.religion, name="religion"),
    path("subjects/science", main.science, name="science"),
    path("subjects/technology", main.technology, name="technology"),
    
    path("terms and policies", main.terms, name="terms and policies"),
    path("terms and policies/terms of use", main.terms_of_use, name="terms of use"),
    path("terms and policies/cookie policy", main.cookie, name="cookie policy"),
    path("terms and policies/safety policy", main.safety, name="safety policy"),
    path("terms and policies/copyright policy", main.copyright, name="copyright"),
    path("terms and policies/terms and conditions", main.terms_conditions, name="terms and conditions"),
    path("terms and policies/privacy policy", main.privacy, name="privacy policy"),
    
    path('contact_ajax/', contact_ajax, name='contact_ajax'),
    path('newsletter_ajax/', newsletter_ajax, name='newsletter_ajax'),
    path('stream_video/<str:video_path>/', stream_video_atc_site, name='stream_video_atc_site'),
    
    path('login', atc_views.loginViewATC, name='login'),
    
    path('register/', views.register_view, name='register'),
    path('register/get_email/', atc_views.register_get_email_view, name='register_get_email'),
    path('register/get_code/', atc_views.register_get_code_view, name='register_get_code'),
    path('register/set_password/', atc_views.register_set_password_view, name='register_set_password'),
    
    path('forgot/', views.forgot_password_view, name='forgot_password'),
    path('forgot/get_email/', atc_views.forgot_password_get_email_view, name='forgot_password_get_email'),
    path('forgot/get_code/', atc_views.forgot_password_get_code_view, name='forgot_password_get_code'),
    path('forgot/set_password/', atc_views.forgot_password_set_password_view, name='forgot_password_set_password'),
    path('forgot/confirmed', main.forgot_password_confirmed, name='forgot_password_confirmed'),
    
    path('account', main.account_page, name='account'),
    path('account/billing/', views.billing_portal_view, name='billing_portal'),
    path('account/manage', main.manage_account_page, name='manage_account'),
    
    # path('dashboard/', views.stripe_dashboard, name='stripe_dashboard'),
    path('admin/dashboard/', admin.admin_dashboard, name='dashboard_admin'),
    
    path('admin/dashboard/vouchers/', admin.vouchers_dashboard, name='vouchers_dashboard'),
    path('admin/dashboard/vouchers/<int:voucher_id>/delete/', admin.delete_voucher, name='delete_voucher'),
    
    path('admin/dashboard/bookings/', admin.bookings_dashboard, name='bookings_dashboard'),
    path('admin/dashboard/bookings/<int:booking_id>/delete/', admin.delete_booking, name='booking_dashboard'),
    
    path('admin/dashboard/users/', admin.users_dashboard, name='users_dashboard'),
    path('admin/dashboard/users/<int:user_id>/delete/', admin.delete_user, name='delete_user'),
    
    path('admin/dashboard/events/', admin.events_dashboard, name='users_dashboard'),
    path('admin/dashboard/events/<int:event_id>/delete/', admin.delete_event, name='delete_event'),
    
    path('admin/dashboard/stripe/invoices/', admin.stripe_invoice_dashboard, name='stripe_invoice'),
    
    path('admin/dashboard/vendors/', admin.vendors_dashboard, name='vendors_dashboard'),
    path('admin/dashboard/vendors/<int:vendor_id>/delete/', admin.delete_vendor, name='delete_vendor'),
    path('admin/dashboard/vendors/items/', admin.vendor_items_dashboard, name='vendor_items_dashboard'),
    path('admin/dashboard/vendors/items/<int:item_id>/activate/', admin.activate_item, name='vendor_item_atcivate'),
    path('admin/dashboard/vendors/items/<int:item_id>/deactivate/', admin.deactivate_item, name='vendor_items_deactivate'),
    path('admin/dashboard/vendors/items/<int:item_id>/edit/', admin.edit_item, name='vendor_item_edit'),
    path('admin/dashboard/vendors/items/<int:item_id>/delete/', admin.delete_item, name='vendor_item_delete'),
        
    path('vendor/dashboard/', vendor.vendor_dashboard, name='dashboard_vendor'),
    path('vendor/dashboard/items/', vendor.vendor_items, name='vendor_items'),
    path('vendor/dashboard/items/<int:item_id>/edit/', vendor.edit_item, name="vendor_item_edit"),
    path('vendor/dashboard/items/<int:item_id>/delete/', vendor.delete_item, name="vendor_item_delete"),
    path('vendor/dashboard/items/create/', vendor.create_item, name='create_item'),
    path('vendor/dashboard/orders/', vendor.vendor_orders, name='vendor_orders'),
    path('vendor/dashboard/orders/<int:order_id>/', vendor.vendor_order, name='vendor_order'),
    
    
    path('logout/', views.logout_view, name='logout'),
    
    path('404', errors.handler404, name='error_404'),
]