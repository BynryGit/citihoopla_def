from django.contrib import admin
from digispaceapp.models import *

#class Category(admin.ModelAdmin):
    #list_display = ['category_name']
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']    

#class CityAdmin(admin.ModelAdmin):
#    list_display = ['city_id__city_name']

# Register your models here.
admin.site.register(City_Place);
admin.site.register(Tax);
admin.site.register(UserRole);
admin.site.register(UserProfile);
admin.site.register(State);
admin.site.register(City);
admin.site.register(Pincode);
admin.site.register(Category,CategoryAdmin);
admin.site.register(CategoryLevel1,CategoryAdmin);
admin.site.register(CategoryLevel2,CategoryAdmin);
admin.site.register(CategoryLevel3,CategoryAdmin);
admin.site.register(CategoryLevel4,CategoryAdmin);
admin.site.register(CategoryLevel5,CategoryAdmin);
admin.site.register(PhoneCategory);
admin.site.register(Currency);
admin.site.register(Supplier);
admin.site.register(Advert);
admin.site.register(PhoneNo);
admin.site.register(AdvertImage);
admin.site.register(Advert_Video);
admin.site.register(WorkingHours);
admin.site.register(Amenities);
admin.site.register(NearByAttraction);
admin.site.register(NearestShopping);
admin.site.register(NearestSchool);
admin.site.register(NearestHospital);
#admin.site.register(Subscription);
admin.site.register(Business);
admin.site.register(PremiumService);
#admin.site.register(RateCard);
admin.site.register(TelephoneEnquiryRateCard);
admin.site.register(PaymentDetail);
admin.site.register(ServiceRateCard);
admin.site.register(AdvertRateCard);
admin.site.register(AdditionalAmenities);
admin.site.register(Places);
admin.site.register(ConsumerProfile);
admin.site.register(Consumer_Feedback);
admin.site.register(AdvertLike);
admin.site.register(AdvertFavourite);
admin.site.register(CategoryCityMap);
admin.site.register(AdvertSubscriptionMap);
admin.site.register(CouponCode);
admin.site.register(Advert_Category_Map);
admin.site.register(Product);
admin.site.register(Privileges);
admin.site.register(Country);
admin.site.register(SellTicket);
admin.site.register(AdvertReview);
admin.site.register(AdvertView);
admin.site.register(SellTicketLike);
admin.site.register(SellTicketFavourite);
admin.site.register(SellTicketReview);
admin.site.register(SellTicketShares);
admin.site.register(RateCard);
admin.site.register(CategoryWiseRateCard);
admin.site.register(CallerDetails);
admin.site.register(EnquiryDetails);
admin.site.register(EnquiryService);
admin.site.register(CallInfo);
admin.site.register(Operator);