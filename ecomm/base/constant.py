
STATE_CHOICES = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),
("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),
("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),
("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),
("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),
("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),
("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),
("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),
("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),
("Puducherry","Puducherry"))



STATE_CHOICES = (('Maharashtra','Maharashtra'),('Goa','Goa'),('Gujrat','Gujrat'))
CITY_CHOICES =(('Pune','Pune'),('Mumbai','Mumbai'),('Banglore','Banglore'),('Delhi','Dehli'),)
PAYMENT_CHOICES =(('wallet','wallet'),('card','card'),('netbanking','netbanking'),('emi','emi'),('paypal','paypal'),('cod','cod'))


STATUS_CHOICES =(

    ('Accepted','Accepted'),('Packed','Packed'),
    ('On The Way','On The Way'),('Delivered','Delivered'),('Cancel','Cancel')
)


CHOICES =(
    ("N", "Normal"),
    ("F", "Fcaebook"),
    ("G", "Google"),
    ("T", "Twitter"),
)   



choices = (('Received', 'Received'),
        ('Scheduled', 'Scheduled'), 
        ('Shipped', 'Shipped'),
        ('In_Progress','In_Progress'),
        )